"""Recorded work state, bound to real project files and review evidence.

Actors are declarations, not authenticated identities. Hashes establish byte
identity, not correct behavior; review evidence remains a human/agent judgment.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
from uuid import uuid4

from .model import (
    FluidError, atomic_json, canonical_digest, downstream, get_module, inside,
    read_project, safe_relative, sha256_file,
)


_STATUSES = {"planned", "active", "delivered", "accepted", "blocked"}
_IGNORED_DIRS = {
    ".git", ".fluid", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".cache",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FluidError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FluidError(f"Expected a JSON object in {path}")
    return value


def _load_state(root: Path, spec: dict) -> dict:
    value = _read_json(inside(root, ".fluid/state.json"))
    if value.get("schema_version") != 1:
        raise FluidError("Unsupported state schema_version")
    if value.get("project_id") != spec["id"]:
        raise FluidError("State project_id does not match the project brief")
    if value.get("spec_digest") != canonical_digest(spec):
        raise FluidError("State spec_digest does not match the project brief")
    modules = value.get("modules")
    if not isinstance(modules, dict) or set(modules) != {m["id"] for m in spec["modules"]}:
        raise FluidError("State module IDs do not match the project brief")
    if not isinstance(value.get("events"), list):
        raise FluidError("State events must be a list")
    for module_id, record in modules.items():
        if not isinstance(record, dict) or record.get("status") not in _STATUSES:
            raise FluidError(f"Invalid state for module {module_id}")
        if record.get("actor") is not None and not isinstance(record["actor"], str):
            raise FluidError(f"Invalid recorded actor for module {module_id}")
        if record["status"] in {"active", "delivered", "accepted"} and not record.get("actor"):
            raise FluidError(f"Module {module_id} has no recorded actor")
        for key in ("delivery", "acceptance"):
            if record.get(key) is not None and not isinstance(record[key], dict):
                raise FluidError(f"Invalid {key} receipt for module {module_id}")
            receipt = record.get(key)
            if receipt is not None and any(
                not isinstance(receipt.get(field), str) or not receipt[field].strip()
                for field in ("id", "actor", "at")
            ):
                raise FluidError(f"Incomplete {key} identity for module {module_id}")
        if record["status"] in {"delivered", "accepted"} and not record.get("delivery"):
            raise FluidError(f"Module {module_id} is missing its delivery receipt")
        if record["status"] == "accepted" and not record.get("acceptance"):
            raise FluidError(f"Module {module_id} is missing its acceptance receipt")
    return value


@contextmanager
def _locked(root: Path):
    """Fail immediately on contention; never guess that somebody's lock is stale."""
    lock_path = inside(root, ".fluid/state.lock")
    token = str(uuid4())
    try:
        fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise FluidError(
            f"State is locked: {lock_path}. Another mutation may be running; "
            "inspect its process diagnostic before manually recovering a leftover lock."
        ) from exc
    except OSError as exc:
        raise FluidError(f"Cannot create state lock {lock_path}: {exc}") from exc
    identity = os.fstat(fd)
    initialized = False
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "token": token, "created_at": _now()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        initialized = True
        yield
    finally:
        # Do not remove a replacement lock created by a different process.
        try:
            current = lock_path.lstat()
            same_file = (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino)
            if same_file and (not initialized or _read_json(lock_path).get("token") == token):
                lock_path.unlink()
        except (FileNotFoundError, FluidError):
            pass


def _snapshot(root: Path, module: dict) -> dict:
    files: dict[str, str] = {}
    missing: list[str] = []

    def visit(relative: str) -> None:
        path = inside(root, relative)
        try:
            mode = path.stat().st_mode
        except FileNotFoundError:
            return
        if stat.S_ISREG(mode):
            if path.suffix.lower() not in {".pyc", ".pyo"}:
                files[relative] = sha256_file(path)
        elif stat.S_ISDIR(mode):
            for child in sorted(path.iterdir(), key=lambda item: (item.name.casefold(), item.name)):
                if child.name.casefold() not in _IGNORED_DIRS:
                    visit(f"{relative}/{child.name}")
        else:
            raise FluidError(f"Owned path is not a regular file or directory: {relative}")

    try:
        for owned in module["owns"]:
            relative = safe_relative(owned)
            path = inside(root, relative)
            if not path.exists():
                missing.append(relative)
            else:
                visit(relative)
    except OSError as exc:
        raise FluidError(f"Cannot inspect owned files for {module['id']}: {exc}") from exc
    return {"files": dict(sorted(files.items())), "missing": sorted(missing)}


