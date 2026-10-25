"""Materialize an inspected project brief without replacing existing files."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile

from .model import (
    FluidError,
    canonical_digest,
    get_module,
    inside,
    safe_relative,
    sha256_file,
    validate_brief,
)


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _destination(root: Path, relative: str) -> Path:
    path = inside(root, relative)
    parent = path.parent
    while True:
        if parent.exists() and not parent.is_dir():
            raise FluidError(f"Target parent is not a directory: {parent}")
        if parent == root:
            break
        if parent.parent == parent:
            raise FluidError(f"Target is outside the declared root: {relative}")
        parent = parent.parent
    return path


def _list(lines: list[str], title: str, values: list[str]) -> None:
    lines.extend([f"### {title}", ""])
    lines.extend(f"- {value}" for value in values)
    if not values:
        lines.append("None declared.")
    lines.append("")


def _source(root: Path, relative: str, live: bool) -> str:
    relative = safe_relative(relative)
    label = f"`{relative}` (project-relative)"
    if not live:
        return label
    path = inside(root, relative)
    if path.is_file():
        return f"{label}; SHA-256 `{sha256_file(path)}`"
    if path.is_dir():
        return f"{label}; directory"
    return f"{label}; missing"


def _check_state(value: object, spec: dict) -> dict:
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise FluidError("Runtime state must be a schema_version 1 object")
    if value.get("project_id") != spec["id"] or value.get("spec_digest") != canonical_digest(spec):
        raise FluidError("Runtime state belongs to a different brief")
    modules = value.get("modules")
    if not isinstance(modules, dict) or set(modules) != {module["id"] for module in spec["modules"]}:
        raise FluidError("Runtime state module IDs do not match the brief")
    for module_id, record in modules.items():
        if not isinstance(record, dict) or record.get("status") not in {"planned", "active", "delivered", "accepted", "blocked"}:
            raise FluidError(f"Invalid runtime record for module {module_id}")
        for name in ("delivery", "acceptance"):
            receipt = record.get(name)
            if receipt is not None and (not isinstance(receipt, dict) or not isinstance(receipt.get("evidence"), dict)):
                raise FluidError(f"Invalid {name} receipt for module {module_id}")
    return value


def _recorded_status(state: dict | None, module_id: str) -> str:
    if state is None:
        return "planned; implementation not established by framing"
    item = state.get("modules", {}).get(module_id, {})
    return str(item.get("status", "planned")) + " (recorded; use status/verify for freshness)"


def _receipt_lines(lines: list[str], root: Path, record: dict, name: str) -> None:
    receipt = record.get(name)
    if not receipt:
        return
    lines.extend([f"### Recorded {name}", ""])
    lines.append(f"- Receipt: `{receipt.get('id', 'unspecified')}`")
    lines.append(f"- Actor: {receipt.get('actor', 'unspecified')}")
    lines.append(f"- Recorded at: {receipt.get('at', 'unspecified')}")
    if receipt.get("note"):
        lines.append(f"- Observation / limits: {receipt['note']}")
    evidence = receipt.get("evidence") or {}
    if evidence.get("path"):
        lines.append(f"- Evidence: {_source(root, evidence['path'], True)}")
        lines.append(f"- Recorded evidence SHA-256: `{evidence.get('sha256', 'unspecified')}`")
    if receipt.get("dependencies"):
        lines.append("- Dependency snapshots: " + ", ".join(f"`{key}`" for key in receipt["dependencies"]))
    lines.append("")


def _module_lines(
    lines: list[str], spec: dict, root: Path, module: dict,
    state: dict | None, live: bool, heading: str,
) -> None:
    module_id = module["id"]
    lines.extend([f"## {heading}: {module['name']} (`{module_id}`)", "", module["purpose"], ""])
    lines.extend([
        f"- Owner role: {module['owner']}",
        f"- Native home: `{module['home']}`",
        f"- Parent: `{module['parent']}`" if module.get("parent") else "- Parent: whole project",
        f"- Implementation status: {_recorded_status(state, module_id)}",
        "- Semantic dependencies: " + (", ".join(f"`{item}`" for item in module.get("depends_on", [])) or "none"),
        "- Build prerequisites: " + (", ".join(f"`{item}`" for item in module.get("build_after", [])) or "none"),
        "",
    ])
    _list(lines, "Owned changes", [_source(root, value, live) for value in module["owns"]])
    _list(lines, "Inputs and shared meaning", module.get("inputs", []))
    _list(lines, "Promised outputs", module["outputs"])
    _list(lines, "Completion observations", module["acceptance"])
    _list(lines, "Relevant original sources", [_source(root, value, live) for value in module.get("context", [])])
    _list(lines, "Local commands (instructions; not executed by Fluid)", [f"`{value}`" for value in module.get("commands", [])])
    consumers = [item["id"] for item in spec["modules"] if module_id in item.get("depends_on", [])]
    lines.extend(["Consumers: " + (", ".join(f"`{value}`" for value in consumers) or "none declared"), ""])
    if live and state:
        record = state.get("modules", {}).get(module_id, {})
        if record.get("actor"):
            lines.extend([f"Current actor: {record['actor']}", ""])
        for name in ("delivery", "acceptance"):
            _receipt_lines(lines, root, record, name)


def _render(spec: dict, root: Path, module_id: str | None, state: dict | None, live: bool) -> str:
    lines = [f"# {spec['name']} — project frame", "", spec["outcome"], ""]
    lines.extend([
        f"Project: `{spec['id']}` · brief SHA-256: `{canonical_digest(spec)}`",
        "",
        "Paths below are relative to the project root. Read linked original artifacts before changing their behavior.",
        "Runtime records describe work and evidence; they do not grant authority. Checksums identify bytes, not correctness.",
        "",
    ])
    if not live:
        lines.extend([
            "This is the initial frame, not an implementation or acceptance claim. Native artifacts may contain unfinished behavior.",
            "Run `python fluid.py context TARGET` for live context and `python fluid.py status TARGET` for readiness and stale evidence.",
            "",
        ])
    if spec.get("state_entry"):
        pointer = safe_relative(spec["state_entry"])
        # These relative links are correct in FRAME.md, which lives at project root.
        lines.extend([f"Existing authoritative project record: [{pointer}](<{pointer}>).", ""])
    _list(lines, "Whole-project acceptance", spec["acceptance"])
    _list(lines, "Global constraints", spec.get("constraints", []))
    _list(lines, "Whole-project sources", [_source(root, value, live) for value in spec.get("sources", [])])
    _list(lines, "Entrypoints (instructions; not executed by Fluid)", [f"`{value}`" for value in spec.get("entrypoints", [])])
    lines.extend(["## Complete capability map", ""])
    for module in spec["modules"]:
        parent = f"; parent `{module['parent']}`" if module.get("parent") else ""
        lines.append(f"- **{module['name']}** (`{module['id']}`{parent}): {module['purpose']}")
        lines.append(f"  Home `{module['home']}`; owner {module['owner']}; {_recorded_status(state, module['id'])}.")
    lines.extend([
        "",
        "`depends_on` records meaning and consumer relationships. Only `build_after` gates dispatch; a declared interface may support work before its implementation exists.",
        "",
    ])
    if module_id is not None:
        selected = get_module(spec, module_id)
        ancestors = []
        ancestor = selected
        while ancestor.get("parent"):
            ancestor = get_module(spec, ancestor["parent"])
            ancestors.append(ancestor)
        rendered = {module_id}
        for ancestor in reversed(ancestors):
            _module_lines(lines, spec, root, ancestor, state, live, "Ancestor responsibility")
            rendered.add(ancestor["id"])
        _module_lines(lines, spec, root, selected, state, live, "Current area / assignment")
        for dependency in dict.fromkeys(selected.get("depends_on", []) + selected.get("build_after", [])):
            if dependency not in rendered:
                _module_lines(lines, spec, root, get_module(spec, dependency), state, live, "Direct neighboring contract")
                rendered.add(dependency)
        lines.extend([
            "## Continue this responsibility", "",
            "Inspect owned artifacts and original input sources, check build prerequisites with `status`, and use the promised outputs and completion observations above to choose the next useful change.",
            "Record actual delivery evidence before requesting acceptance. If a shared contract is wrong, identify affected consumers and revise it through the project owner.",
            "",
        ])
    else:
        lines.extend([
            "## Continue the project", "",
            "Use `python fluid.py status TARGET` to find ready work and stale evidence; then `python fluid.py context TARGET --module ID` for the chosen responsibility and its neighboring contracts.",
            "Existing source artifacts, the declared completion observations, and actual evidence determine useful progress. A generated module home does not establish implementation.",
            "",
        ])
    return "\n".join(lines)


def render_context(spec: dict, root: Path, module_id: str | None = None) -> str:
    """Render live source pointers and recorded state without executing commands."""
    errors = validate_brief(spec)
    if errors:
        raise FluidError("Invalid project brief: " + "; ".join(errors))
    root = Path(root).absolute()
    path = inside(root, ".fluid/state.json")
    state = None
    if path.exists():
        try:
            state = _check_state(json.loads(path.read_text(encoding="utf-8")), spec)
        except (OSError, ValueError) as error:
            raise FluidError(f"Cannot read runtime state: {error}") from error
    return _render(spec, root, module_id, state, True)


def plan_frame(spec: dict, brief_dir: Path, target: Path) -> dict:
    """Read all inputs and describe all file actions before materialization."""
    errors = validate_brief(spec)
    if errors:
        raise FluidError("Invalid project brief: " + "; ".join(errors))
    target = Path(target).absolute()
    brief_dir = Path(brief_dir).absolute()
    spec_digest = canonical_digest(spec)
    plan = {"project_id": spec["id"], "target": str(target), "spec_digest": spec_digest,
            "files": [], "conflicts": [], "content": {}}
    kinds: dict[str, str] = {}
    spellings: dict[str, str] = {}

    def add(relative: str, content: bytes, kind: str) -> None:
        relative = safe_relative(relative)
        key = relative.casefold()
        if key in spellings:
            plan["conflicts"].append(f"Generated/artifact path collision: {spellings[key]} and {relative}")
            return
        spellings[key] = relative
        plan["content"][relative] = content
        kinds[relative] = kind

    add(".fluid/project.json", _json_bytes(spec), "project")
    add("FRAME.md", _render(spec, target, None, None, False).encode("utf-8"), "context")
    for module in spec["modules"]:
        relative = safe_relative(module["home"] + "/MODULE.md")
        # Module documents declare project-relative pointers rather than misleading local links.
        text = _render(spec, target, module["id"], None, False)
        if spec.get("state_entry"):
            pointer = safe_relative(spec["state_entry"])
            text = text.replace(f"[{pointer}](<{pointer}>)", f"`{pointer}` (project-relative)")
        add(relative, text.encode("utf-8"), "context")
    for artifact in spec.get("artifacts", []):
        relative = artifact["path"]
        try:
            if "content" in artifact:
                content = artifact["content"].encode("utf-8")
            else:
                source = inside(brief_dir, safe_relative(artifact["copy_from"]))
                if not source.is_file():
                    raise FluidError(f"Copy source is not a regular file: {artifact['copy_from']}")
                content = source.read_bytes()
            if artifact.get("sha256") and _digest(content) != artifact["sha256"].lower():
                raise FluidError(f"Source SHA-256 does not match for {relative}")
            add(relative, content, "native")
        except (OSError, FluidError) as error:
            plan["conflicts"].append(f"Artifact {relative}: {error}")
    manifest = {"schema_version": 1, "project_id": spec["id"], "spec_digest": spec_digest,
                "files": {relative: _digest(content) for relative, content in sorted(plan["content"].items())}}
    add(".fluid/manifest.json", _json_bytes(manifest), "manifest")
    initial_state = {"schema_version": 1, "project_id": spec["id"], "spec_digest": spec_digest,
                     "modules": {module["id"]: {"status": "planned", "actor": None, "delivery": None,
                                                "acceptance": None} for module in spec["modules"]}, "events": []}
    add(".fluid/state.json", _json_bytes(initial_state), "state")

    # Reject planned file/parent collisions even when neither path exists yet.
    names = {relative.casefold() for relative in plan["content"]}
    for relative in plan["content"]:
        for parent in PurePosixPath(relative).parents:
            if str(parent).casefold() in names:
                plan["conflicts"].append(f"Planned file is also a parent directory: {parent}")
    same_project = False
    try:
        project_path = _destination(target, ".fluid/project.json")
        same_project = project_path.is_file() and project_path.read_bytes() == plan["content"][".fluid/project.json"]
    except (OSError, FluidError) as error:
        plan["conflicts"].append(str(error))
    for relative, content in plan["content"].items():
        digest = _digest(content)
        action = "create"
        try:
            path = _destination(target, relative)
            if path.exists():
                if not path.is_file():
                    raise FluidError("Target exists and is not a regular file")
                existing = path.read_bytes()
                if relative == ".fluid/state.json" and same_project:
                    _check_state(json.loads(existing), spec)
                    action, digest = "preserve-runtime", _digest(existing)
                elif existing == content:
                    action = "identical"
                else:
                    raise FluidError("Existing file differs; v1 preserves it and requires an unused target or explicit reconciliation")
        except (OSError, ValueError) as error:
            action = "conflict"
            plan["conflicts"].append(f"{relative}: {error}")
        plan["files"].append({"path": relative, "action": action, "sha256": digest, "kind": kinds[relative]})
    return plan


def _atomic_create(root: Path, relative: str, content: bytes) -> bool:
    """Publish complete bytes with a hard link; never replace an existing path."""
    path = _destination(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path = _destination(root, relative)
    temporary: str | None = None
    try:
        descriptor, temporary = tempfile.mkstemp(prefix=".fluid-write-", dir=path.parent)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        path = _destination(root, relative)
        try:
            os.link(temporary, path)
        except FileExistsError:
            path = _destination(root, relative)
            if path.is_file() and path.read_bytes() == content:
                return False
            raise FluidError(f"Target changed while applying frame: {relative}")
        return True
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def apply_frame(plan: dict) -> dict:
    """Apply a checked frame one atomic file at a time; interruption is resumable."""
    if plan["conflicts"]:
        raise FluidError("Frame has conflicts: " + "; ".join(plan["conflicts"]))
    root = Path(plan["target"]).absolute()
    actions = []
    # Recheck every path before creating any file, including preview/apply drift.
    for entry in plan["files"]:
        relative = safe_relative(entry["path"])
        path = _destination(root, relative)
        content = plan["content"][relative]
        preserve = entry["action"] == "preserve-runtime"
        if not preserve and _digest(content) != entry["sha256"]:
            raise FluidError(f"Plan content changed: {relative}")
        if path.exists():
            if not path.is_file() or sha256_file(path) != entry["sha256"]:
                raise FluidError(f"Target changed since preview: {relative}")
            actions.append((relative, "preserve-runtime" if preserve else "identical", content))
        elif preserve or entry["action"] == "identical":
            raise FluidError(f"Target disappeared since preview: {relative}")
        else:
            actions.append((relative, "create", content))
    result = {"project_id": plan["project_id"], "target": str(root), "spec_digest": plan["spec_digest"],
              "created": [], "unchanged": [], "preserved": []}
    for relative, action, content in actions:
        if action == "preserve-runtime":
            result["preserved"].append(relative)
        elif action == "identical":
            result["unchanged"].append(relative)
        else:
            if _atomic_create(root, relative, content):
                result["created"].append(relative)
            else:
                result["unchanged"].append(relative)
    return result
