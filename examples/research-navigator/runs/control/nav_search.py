"""Literal retrieval, complete passage reconstruction, and Markdown evidence."""
from __future__ import annotations

import bisect
import re
from pathlib import Path

from nav_index import NavigatorError, atomic_write, freshness, source_path


def normalize(text: str) -> str:
    return " ".join(text.split()).casefold()


def normalized_offsets(text: str) -> tuple[str, list[int], list[int]]:
    """Casefold and collapse whitespace with reversible character offsets."""
    pieces, starts, ends = [], [], []
    for match in re.finditer(r"\s+|\S+", text):
        if match.group().isspace():
            pieces.append(" ")
            starts.append(match.start())
            ends.append(match.end())
        else:
            for offset, character in enumerate(match.group(), match.start()):
                folded = character.casefold()
                pieces.append(folded)
                starts.extend([offset] * len(folded))
                ends.extend([offset + 1] * len(folded))
    return "".join(pieces), starts, ends


def validate_query(query: str, limit: int) -> str:
    phrase = normalize(query)
    if not phrase:
        raise NavigatorError("Query must contain non-whitespace text")
    if limit <= 0:
        raise NavigatorError("Limit must be a positive integer")
    return phrase


def passage(index: dict, document: dict, start: int, end: int, state: dict | None = None) -> dict:
    # Exclude only boundary whitespace from location attribution, not from text.
    fragment = document["text"][start:end]
    left = start + len(fragment) - len(fragment.lstrip())
    right = end - len(fragment) + len(fragment.rstrip()) - 1
    offsets = [unit["start"] for unit in document["units"]]
    first = max(0, bisect.bisect_right(offsets, left) - 1)
    last = max(first, bisect.bisect_right(offsets, max(left, right)) - 1)
    return {
        "id": f"p1:{document['key']}:{start}:{end}",
        "source": document["source"],
        "sha256": document["sha256"],
        **(state if state is not None else freshness(index, document)),
        "locator": {"kind": document["kind"], "start": document["units"][first]["ordinal"], "end": document["units"][last]["ordinal"]},
        "headings": document["units"][first]["headings"],
        "text": fragment,
    }


def search(index: dict, query: str, limit: int) -> list[dict]:
    phrase = validate_query(query, limit)
    results = []
    for document in index["documents"]:
        normalized, starts, ends = normalized_offsets(document["text"])
        range_starts = [start for start, _ in document["ranges"]]
        cursor, seen, state = 0, set(), None
        while True:
            hit = normalized.find(phrase, cursor)
            if hit < 0:
                break
            original_start, original_end = starts[hit], ends[hit + len(phrase) - 1]
            first = max(0, bisect.bisect_right(range_starts, original_start) - 1)
            last = max(first, bisect.bisect_right(range_starts, original_end - 1) - 1)
            bounds = (document["ranges"][first][0], document["ranges"][last][1])
            if bounds not in seen:
                if state is None:
                    state = freshness(index, document)
                results.append(passage(index, document, *bounds, state))
                seen.add(bounds)
                if len(results) >= limit:
                    return results
            cursor = hit + 1
    return results


def show(index: dict, identifier: str) -> dict:
    match = re.fullmatch(r"p1:([a-f0-9]{64}):(\d+):(\d+)", identifier)
    if match:
        key, start, end = match.group(1), int(match.group(2)), int(match.group(3))
        for document in index["documents"]:
            if document["key"] == key:
                if start < end and start in {a for a, _ in document["ranges"]} and end in {b for _, b in document["ranges"]}:
                    return passage(index, document, start, end)
                break
    raise NavigatorError(f"Unknown passage ID: {identifier}")


def markdown_escape(text: str) -> str:
    return re.sub(r"([\\`*_{}\[\]<>#!|])", r"\\\1", text).replace("\n", " ")


def export(index: dict, index_path: Path, query: str, limit: int, output: Path) -> dict:
    matches = search(index, query, limit)
    destination = output.resolve()
    if destination == index_path.resolve() or any(destination == source_path(index, document).resolve() for document in index["documents"]):
        raise NavigatorError("Report output must not overwrite the index or a source file")
    lines = ["# Research Navigator evidence", "", f"Query: {markdown_escape(query)}", "", f"Passages: {len(matches)} (limit {limit})", "", f"Index created: {index['indexed_at']}", "", "The passages below are indexed source text. Source status was checked from current bytes at export time.", ""]
    for number, item in enumerate(matches, 1):
        locator = item["locator"]
        document = next(d for d in index["documents"] if d["source"] == item["source"])
        uri = source_path(index, document).resolve().as_uri()
        lines.extend([
            f"## {number}. {markdown_escape(item['source'])}", "",
            f"Source: [{markdown_escape(item['source'])}]({uri})", "",
            f"Location: {locator['kind']} {locator['start']}–{locator['end']} (inclusive, 1-based)", "",
            f"Heading context: {markdown_escape(' → '.join(item['headings'])) if item['headings'] else '(unheaded)'}", "",
            f"Source status: **{item['status']}**", "",
            f"Indexed SHA-256: `{item['sha256']}`", "",
            f"Passage ID: `{item['id']}`", "",
        ])
        if item["status"] != "current":
            lines.extend(["**This passage is retained from the index; the current source has changed or is missing.**", ""])
        # A dynamic fence preserves literal source markup, tables and Unicode.
        longest = max((len(m.group()) for m in re.finditer(r"`+", item["text"])), default=0)
        fence = "`" * max(3, longest + 1)
        lines.extend([fence + "text", item["text"], fence, ""])
    atomic_write(destination, "\n".join(lines) + "\n")
    return {"output": str(destination), "passage_count": len(matches), "sources": [{"source": item["source"], "status": item["status"]} for item in matches]}