def _evidence(root: Path, relative: str | None) -> dict:
    if not isinstance(relative, str) or not relative.strip():
        raise FluidError("An existing target-relative evidence file is required")
    relative = safe_relative(relative)
    if relative.split("/", 1)[0].casefold() == ".fluid":
        raise FluidError("Evidence must be outside .fluid")
    path = inside(root, relative)
    try:
        if not path.is_file():
            raise FluidError(f"Evidence is not an existing regular file: {relative}")
        return {"path": relative, "sha256": sha256_file(path), "size": path.stat().st_size}
    except OSError as exc:
        raise FluidError(f"Cannot inspect evidence {relative}: {exc}") from exc


def _evidence_issues(root: Path, evidence: object, label: str) -> list[str]:
    if not isinstance(evidence, dict) or not evidence.get("path") or not evidence.get("sha256"):
        return [f"{label} evidence receipt is invalid"]
    try:
        current = _evidence(root, evidence["path"])
    except FluidError as exc:
        return [f"{label} evidence unavailable: {exc}"]
    if current["sha256"] != evidence["sha256"]:
        return [f"{label} evidence changed: {evidence['path']}"]
    return []


def _file_changes(expected: object, actual: dict[str, str]) -> dict:
    if not isinstance(expected, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in expected.items()
    ):
        return {"invalid_snapshot": True, "added": [], "deleted": [], "modified": []}
    return {
        "added": sorted(actual.keys() - expected.keys()),
        "deleted": sorted(expected.keys() - actual.keys()),
        "modified": sorted(key for key in actual.keys() & expected.keys() if actual[key] != expected[key]),
    }


def _dependency_snapshot(spec: dict, state: dict, snapshots: dict, module: dict) -> dict:
    result = {}
    for dependency in module.get("depends_on", []):
        delivery = state["modules"][dependency].get("delivery")
        result[dependency] = {
            "outputs": deepcopy(snapshots[dependency]["files"]),
            "evidence": deepcopy(delivery.get("evidence")) if delivery else None,
        }
    return result


