"""Unit and integration tests for the zero-dependency FluidSoftware CLI and data model."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fluid import __version__
from fluid.frame import apply_frame, plan_frame, render_context
from fluid.model import FluidError, canonical_digest, load_brief, read_project, validate_brief
from fluid.state import status, transition, verify


def make_minimal_brief() -> dict:
    return {
        "schema_version": 1,
        "id": "demo-app",
        "name": "Demo App",
        "outcome": "Verify 3-DAG validation, frame materialization, and transitive staleness.",
        "acceptance": ["All unit tests pass."],
        "constraints": ["Standard library only."],
        "modules": [
            {
                "id": "core",
                "name": "Core",
                "purpose": "Define core data structures.",
                "owner": "core-maintainer",
                "home": "areas/core",
                "owns": ["src/core.py"],
                "outputs": ["Core types"],
                "acceptance": ["Core types import cleanly."],
                "depends_on": [],
                "build_after": [],
            },
            {
                "id": "service",
                "name": "Service",
                "purpose": "Implement business rules over Core.",
                "owner": "service-maintainer",
                "home": "areas/service",
                "parent": "core",
                "owns": ["src/service.py"],
                "outputs": ["Service operations"],
                "acceptance": ["Service calls Core."],
                "depends_on": ["core"],
                "build_after": ["core"],
            },
        ],
        "artifacts": [
            {
                "path": "src/core.py",
                "owner": "core",
                "purpose": "Core starter module",
                "content": "VALUE = 1\n",
            },
            {
                "path": "src/service.py",
                "owner": "service",
                "purpose": "Service starter module",
                "content": "from .core import VALUE\n",
            },
        ],
    }


class FluidModelAndLifecycleTests(unittest.TestCase):
    def test_version_is_0_1_1(self) -> None:
        self.assertEqual(__version__, "0.1.1")

    def test_valid_brief_has_no_errors(self) -> None:
        brief = make_minimal_brief()
        errors = validate_brief(brief)
        self.assertEqual(errors, [])
        self.assertEqual(len(canonical_digest(brief)), 64)

    def test_falsey_non_null_parent_rejected(self) -> None:
        for bad_parent in ["", 0, False, []]:
            with self.subTest(bad_parent=bad_parent):
                brief = make_minimal_brief()
                brief["modules"][0]["parent"] = bad_parent
                errors = validate_brief(brief)
                self.assertTrue(errors, f"Expected validation error for parent={bad_parent!r}")

    def test_cycle_detection_across_all_three_dags(self) -> None:
        for edge_field in ["parent", "depends_on", "build_after"]:
            with self.subTest(edge_field=edge_field):
                brief = make_minimal_brief()
                if edge_field == "parent":
                    brief["modules"][0]["parent"] = "service"
                    brief["modules"][1]["parent"] = "core"
                else:
                    brief["modules"][0][edge_field] = ["service"]
                    brief["modules"][1][edge_field] = ["core"]
                errors = validate_brief(brief)
                self.assertTrue(any("Cycle" in e for e in errors), f"Expected cycle error for {edge_field}: {errors}")

    def test_unsafe_paths_and_overlapping_ownership_rejected(self) -> None:
        for bad_path in ["../escape.py", "/abs/path.py", "CON.py", ".git/config"]:
            with self.subTest(bad_path=bad_path):
                brief = make_minimal_brief()
                brief["modules"][0]["owns"] = [bad_path]
                errors = validate_brief(brief)
                self.assertTrue(errors, f"Expected path error for {bad_path!r}")

        overlap = make_minimal_brief()
        overlap["modules"][1]["owns"] = ["src/core.py"]
        self.assertTrue(any("Overlap" in e or "overlap" in e for e in validate_brief(overlap)))

    def test_full_lifecycle_staleness_and_invalidation(self) -> None:
        brief = make_minimal_brief()
        with tempfile.TemporaryDirectory(prefix="fluid-test-") as tmp:
            tmp_dir = Path(tmp)
            spec_path = tmp_dir / "project.json"
            target_dir = tmp_dir / "workspace"
            spec_path.write_text(json.dumps(brief, indent=2), encoding="utf-8")

            spec = load_brief(spec_path)
            plan = plan_frame(spec, spec_path.parent, target_dir)
            self.assertEqual(plan["conflicts"], [])
            self.assertFalse(target_dir.exists())

            applied = apply_frame(plan)
            self.assertTrue((target_dir / "FRAME.md").is_file())
            self.assertTrue((target_dir / ".fluid/state.json").is_file())
            self.assertGreater(len(applied["created"]), 0)

            ctx_text = render_context(read_project(target_dir), target_dir, "service")
            self.assertIn("Service (`service`)", ctx_text)
            self.assertIn("Core (`core`)", ctx_text)

            # Service cannot be claimed before core is delivered/accepted because build_after=["core"]
            with self.assertRaises(FluidError):
                transition(target_dir, "service", "claim", "builder-2", None, "")

            transition(target_dir, "core", "claim", "builder-1", None, "")
            ev_core = target_dir / "ev-core.md"
            ev_core.write_text("Core tested.\n", encoding="utf-8")
            transition(target_dir, "core", "deliver", "builder-1", "ev-core.md", "Delivered core")
            transition(target_dir, "core", "accept", "reviewer-1", "ev-core.md", "Accepted core")

            # Now service is ready to claim, deliver, and accept
            transition(target_dir, "service", "claim", "builder-2", None, "")
            ev_svc = target_dir / "ev-service.md"
            ev_svc.write_text("Service tested.\n", encoding="utf-8")
            transition(target_dir, "service", "deliver", "builder-2", "ev-service.md", "Delivered service")
            transition(target_dir, "service", "accept", "reviewer-1", "ev-service.md", "Accepted service")

            ver_ok = verify(target_dir)
            self.assertTrue(ver_ok["ok"])
            self.assertEqual(ver_ok["stale"], [])

            # Mutate upstream core.py -> both core and downstream service become stale
            (target_dir / "src/core.py").write_text("VALUE = 2\n", encoding="utf-8")
            st = status(target_dir)
            self.assertIn("core", st["stale"])
            self.assertIn("service", st["stale"])

            # Invalidate core -> resets core and downstream consumer service to planned
            transition(target_dir, "core", "invalidate", "maintainer", None, "Contract updated")
            st_after = status(target_dir)
            by_id_after = {m["id"]: m for m in st_after["modules"]}
            self.assertEqual(by_id_after["core"]["status"], "planned")
            self.assertEqual(by_id_after["service"]["status"], "planned")

    def test_foundation_self_host_brief_validates_and_frames(self) -> None:
        with tempfile.TemporaryDirectory(prefix="fluid-selfhost-") as tmp:
            target = Path(tmp) / "self-host"
            cmd = [
                sys.executable,
                str(ROOT / "fluid.py"),
                "frame",
                str(ROOT / "foundation.project.json"),
                str(target),
                "--apply",
                "--json",
            ]
            out = json.loads(subprocess.check_output(cmd, text=True, encoding="utf-8"))
            self.assertGreater(len(out["created"]), 0)

            ver_cmd = [sys.executable, str(target / "fluid.py"), "verify", str(target), "--json"]
            ver_out = json.loads(subprocess.check_output(ver_cmd, text=True, encoding="utf-8"))
            self.assertTrue(ver_out["ok"])
            self.assertEqual(ver_out["integrity_issues"], [])


if __name__ == "__main__":
    unittest.main()
