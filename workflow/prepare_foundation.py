"""Package the actual foundation source through its own declarative frame."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    responsibilities = [
        ("model", ["fluid/model.py"], [], "Validate briefs and confine portable filesystem paths."),
        ("frame", ["fluid/frame.py"], ["model"], "Materialize native files safely and render bounded context."),
        ("state", ["fluid/state.py"], ["model"], "Preserve ownership, real evidence and delivery freshness."),
        ("cli", ["fluid.py", "fluid/__main__.py"], ["model", "frame", "state"], "Expose useful local commands and clear machine/human output."),
    ]
    modules = []
    artifacts = []
    for module_id, paths, dependencies, purpose in responsibilities:
        modules.append({"id": module_id, "name": module_id.title(), "purpose": purpose,
                        "owner": f"{module_id} maintainer", "home": f"areas/{module_id}",
                        "owns": paths, "outputs": [purpose], "acceptance": ["Actual CLI use and separate code review support the promised behavior."],
                        "depends_on": dependencies, "build_after": [],
                        "context": ["docs/FOUNDATION-CONTRACT.md"],
                        "commands": ["python fluid.py --help"]})
        for path in paths:
            artifacts.append({"path": path, "owner": module_id, "purpose": "Actual portable foundation implementation",
                              "copy_from": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()})
    for path in ["fluid/__init__.py", "docs/FOUNDATION-CONTRACT.md"]:
        artifacts.append({"path": path, "owner": "shared", "purpose": "Runtime package identity and frozen public contract",
                          "copy_from": path, "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()})
    spec = {"schema_version": 1, "id": "fluid-foundation", "name": "Portable Fluid foundation",
            "outcome": "A working portable copy of the real local project framing and continuation tool.",
            "acceptance": ["Run CLI from this directory with Python 3.11+ and no installation.", "Track actual implementation delivery and independent review with current evidence."],
            "constraints": ["No service, network, agent launching or embedded-command execution."],
            "sources": ["docs/FOUNDATION-CONTRACT.md"], "entrypoints": ["python fluid.py status .", "python fluid.py context . --module cli"],
            "modules": modules, "artifacts": artifacts}
    (ROOT / "foundation.project.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    print("foundation.project.json contains pinned actual implementation sources.")


if __name__ == "__main__":
    main()