def _inspect(root: Path, spec: dict, state: dict) -> dict:
    snapshots, snapshot_errors = {}, {}
    for module in spec["modules"]:
        try:
            snapshots[module["id"]] = _snapshot(root, module)
        except FluidError as exc:
            snapshots[module["id"]] = {"files": {}, "missing": []}
            snapshot_errors[module["id"]] = str(exc)

    reasons: dict[str, list[str]] = {m["id"]: [] for m in spec["modules"]}
    changes = {}
    for module in spec["modules"]:
        module_id = module["id"]
        record = state["modules"][module_id]
        delivery = record.get("delivery")
        acceptance = record.get("acceptance")
        # Blocked work can retain receipts. Their freshness remains visible.
        if not delivery:
            continue
        if module_id in snapshot_errors:
            reasons[module_id].append(snapshot_errors[module_id])
        if not delivery.get("outputs"):
            reasons[module_id].append("Delivery has no recorded owned files")
        changes[module_id] = _file_changes(delivery.get("outputs"), snapshots[module_id]["files"])
        if any(changes[module_id].values()):
            reasons[module_id].append("Owned files changed since delivery")
        reasons[module_id].extend(_evidence_issues(root, delivery.get("evidence"), "Delivery"))
        current_dependencies = _dependency_snapshot(spec, state, snapshots, module)
        recorded_dependencies = delivery.get("dependencies")
        if not isinstance(recorded_dependencies, dict):
            reasons[module_id].append("Delivery dependency snapshot is invalid")
        elif recorded_dependencies != current_dependencies:
            reasons[module_id].append("Semantic dependency outputs or delivery evidence changed")
        if acceptance:
            reasons[module_id].extend(_evidence_issues(root, acceptance.get("evidence"), "Acceptance"))
            if acceptance.get("delivery_id") != delivery.get("id"):
                reasons[module_id].append("Acceptance references a different delivery")
            if not acceptance.get("actor") or acceptance.get("actor") == delivery.get("actor"):
                reasons[module_id].append("Acceptance has no distinct recorded reviewer")
            if not isinstance(acceptance.get("note"), str) or not acceptance["note"].strip():
                reasons[module_id].append("Acceptance has no recorded observation")
            if acceptance.get("outputs") != delivery.get("outputs"):
                reasons[module_id].append("Acceptance output snapshot differs from delivery")
            if acceptance.get("dependencies") != delivery.get("dependencies"):
                reasons[module_id].append("Acceptance dependency snapshot differs from delivery")

    # Semantic linkage is transitive. build_after deliberately does not imply
    # semantic dependence; it only controls when planned work can be claimed.
    changed = True
    while changed:
        changed = False
        for module in spec["modules"]:
            module_id = module["id"]
            if not state["modules"][module_id].get("delivery"):
                continue
            for dependency in module.get("depends_on", []):
                reason = f"Semantic dependency is stale: {dependency}"
                if (reasons[dependency] or dependency in snapshot_errors) and reason not in reasons[module_id]:
                    reasons[module_id].append(reason)
                    changed = True

    rows, ready, stale, blockers = [], [], [], {}
    for module in spec["modules"]:
        module_id = module["id"]
        record = state["modules"][module_id]
        gate = []
        for dependency in module.get("build_after", []):
            provider = state["modules"][dependency]
            if provider["status"] not in {"delivered", "accepted"}:
                gate.append(f"build_after {dependency} is {provider['status']}")
            elif reasons[dependency]:
                gate.append(f"build_after {dependency} is stale")
        if record["status"] == "blocked":
            gate.append(record.get("note") or "Explicitly blocked")
        if module_id in snapshot_errors:
            gate.append(snapshot_errors[module_id])
        if gate:
            blockers[module_id] = gate
        if record["status"] == "planned" and not gate:
            ready.append(module_id)
        if reasons[module_id]:
            stale.append(module_id)
        if reasons[module_id]:
            next_action = "Inspect changes, invalidate, then claim and deliver fresh evidence"
        elif record["status"] == "accepted":
            next_action = "Continue with consumers; recheck after file or evidence changes"
        elif record["status"] == "delivered":
            next_action = "A distinct reviewer records acceptance with evidence and an observation"
        elif record["status"] == "active":
            next_action = "Recorded actor completes owned outputs and delivers evidence"
        elif gate:
            next_action = "Resolve blockers before claiming work"
        else:
            next_action = "Claim with the builder actor before implementing owned outputs"
        complete = record["status"] == "accepted" and not reasons[module_id]
        rows.append({
            "id": module_id, "name": module["name"], "status": record["status"],
            "actor": record.get("actor"), "ready": module_id in ready,
            "stale": bool(reasons[module_id]), "stale_reasons": reasons[module_id],
            "blockers": gate, "home": str(inside(root, module["home"])),
            "owns": module["owns"], "artifacts": [
                {"path": path, "location": str(inside(root, path)), "sha256": digest}
                for path, digest in snapshots[module_id]["files"].items()
            ],
            "missing_owned_paths": snapshots[module_id]["missing"],
            "unfinished_outputs": [] if complete else module["outputs"],
            "changes_since_delivery": changes.get(module_id),
            "delivery": record.get("delivery"), "acceptance": record.get("acceptance"),
            "next_action": next_action,
        })
    counts = {key: sum(row["status"] == key for row in rows) for key in sorted(_STATUSES)}
    counts.update(total=len(rows), ready=len(ready), stale=len(stale))
    return {
        "ok": not stale and not snapshot_errors, "project_id": spec["id"],
        "root": str(root.resolve()), "state_path": str(inside(root, ".fluid/state.json")),
        "modules": rows, "ready": ready, "stale": stale, "blockers": blockers,
        "counts": counts, "event_count": len(state["events"]),
        "identity_note": "Actors are recorded declarations, not authenticated identities.",
    }


def status(root: Path) -> dict:
    root = Path(root)
    spec = read_project(root)
    return _inspect(root, spec, _load_state(root, spec))


def verify(root: Path) -> dict:
    root = Path(root)
    spec = read_project(root)
    result = _inspect(root, spec, _load_state(root, spec))
    manifest = _read_json(inside(root, ".fluid/manifest.json"))
    issues, managed = [], []
    if manifest.get("schema_version") != 1:
        issues.append("Unsupported manifest schema_version")
    if manifest.get("project_id") != spec["id"]:
        issues.append("Manifest project_id does not match the project brief")
    if manifest.get("spec_digest") != canonical_digest(spec):
        issues.append("Manifest spec_digest does not match the project brief")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise FluidError("Manifest files must be a nonempty path-to-hash object")
    if ".fluid/project.json" not in files:
        issues.append("Manifest is missing the project brief identity")
    for relative, digest in sorted(files.items()):
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise FluidError("Manifest contains an invalid file/hash entry")
        path = inside(root, relative)
        actual = sha256_file(path) if path.is_file() else None
        condition = "missing" if actual is None else "unchanged" if actual == digest else "modified"
        managed.append({"path": relative, "status": condition, "expected_sha256": digest, "actual_sha256": actual})
        if relative == ".fluid/project.json" and condition != "unchanged":
            issues.append("Project brief bytes differ from the frame manifest")
    result.update({
        "ok": result["ok"] and not issues, "integrity_issues": issues,
        "manifest": managed,
        "manifest_note": "Manifest hashes identify initial frame inputs. Modified or removed starter files are historical differences; current delivery and acceptance snapshots establish freshness.",
        "verification_note": "File and evidence hashes establish freshness, not behavioral correctness.",
    })
    return result


