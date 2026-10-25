#!/usr/bin/env python3
"""Offline, source-linked research passage retrieval. Python 3.11+, stdlib only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nav_index import NavigatorError, build_index, load_index, status
from nav_search import export, search, show


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="Search actual Markdown, text, and Word sources with native locations and byte-checked freshness.")
    commands = cli.add_subparsers(dest="command", required=True)
    for name, description in (
        ("index", "Build or atomically replace an index from a source directory."),
        ("search", "Find a case-insensitive literal phrase, normalizing whitespace."),
        ("show", "Read a complete indexed passage by its stable ID."),
        ("export", "Save selected source passages and provenance as Markdown."),
        ("status", "Hash every indexed source and report current, changed, or missing."),
    ):
        command = commands.add_parser(name, help=description, description=description)
        command.add_argument("--index", required=True, type=Path, help="Index JSON file; relative or absolute path.")
        command.add_argument("--json", action="store_true", help="Emit exactly one JSON value on stdout; errors go to stderr.")
        if name == "index":
            command.add_argument("--source-dir", required=True, type=Path, help="Recursively read .md, .txt and .docx sources here.")
        if name in {"search", "export"}:
            command.add_argument("--query", required=True, help="Nonempty literal phrase; quote queries containing spaces.")
            command.add_argument("--limit", type=int, default=10, help="Maximum matching passages (positive integer; default: 10).")
        if name == "show":
            command.add_argument("--id", required=True, help="Complete passage ID returned by search.")
        if name == "export":
            command.add_argument("--output", required=True, type=Path, help="UTF-8 Markdown report path; parent directories are created.")
    return cli


def print_passage(item: dict) -> None:
    location = item["locator"]
    print(f"{item['source']} — {location['kind']} {location['start']}–{location['end']} — {item['status']}")
    print(f"ID: {item['id']}")
    print(f"Heading: {' → '.join(item['headings']) or '(unheaded)'}")
    print(f"Indexed SHA-256: {item['sha256']}")
    print(item["text"])


def main(argv: list[str] | None = None) -> int:
    # Windows redirected stdout is frequently cp1252; JSON and text must retain Unicode.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        index = build_index(args.source_dir, args.index) if args.command == "index" else load_index(args.index)
        if args.command in {"index", "status"}:
            result = status(index)
        elif args.command == "search":
            result = {"matches": search(index, args.query, args.limit)}
        elif args.command == "show":
            result = show(index, args.id)
        else:
            result = export(index, args.index, args.query, args.limit, args.output)
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        elif args.command in {"index", "status"}:
            print(f"{len(result['sources'])} sources; {result['passage_count']} passages")
            for source in result["sources"]:
                print(f"{source['status']:7}  {source['source']}  {source['sha256']}")
            if result["ignored"]:
                print(f"Ignored {len(result['ignored'])} unsupported files.")
        elif args.command == "search":
            print(f"{len(result['matches'])} matching passages")
            for item in result["matches"]:
                print()
                print_passage(item)
        elif args.command == "show":
            print_passage(result)
        else:
            print(f"Exported {result['passage_count']} passages to {result['output']}")
        return 0
    except (NavigatorError, OSError, UnicodeError) as exc:
        print(f"navigator: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
