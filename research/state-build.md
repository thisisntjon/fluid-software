# State implementation record

2026-10-23. Implements the frozen foundation contract in `fluid/state.py`.

- Delivery records every current regular file under ownership roots, excluding cache files/directories and tool/Git state. Added, deleted and changed owned files are detected by comparing complete path/hash maps.
- Delivery records direct semantic dependencies' current file maps and delivery evidence. Staleness also propagates through semantic dependency chains. `build_after` only gates claim/readiness; it does not silently become a semantic edge.
- Evidence must be an actual target-relative regular file outside `.fluid`. Acceptance requires a different declared actor and a written observation. Actor strings do not authenticate identity, and checksums do not prove behavior.
- Exclusive state locks carry process ID, timestamp and creator token. Busy locks fail immediately; only the creating operation removes its lock. State JSON writes are atomic through the shared model helper.
- Events store before/after receipt snapshots. Invalidation clears live receipts, preserves history, propagates across both graphs, and rejects another actor's active work before changing anything.
- Manifest differences describe starter history. Brief identity mismatches fail verification; modified/removed starter files are not automatically treated as corruption of later accepted implementations.

## Actual checks

- Parsed and imported `fluid/state.py` under Python 3.11 with `-B`; import did not create project state.
- Inspected `foundation.project.json`; all seven pinned copy sources matched the actual source files. State source SHA-256: `b040c97a76deec75a35b3b3500bbbf0eee3be875179063765c9160b5f416674f`.
- Read-only frame preview against the real `workspaces/foundation` materialization (run `cc667f26-c3b2-4d05-8172-3b509eb89e84`) found fourteen identical files, preserved runtime state, and reported no conflicts.
- Ran the portable CLI from inside the materialized project, `fluid.py --json status .` (run `bcd78245-35d6-4cd0-a4c4-e81d0abc795d`). All four modules were honestly reported planned and ready, with actual file paths/hashes, unfinished outputs, zero events, and no delivery or acceptance claims.
- Called `verify(workspaces/foundation)` from the original implementation: `ok=true`, no integrity issues, and every manifest path unchanged.
- One invocation could not resolve bare `python`; the installed absolute Python 3.11 executable succeeded. This is a shell PATH observation, not a product failure.

Lifecycle mutations and adversarial stale-content checks remain with the coordinator to avoid overlapping writes to the same real project. No fabricated state or pretend behavioral evidence was introduced by this builder.

## Authorized final lifecycle on foundation-v1

The coordinator subsequently assigned the corrected portable target `workspaces/foundation-v1` for final lifecycle recording. The earlier `workspaces/foundation` was retained with its observed UTF-8 context-output failure; CLI output was corrected before v1 framing.

- Claimed and delivered `state` as `state-builder` using the actual copied implementation/check evidence at `evidence/state-build.md`. Delivery: `a3005b67-c667-4547-8b1a-eef11bdf66d1`; evidence SHA-256 `e00e2c948e6168355b2198fae694e76e0b0224de4409fa33470671d9fae2c57c`. State was fresh; CLI correctly became stale because its older semantic dependency fingerprint lacked this delivery evidence.
- Independently reviewed root's model and CLI source plus all eight real runtime command records. The real project validated; actual root path checks rejected traversal, absolute paths, reserved devices, stream syntax and case aliases. No source was changed.
- Accepted only `model` as distinct actor `state-reviewer`, supported by `evidence/state-review.md`. Acceptance: `24abd5aa-714c-4699-b85c-cabb43bf9df1`; evidence SHA-256 `8c0c94e85d6aa0843bbdcc3f5e3f75350f0f277370439fcaa0064c82513f77d5`. Model was accepted and fresh. Link/junction races and exhaustive malformed-schema coverage remain unproved, explicitly recorded in evidence.
- State acceptance is left to the independent frame reviewer. CLI renewal/acceptance remains with the coordinator after provider delivery. At the observation, frame was active, state delivered/fresh, and CLI delivered/stale.
