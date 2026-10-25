# FluidSoftware

A local starting kit for building with AI: make the intended whole visible, materialize native module interfaces, give agents bounded responsibilities, then connect and improve real working parts.

**Working foundation 0.1.0 (schema v1), Python 3.11+, standard library only.** No install, account, server or model API is needed. The host agent reasons about architecture and uses its existing harness; Fluid creates the reviewed files, renders scoped context and tracks version-bound work. It does not generate a sound architecture automatically or launch agents. [The real with/without comparison is complete](workflow/comparison/RESULTS.md): both fresh builders delivered independently accepted Research Navigators. Builder times were 7m51s assisted and 10m1s ordinary; untimed frame authoring and additional review prevent a total multiplier claim.

## Start a project

Give your agent [BUILD.md](starter-kit/BUILD.md), your idea, and the target directory. It inspects reuse and writes a project brief using the [field contract](docs/FOUNDATION-CONTRACT.md). Literal native artifacts belong in that brief; the tool does not generate useful code from module names alone. [navigator.project.json](workflow/comparison/navigator.project.json) is an actual example with four module interfaces, and [foundation.project.json](foundation.project.json) packages actual tool source with pinned hashes.

```text
python fluid.py validate project.json
python fluid.py frame project.json path/to/project
python fluid.py frame project.json path/to/project --apply
python fluid.py status path/to/project
python fluid.py context path/to/project --module parsing
```

`frame` without `--apply` is a read-only preview. Use an explicit Python 3.11+ executable if `python` is not on PATH. The current real portable copy can be run directly:

```text
python workspaces/foundation-v1/fluid.py status workspaces/foundation-v1
python workspaces/foundation-v1/fluid.py verify workspaces/foundation-v1 --json
```

## Build and continue

```text
python fluid.py claim path/to/project parsing --actor builder-1
python fluid.py deliver path/to/project parsing --actor builder-1 --evidence evidence/parsing.md --note "Actual commands, observations and limits"
python fluid.py accept path/to/project parsing --actor reviewer-2 --evidence evidence/review.md --note "Independent observed behavior"
python fluid.py verify path/to/project --json
```

Create real evidence files before delivery or acceptance, then keep them unchanged. A reviewer should inspect actual behavior and sources; changing the actor name is not an independent review. `--json` works before or after the command and returns a clean UTF-8 JSON value, run ID and elapsed time. State events retain old receipts under `.fluid/state.json`; source and evidence hashes identify versions, not correctness.

For continuation, run `status` and the chosen module's `context`, inspect its actual files and latest evidence, then claim ready work. `depends_on` records semantic consumers; `build_after` gates claims. Both are separate from optional parent hierarchy. No whole-project wait is implied by a semantic dependency. An earlier delivery becomes stale when its files, evidence or semantic provider snapshots change.

```text
python fluid.py block path/to/project parsing --actor builder-1 --note "Missing real source input"
python fluid.py invalidate path/to/project parsing --actor builder-1 --note "Source or shared contract changed; inspect affected consumers"
```

Invalidation resets that responsibility and transitive consumers to planned while retaining their old receipts in history. It refuses to take another actor's active work. A blocked item can be reclaimed once its real blocker is resolved. Commands never execute instructions embedded in a brief.

## Operational limits

- Creation never replaces differing files. Identical reapply preserves work state. Once implementation changes starter files, reapply reports conflicts; v1 is not a synchronizer or migration tool. Continue through context/status, or use a new target for a new brief.
- Creation is atomic per file and restartable, not a whole-directory transaction. It requires hard-link support (exercised on this Windows filesystem). State JSON replacement is atomic and mutations use an exclusive lock. If interrupted, inspect status; diagnose a leftover `.fluid/state.lock` against its recorded process before manually recovering it. No automatic lock stealing or conflict retries.
- Portable relative paths reject traversal, drive/device names, case aliases and links/reparse components. This is a cooperative local tool, not a sandbox against another process racing filesystem changes. Actor labels are declarations, not authentication.
- The v1 schema does not strictly reject all unknown fields. One reviewed limitation: falsey invalid `parent` values are interpreted as absent; supply a valid module ID or omit the field. Hierarchy can be rendered, but arbitrary-scale effectiveness and non-code-domain effectiveness have not been measured.
- `verify` checks identity/freshness. A planned empty project can have intact metadata without delivering any behavior; inspect module states and actual completion evidence. Modified initial source files are historical manifest differences, not automatically failed current deliveries.

Exit codes: 0 success/current metadata, 1 stale or failed verification, 2 invalid input/conflict, 130 cancellation. No network retries, rate limits, credential files, paid dependencies or destructive cleanup commands. [Operational baseline](docs/QOL.md) lists the full applicability assessment and checks.

## Evidence and design

- [Living phased plan](workflow/PLAN.md)
- [Research synthesis](workflow/research/SYNTHESIS.md), [design](docs/DESIGN.md), [starter workflow](starter-kit/START.md)
- [Real runtime check](workflow/research/foundation-runtime-r2.json), [retained initial failure](workflow/research/foundation-runtime.json)
- [Comparison protocol](workflow/comparison/PROTOCOL.md) and [frozen inputs](workflow/comparison/freeze.json)
- [Results and limitations](workflow/comparison/RESULTS.md), [working assisted example](workflow/comparison/runs/foundation/README.md), [working control example](workflow/comparison/runs/control/README.md)

The four supplied research documents remain unchanged. Installed global skills and other projects are untouched. The framework is a usable local foundation; one example cannot establish a universal productivity multiplier.
