"""Command line for explicit project framing and evidence-bound work state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
import uuid

from .frame import apply_frame, plan_frame, render_context
from .model import FluidError, canonical_digest, load_brief, read_project
from .state import status, transition, verify


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Materialize project structure, scope agent context, and resume work from checked evidence.")
    result.add_argument("--json", action="store_true", help="Emit one JSON value on stdout.")
    commands = result.add_subparsers(dest="command", required=True)
    for name in ("validate", "frame"):
        command = commands.add_parser(name)
        command.add_argument("brief", type=Path)
        if name == "frame":
            command.add_argument("target", type=Path)
            command.add_argument("--apply", action="store_true", help="Create missing files; default is read-only preview.")
    for name in ("context", "status", "verify"):
        command = commands.add_parser(name)
        command.add_argument("target", type=Path)
        if name == "context":
            command.add_argument("--module")
    for name in ("claim", "deliver", "accept", "block", "invalidate"):
        command = commands.add_parser(name)
        command.add_argument("target", type=Path)
        command.add_argument("module_id")
        command.add_argument("--actor", required=True)
        if name in ("deliver", "accept"):
            command.add_argument("--evidence", required=True, help="Existing project-relative file containing actual observations.")
        command.add_argument("--note", default="", required=name in ("accept", "block", "invalidate"))
    return result


def _human(value: dict) -> str:
    if "context" in value:
        return value["context"]
    if "files" in value and "conflicts" in value:
        lines = [f"Frame preview: {value['project_id']} -> {value['target']}"]
        lines += [f"  {item['action']}: {item['path']}" for item in value['files']]
        lines += [f"Conflict: {item}" for item in value['conflicts']]
        lines.append("No files written. Use --apply after reviewing this plan.")
        return "\n".join(lines)
    if "created" in value:
        return f"Frame ready: {value['target']}\nCreated {len(value['created'])}; identical {len(value['unchanged'])}; preserved runtime files {len(value['preserved'])}."
    if "modules" in value and isinstance(value["modules"], list):
        lines = [f"Project: {value.get('project_id', '')}", f"Ready: {', '.join(value.get('ready', [])) or 'none'}; stale: {', '.join(value.get('stale', [])) or 'none'}"]
        for item in value["modules"]:
            lines.append(f"  {item.get('id', item.get('module_id', '?'))}: {item.get('status', '?')}" + (" (stale)" if item.get('stale') else ""))
            for reason in item.get("stale_reasons", []):
                lines.append(f"    {reason}")
        for key in ("integrity_issues", "next_actions"):
            for item in value.get(key, []):
                lines.append(f"  {item}")
        return "\n".join(lines)
    if "error" in value:
        return f"Error: {value['error']}"
    return json.dumps(value, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    arguments = list(sys.argv[1:] if argv is None else argv)
    # Accept the formatting flag before or after a subcommand.
    machine = "--json" in arguments
    arguments = [value for value in arguments if value != "--json"]
    args = parser().parse_args(arguments)
    started = time.perf_counter()
    run_id = str(uuid.uuid4())
    code = 0
    try:
        if args.command in ("validate", "frame"):
            spec = load_brief(args.brief)
            if args.command == "validate":
                result = {"ok": True, "project_id": spec["id"], "spec_digest": canonical_digest(spec), "modules": len(spec["modules"])}
            else:
                plan = plan_frame(spec, args.brief.parent, args.target)
                if args.apply:
                    result = apply_frame(plan)
                else:
                    result = {key: value for key, value in plan.items() if key != "content"}
                    code = 2 if plan["conflicts"] else 0
        elif args.command == "context":
            result = {"context": render_context(read_project(args.target), args.target, args.module)}
        elif args.command in ("status", "verify"):
            result = (verify if args.command == "verify" else status)(args.target)
            code = 0 if result.get("ok", True) else 1
        else:
            result = transition(args.target, args.module_id, args.command, args.actor, getattr(args, "evidence", None), args.note)
    except KeyboardInterrupt:
        result, code = {"ok": False, "error": "Cancelled. Run status before continuing; a partial frame can be safely re-applied."}, 130
    except (FluidError, OSError, ValueError) as error:
        result, code = {"ok": False, "error": str(error)}, 2
    result.update(run_id=run_id, elapsed_seconds=round(time.perf_counter() - started, 6))
    if machine:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(_human(result), file=sys.stderr if code == 2 else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