def _append_event(state: dict, module_id: str, action: str, actor: str, note: str, before: dict) -> None:
    state["events"].append({
        "id": str(uuid4()), "at": _now(), "module_id": module_id,
        "action": action, "actor": actor, "note": note,
        "before": deepcopy(before), "after": deepcopy(state["modules"][module_id]),
    })


def transition(root: Path, module_id: str, action: str, actor: str,
               evidence: str | None = None, note: str = "") -> dict:
    root = Path(root)
    if not isinstance(actor, str) or not actor.strip():
        raise FluidError("A nonempty actor declaration is required")
    actor = actor.strip()
    if not isinstance(note, str):
        raise FluidError("Note must be text")
    if action not in {"claim", "deliver", "accept", "block", "invalidate"}:
        raise FluidError(f"Unknown transition: {action}")
    if action in {"accept", "block", "invalidate"} and not note.strip():
        raise FluidError(f"{action} requires a note describing the observation or reason")
    spec = read_project(root)
    module = get_module(spec, module_id)
    with _locked(root):
        # Re-read authority under the same lock as its state read and mutation.
        spec = read_project(root)
        module = get_module(spec, module_id)
        state = _load_state(root, spec)
        record = state["modules"][module_id]
        before = deepcopy(record)
        inspection = _inspect(root, spec, state)
        row = next(item for item in inspection["modules"] if item["id"] == module_id)
        affected = [module_id]
        changed = True
        if action == "claim":
            if record["status"] == "active":
                if record["actor"] != actor:
                    raise FluidError(f"Module {module_id} is active under {record['actor']}; ownership cannot be taken over")
                changed = False
            elif record["status"] not in {"planned", "blocked"}:
                raise FluidError(f"Cannot claim {module_id} from {record['status']}; invalidate it first")
            else:
                gates = [reason for reason in row["blockers"] if reason.startswith("build_after ")]
                if gates:
                    raise FluidError(f"Cannot claim {module_id}: {'; '.join(gates)}")
                record.update(status="active", actor=actor, note=note)
        elif action == "deliver":
            if record["status"] != "active" or record["actor"] != actor:
                raise FluidError(f"Deliver requires {module_id} to be active under actor {actor}")
            snapshots = {item["id"]: _snapshot(root, item) for item in spec["modules"]}
            outputs = snapshots[module_id]["files"]
            if not outputs:
                raise FluidError(f"Cannot deliver {module_id}: no owned files exist")
            receipt = {
                "id": str(uuid4()), "at": _now(), "actor": actor, "note": note,
                "evidence": _evidence(root, evidence), "outputs": outputs,
                "dependencies": _dependency_snapshot(spec, state, snapshots, module),
            }
            record.update(status="delivered", delivery=receipt, acceptance=None, note=note)
        elif action == "accept":
            if record["status"] != "delivered":
                raise FluidError(f"Accept requires {module_id} to be delivered")
            if row["stale"]:
                raise FluidError(f"Cannot accept stale module {module_id}: {'; '.join(row['stale_reasons'])}")
            delivery = record["delivery"]
            if actor == delivery["actor"]:
                raise FluidError("Acceptance requires a distinct recorded reviewer actor")
            record.update(status="accepted", acceptance={
                "id": str(uuid4()), "at": _now(), "actor": actor, "note": note,
                "delivery_id": delivery["id"], "evidence": _evidence(root, evidence),
                "outputs": deepcopy(delivery["outputs"]),
                "dependencies": deepcopy(delivery["dependencies"]),
            }, note=note)
        elif action == "block":
            if record["status"] == "active" and record["actor"] != actor:
                raise FluidError(f"Cannot block active module {module_id} owned by {record['actor']}")
            record.update(status="blocked", actor=actor, note=note)
        else:
            selected = {module_id} | downstream(spec, {module_id})
            affected = [item["id"] for item in spec["modules"] if item["id"] in selected]
            for selected_id in affected:
                current = state["modules"][selected_id]
                if current["status"] == "active" and current["actor"] != actor:
                    raise FluidError(f"Cannot invalidate active module {selected_id} owned by {current['actor']}")
            for selected_id in affected:
                previous = deepcopy(state["modules"][selected_id])
                state["modules"][selected_id].update(
                    status="planned", actor=None, delivery=None, acceptance=None, note=note,
                )
                _append_event(state, selected_id, action, actor, note, previous)
        if changed:
            if action != "invalidate":
                _append_event(state, module_id, action, actor, note, before)
            atomic_json(inside(root, ".fluid/state.json"), state)
        result = _inspect(root, spec, state)
        result.update(action=action, module_id=module_id, affected=affected, changed=changed)
        return result
