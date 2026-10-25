# FluidSoftware

A local starting kit for building software with AI coding agents: make the intended whole visible (`FRAME.md`), materialize native module interfaces (`areas/*/MODULE.md`), separate semantic contracts (`depends_on`) from dispatch gates (`build_after`), render three-tier bounded context packets, and track hash-bound delivery and independent review receipts.

**Working foundation `v0.1.1` (schema v1; frozen `v0.1.0` tagged at `v0.1.0-frozen`), Python 3.11+, standard library only.** No installation, account, background service, or model API key is required. Your host coding agent reasons about architecture in its existing harness; `fluid.py` validates the brief, materializes the workspace safely, renders scoped context, and verifies version-bound receipts.

## Quick start (under 30 seconds)

Validate and materialize the self-hosted `fluid` foundation brief into a temporary folder, then run the unit test suite and the paired Research Navigator comparison demo:

```bash
python fluid.py validate foundation.project.json
python fluid.py frame foundation.project.json ./tmp-self-host
python fluid.py frame foundation.project.json ./tmp-self-host --apply
python ./tmp-self-host/fluid.py verify ./tmp-self-host --json

python -m unittest discover -s tests -v
python examples/research-navigator/run_demo.py
```

`frame` without `--apply` is a read-only preview. Give your agent [starter-kit/BUILD.md](starter-kit/BUILD.md), your project idea, and the target directory. It inspects reusable assets first and writes a declarative brief following [docs/FOUNDATION-CONTRACT.md](docs/FOUNDATION-CONTRACT.md).

## Core workflow

```bash
python fluid.py status path/to/project
python fluid.py context path/to/project --module parsing
python fluid.py claim path/to/project parsing --actor builder-1
python fluid.py deliver path/to/project parsing --actor builder-1 --evidence evidence/parsing.md --note "Actual commands, observations and limits"
python fluid.py accept path/to/project parsing --actor reviewer-2 --evidence evidence/review.md --note "Independent observed behavior"
python fluid.py verify path/to/project --json
```

When a shared upstream contract or file changes after downstream work was delivered, `fluid.py status` and `fluid.py verify` automatically detect the SHA-256 mismatch across `depends_on` edges and mark affected downstream modules `stale`:

```bash
python fluid.py block path/to/project parsing --actor builder-1 --note "Missing source fixture"
python fluid.py invalidate path/to/project parsing --actor builder-1 --note "Upstream contract changed; re-verify consumers"
```

## What is in this repository

- **`fluid.py` and `fluid/` (`1,264` LOC, Python 3.11+ stdlib):**
  - `fluid/model.py`: Schema v1 validation, 3-DAG cycle and reference checks (`parent`, `depends_on`, `build_after`), portable path confinement, and canonical SHA-256 digests.
  - `fluid/frame.py`: Read-only frame preview (`plan_frame`), hard-link atomic file creation (`apply_frame`), and three-tier bounded context packets (`render_context`).
  - `fluid/state.py`: Exclusive `.fluid/state.lock`, lifecycle transitions (`claim`, `deliver`, `accept`, `block`, `invalidate`), and transitive SHA-256 staleness propagation.
  - `fluid/__main__.py`: CLI parser, human and `--json` output envelopes, and exit codes (`0` current/ok, `1` stale/unverified, `2` validation/conflict error, `130` interrupted).
- **`starter-kit/` and `docs/`:**
  - Agent workflow templates ([START.md](starter-kit/START.md), [BUILD.md](starter-kit/BUILD.md), [SCAFFOLD.md](starter-kit/SCAFFOLD.md), [PROJECT.md](starter-kit/PROJECT.md), [WORK-UNIT.md](starter-kit/WORK-UNIT.md), [RESULT.md](starter-kit/RESULT.md), [ADAPTERS.md](starter-kit/ADAPTERS.md)) and specifications ([DESIGN.md](docs/DESIGN.md), [FOUNDATION-CONTRACT.md](docs/FOUNDATION-CONTRACT.md), [EVALUATION.md](docs/EVALUATION.md), [QOL.md](docs/QOL.md)).
- **`research/`:**
  - Audited synthesis ([SYNTHESIS.md](research/SYNTHESIS.md)) and deep-dive notes on decomposition stopping rules ([scaffold-scaling.md](research/scaffold-scaling.md)), contract construction ([scaffold-construction.md](research/scaffold-construction.md)), context mechanisms ([mechanisms.md](research/mechanisms.md)), verification ([verification.md](research/verification.md)), and adversarial failure modes ([challenge.md](research/challenge.md)).
- **`examples/research-navigator/`:**
  - Complete artifacts from the matched with/without comparison ([PROTOCOL.md](examples/research-navigator/PROTOCOL.md), [RESULTS.md](examples/research-navigator/RESULTS.md), [EVALUATOR-REVIEW.md](examples/research-navigator/EVALUATOR-REVIEW.md)), both delivered 5-command Python CLIs ([runs/foundation/](examples/research-navigator/runs/foundation/README.md) and [runs/control/](examples/research-navigator/runs/control/README.md)), the frozen evaluator and oracle adjudication scripts (`evaluate.py`, `adjudicate_newlines.py`, `adjudicate_headings.py`), and a self-contained runner (`run_demo.py`).
- **`showcase/fluid-architecture-showcase.html`:**
  - Self-contained offline SVG explainer illustrating module-bounded decomposition, the 3-DAG model, 3-tier context lenses, and hash-bound staleness propagation.

## Measured comparison and honest limits

1. **Matched Research Navigator comparison ([examples/research-navigator/RESULTS.md](examples/research-navigator/RESULTS.md)):**
   - On 2026-10-23, one fresh builder given a 4-module Fluid frame (`runs/foundation`) and one fresh builder using an ordinary workflow (`runs/control`) built a 5-command offline Python CLI (`index`, `search`, `show`, `export`, `status`) over four documents.
   - Both builders satisfied **13/13** protocol checks on their unchanged first-delivery bytes after adjudicating two defects in the frozen evaluation harness (`Path.read_text()` newline normalization in `adjudicate_newlines.py` and a valid CommonMark setext heading in `adjudicate_headings.py`).
   - Because target-frame authoring (`navigator.project.json`) was completed before builder dispatch and manual/adjudication review was required in both arms on an $n = 1$ paired run, **this comparison demonstrates workflow feasibility and oracle accountability rather than a net speed multiplier**.
2. **Operational boundaries:**
   - `frame --apply` never overwrites existing differing files; once starter files are edited, `v1` reports conflicts rather than attempting automatic code migration.
   - `verify` proves byte identity and receipt freshness across the dependency graph; it does not replace behavioral testing or independent code review.
   - Tag `v0.1.0-frozen` preserves the exact initial October 23 freeze; `v0.1.1` tightens `fluid/model.py` so falsey non-null `parent` values (`""`, `0`, `false`) are rejected as invalid module IDs rather than coerced to `None`.

## License

MIT License. See [LICENSE](LICENSE).
