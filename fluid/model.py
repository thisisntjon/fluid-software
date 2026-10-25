"""Validated project contracts and shared filesystem primitives.

Briefs are data. Commands recorded in them are never executed by this package.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any


class FluidError(ValueError):
    """An actionable input, ownership, or project-state problem."""


_SLUG = re.compile(r"^[a-z][a-z0-9_-]*$")
_RESERVED = {".git", ".agents", ".codex", ".aws", ".fluid"}
_DEVICES = {"con", "prn", "aux", "nul", "clock$"}
_DEVICES.update(f"{prefix}{i}" for prefix in ("com", "lpt") for i in range(1, 10))


def canonical_digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise FluidError("Path must be a nonempty project-relative string.")
    normalized = value.replace("\\", "/")
    if normalized.startswith("/"):
        raise FluidError(f"Absolute path is not allowed: {value}")
    parts = normalized.split("/")
    for part in parts:
        if part in ("", ".", "..") or part.endswith((".", " ")):
            raise FluidError(f"Ambiguous or traversing path is not allowed: {value}")
        if any(ord(c) < 32 or c in '<>:"|?*' for c in part):
            raise FluidError(f"Path contains a nonportable character: {value}")
        if part.split(".")[0].casefold() in _DEVICES:
            raise FluidError(f"Reserved device path is not allowed: {value}")
    return "/".join(parts)


def _not_link(path: Path) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return
    if stat.S_ISLNK(metadata.st_mode) or (
        getattr(metadata, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    ):
        raise FluidError(f"Linked/reparse path is not allowed: {path}")


def inside(root: Path, relative: str) -> Path:
    relative = safe_relative(relative)
    base = Path(root).expanduser().absolute()
    for ancestor in reversed((base, *base.parents)):
        _not_link(ancestor)
    current = base
    for part in relative.split("/"):
        if current.exists():
            if not current.is_dir():
                raise FluidError(f"Path parent is not a directory: {current}")
            for sibling in current.iterdir():
                if sibling.name.casefold() == part.casefold() and sibling.name != part:
                    raise FluidError(f"Portable case collision: {sibling.name} versus {part}")
        current = current / part
        _not_link(current)
    resolved = current.resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise FluidError(f"Path escapes project root: {relative}")
    return current


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _under(path: str, prefix: str) -> bool:
    path, prefix = path.casefold(), prefix.casefold()
    return path == prefix or path.startswith(prefix + "/")


def _paths_overlap(a: str, b: str) -> bool:
    return _under(a, b) or _under(b, a)


def validate_brief(spec: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["Brief must be a JSON object."]
    if spec.get("schema_version") != 1:
        errors.append("schema_version must be 1.")
    if not isinstance(spec.get("id"), str) or not _SLUG.fullmatch(spec["id"]):
        errors.append("Project id must be a lowercase slug beginning with a letter.")
    for field in ("name", "outcome"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            errors.append(f"Project {field} must be nonempty text.")

    def strings(container, field, label, required=False):
        value = container.get(field, [])
        if not isinstance(value, list) or any(
            not isinstance(v, str) or not v.strip() for v in value
        ) or (required and not value):
            errors.append(f"{label}.{field} must be {'a nonempty' if required else 'a'} list of nonempty strings.")
            return []
        if len(value) != len(set(value)):
            errors.append(f"{label}.{field} contains duplicates.")
        return value

    def user_path(value, label):
        try:
            normalized = safe_relative(value)
            if any(p.casefold() in _RESERVED for p in normalized.split("/")):
                raise FluidError(f"Reserved tool/authority destination: {value}")
            return normalized
        except FluidError as exc:
            errors.append(f"{label}: {exc}")
            return None

    strings(spec, "acceptance", "project", True)
    strings(spec, "constraints", "project")
    strings(spec, "entrypoints", "project")
    for source in strings(spec, "sources", "project"):
        user_path(source, "source")
    if "state_entry" in spec:
        user_path(spec["state_entry"], "state_entry")
    modules = spec.get("modules")
    if not isinstance(modules, list) or not modules:
        errors.append("modules must be a nonempty list.")
        return errors
    by_id: dict[str, dict] = {}
    homes: dict[str, str] = {}
    ownership: list[tuple[str, str]] = []
    for index, module in enumerate(modules):
        label = f"modules[{index}]"
        if not isinstance(module, dict):
            errors.append(f"{label} must be an object.")
            continue
        module_id = module.get("id")
        if not isinstance(module_id, str) or not _SLUG.fullmatch(module_id):
            errors.append(f"{label}.id must be a lowercase slug.")
            continue
        label = module_id
        if module_id in by_id:
            errors.append(f"Duplicate module id: {module_id}")
        by_id[module_id] = module
        for field in ("name", "purpose", "owner"):
            if not isinstance(module.get(field), str) or not module[field].strip():
                errors.append(f"{label}.{field} must be nonempty text.")
        home = user_path(module.get("home"), f"{label}.home")
        if home:
            if home.casefold() in homes:
                errors.append(f"Module home collision: {home}")
            homes[home.casefold()] = module_id
        for owned in strings(module, "owns", label, True):
            normalized = user_path(owned, f"{label}.owns")
            if normalized:
                for existing, other in ownership:
                    if other != module_id and _paths_overlap(existing, normalized):
                        errors.append(f"Ownership overlaps: {other}:{existing} and {module_id}:{normalized}")
                ownership.append((normalized, module_id))
        for field in ("outputs", "acceptance"):
            strings(module, field, label, True)
        for field in ("inputs", "commands", "depends_on", "build_after", "context"):
            strings(module, field, label)
        for source in module.get("context", []) if isinstance(module.get("context", []), list) else []:
            user_path(source, f"{label}.context")
    for module_id, module in by_id.items():
        for field in ("depends_on", "build_after", "parent"):
            values = [module[field]] if field == "parent" and module.get(field) else module.get(field, []) if field != "parent" else []
            if not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, str) or value not in by_id:
                    errors.append(f"{module_id}.{field} references unknown module {value!r}.")
                elif value == module_id:
                    errors.append(f"{module_id}.{field} cannot reference itself.")
    for field in ("depends_on", "build_after", "parent"):
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(module_id):
            if module_id in visiting:
                errors.append(f"Cycle in {field} at {module_id}.")
                return
            if module_id in visited:
                return
            visiting.add(module_id)
            module = by_id[module_id]
            edges = [module[field]] if field == "parent" and module.get(field) else module.get(field, []) if field != "parent" else []
            if isinstance(edges, list):
                for edge in edges:
                    if isinstance(edge, str) and edge in by_id:
                        visit(edge)
            visiting.remove(module_id)
            visited.add(module_id)
        for module_id in by_id:
            visit(module_id)
    artifacts = spec.get("artifacts", [])
    if not isinstance(artifacts, list):
        errors.append("artifacts must be a list.")
        artifacts = []
    artifact_paths: list[str] = []
    generated = ["FRAME.md"] + [m['home'].replace('\\', '/') + '/MODULE.md' for m in by_id.values() if isinstance(m.get("home"), str)]
    for module_id, module in by_id.items():
        if isinstance(module.get("home"), str):
            contract_path = module['home'].replace('\\', '/') + '/MODULE.md'
            for owned, owner in ownership:
                if owner != module_id and _paths_overlap(contract_path, owned):
                    errors.append(f"Generated contract overlaps another module's ownership: {contract_path} and {owner}:{owned}")
    for index, artifact in enumerate(artifacts):
        label = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{label} must be an object.")
            continue
        path = user_path(artifact.get("path"), label)
        if not path:
            continue
        if any(_paths_overlap(path, other) for other in artifact_paths + generated):
            errors.append(f"Artifact/generated path collision: {path}")
        artifact_paths.append(path)
        owner = artifact.get("owner")
        if owner == "shared":
            if any(_paths_overlap(path, owned) for owned, _ in ownership):
                errors.append(f"Shared artifact overlaps module ownership: {path}")
        elif not isinstance(owner, str) or owner not in by_id or not any(
            owner == other and _under(path, owned) for owned, other in ownership
        ):
            errors.append(f"Artifact {path} does not match declared owner {owner!r}.")
        if not isinstance(artifact.get("purpose"), str) or not artifact["purpose"].strip():
            errors.append(f"{label}.purpose must be nonempty text.")
        if ("content" in artifact) == ("copy_from" in artifact):
            errors.append(f"{label} needs exactly one of content or copy_from.")
        if "content" in artifact and not isinstance(artifact["content"], str):
            errors.append(f"{label}.content must be text.")
        if "copy_from" in artifact:
            try:
                safe_relative(artifact["copy_from"])
            except FluidError as exc:
                errors.append(f"{label}.copy_from: {exc}")
        if "sha256" in artifact and (not isinstance(artifact["sha256"], str) or not re.fullmatch(r"[0-9a-fA-F]{64}", artifact["sha256"])):
            errors.append(f"{label}.sha256 must have 64 hexadecimal characters.")
    return list(dict.fromkeys(errors))


def load_brief(path: Path) -> dict:
    try:
        spec = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FluidError(f"Cannot read project brief {path}: {exc}") from exc
    errors = validate_brief(spec)
    if errors:
        raise FluidError("Invalid project brief:\n- " + "\n- ".join(errors))
    return spec


def read_project(root: Path) -> dict:
    return load_brief(inside(root, ".fluid/project.json"))


def get_module(spec: dict, module_id: str) -> dict:
    for module in spec["modules"]:
        if module["id"] == module_id:
            return module
    raise FluidError(f"Unknown module {module_id!r}; choose one from project modules.")


def downstream(spec: dict, ids: set[str]) -> set[str]:
    result = set(ids)
    while True:
        found = {
            module["id"] for module in spec["modules"]
            if result.intersection(module.get("depends_on", []) + module.get("build_after", []))
        }
        if found <= result:
            return result
        result.update(found)
