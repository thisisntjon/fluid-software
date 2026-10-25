"""Frozen initial integration contracts; revise explicitly if actual evidence requires it.

Index is a JSON-compatible dict with schema_version=1, source_dir (absolute),
sources (list of source/sha256 dicts), passages (list of public PASSAGE dicts).
Stored passages omit dynamic status; query/show attach status from current bytes.
Parsing owns text, native locators, heading context and deterministic IDs.
Storage owns atomic JSON persistence and current/changed/missing source status.
Query owns literal normalized-whitespace phrase matching and full passage lookup.
CLI owns public arguments, JSON/diagnostics and readable evidence export.
Functions raise NavigatorError for actionable user failures; no fake success.
"""

class NavigatorError(ValueError):
    pass
