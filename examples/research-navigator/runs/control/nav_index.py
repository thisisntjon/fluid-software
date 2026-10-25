"""Index persistence, source discovery, and byte-based freshness checks."""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from nav_sources import SUPPORTED, parse_source, sha256

FORMAT = "research-navigator-v1"


class NavigatorError(Exception):
    """A concise user-facing operational failure."""


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=".navigator-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def discover(root: Path) -> tuple[list[Path], list[str]]:
    files, ignored = [], []
    def fail(error):
        raise error
    for directory, folders, names in os.walk(root, onerror=fail, followlinks=False):
        folders.sort()
        for name in sorted(names):
            path = Path(directory) / name
            if path.suffix.lower() in SUPPORTED:
                files.append(path)
            else:
                ignored.append(path.relative_to(root).as_posix())
    return sorted(files, key=lambda p: p.relative_to(root).as_posix()), ignored


def build_index(source_dir: Path, index_path: Path) -> dict:
    root = source_dir.resolve()
    target = index_path.resolve()
    if not root.is_dir():
        raise NavigatorError(f"Source directory does not exist or is not a directory: {root}")
    paths, ignored = discover(root)
    if not paths:
        raise NavigatorError(f"No supported .md, .txt, or .docx files in: {root}")
    documents = []
    for path in paths:
        if path.resolve() == target:
            raise NavigatorError("The index output must not overwrite a source file")
        relative = path.relative_to(root).as_posix()
        try:
            documents.append(parse_source(path, relative))
        except Exception as exc:
            raise NavigatorError(f"Cannot parse {relative}: {exc}") from exc
    index = {"format": FORMAT, "source_dir": str(root), "indexed_at": datetime.now(timezone.utc).isoformat(), "documents": documents, "ignored": ignored}
    atomic_write(target, json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    return index


def load_index(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["format"] != FORMAT:
            raise ValueError("unsupported index format; rebuild with index")
        if not isinstance(data["indexed_at"], str) or not data["indexed_at"]:
            raise ValueError("missing index creation timestamp")
        if not isinstance(data.get("ignored", []), list) or not all(isinstance(item, str) for item in data.get("ignored", [])):
            raise ValueError("invalid ignored-file list")
        if not isinstance(data["source_dir"], str) or not Path(data["source_dir"]).is_absolute():
            raise ValueError("invalid source directory")
        if not isinstance(data["documents"], list):
            raise ValueError("invalid document list")
        keys = set()
        for document in data["documents"]:
            source = Path(document["source"])
            if source.is_absolute() or ".." in source.parts:
                raise ValueError("invalid source-relative path")
            if not re.fullmatch(r"[0-9a-f]{64}", document["sha256"]):
                raise ValueError("invalid source hash")
            expected_key = sha256((document["source"] + "\0" + document["sha256"]).encode("utf-8"))
            if document["key"] != expected_key or document["key"] in keys:
                raise ValueError("invalid or duplicate document identity")
            keys.add(document["key"])
            if document["kind"] not in {"lines", "paragraphs"} or not isinstance(document["text"], str):
                raise ValueError("invalid document text or locator kind")
            cursor = 0
            for start, end in document["ranges"]:
                if type(start) is not int or type(end) is not int or start != cursor or not start < end <= len(document["text"]):
                    raise ValueError("invalid passage range")
                cursor = end
            if cursor != len(document["text"]):
                raise ValueError("incomplete passage ranges")
            previous_start = -1
            for ordinal, unit in enumerate(document["units"], 1):
                if unit["ordinal"] != ordinal or not previous_start < unit["start"] <= unit["end"] <= len(document["text"]):
                    raise ValueError("invalid native source locations")
                if not isinstance(unit["headings"], list) or not all(isinstance(x, str) for x in unit["headings"]):
                    raise ValueError("invalid heading context")
                previous_start = unit["start"]
            if document["text"] and not document["units"]:
                raise ValueError("missing native source locations")
        return data
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise NavigatorError(f"Invalid index {path}: {exc}") from exc


def source_path(index: dict, document: dict) -> Path:
    return Path(index["source_dir"]) / document["source"]


def freshness(index: dict, document: dict) -> dict:
    path = source_path(index, document)
    try:
        current_hash = sha256(path.read_bytes())
    except FileNotFoundError:
        return {"status": "missing", "current_sha256": None}
    except OSError as exc:
        raise NavigatorError(f"Cannot check freshness of {document['source']}: {exc}") from exc
    return {"status": "current" if current_hash == document["sha256"] else "changed", "current_sha256": current_hash}


def status(index: dict) -> dict:
    return {"sources": [{"source": document["source"], "sha256": document["sha256"], **freshness(index, document)} for document in index["documents"]], "indexed_at": index["indexed_at"], "source_dir": index["source_dir"], "passage_count": sum(len(d["ranges"]) for d in index["documents"]), "ignored": index.get("ignored", [])}
