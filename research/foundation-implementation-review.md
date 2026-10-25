# Foundation implementation review

2026-10-23. Bounded architecture review of the proposed Python 3.11 standard-library CLI. Sources inspected: [design](../../docs/DESIGN.md), [scaffold guide](../../starter-kit/SCAFFOLD.md), [plan](../PLAN.md), and the read-only prior package at `local-agent-guidance`. Implementation is newly authorized by the current user instruction; the inspected plan still describes the earlier design-only stage.

## Verdict

Proceed with a small executable foundation. Host agents make architectural and domain decisions; the CLI validates their declared structure, materializes it safely, renders bounded context, and preserves version-specific results. It needs no embedded model API, scheduler, agent service, or generic plugin registry.

The decisive distinction is observable output: `frame` must create explicit native starter files and operational entrypoints, or identify real existing ones. Generating Markdown around empty directories does not fulfill the design. Native contents come from the host-authored specification; the CLI neither invents implementation nor pretends placeholders work. The demonstration must exercise a real connection built from the resulting frame.

## Minimal data contract

One authoritative project JSON, with a schema version, should contain:

- Project ID, intended outcome, constraints, global semantic decisions, and an existing-state synopsis.
- Modules: stable ID, optional parent, responsibility, native home, exact owned paths or unambiguous owned subtrees, dependencies, named consumer, and next action. Parent links organize capabilities; dependency links govern readiness. They are different graphs.
- Each ready module's contract: inputs/outputs, relevant meaning and failure behavior, delegated decisions, completion observation, and expectation basis. Deferred capabilities can remain shallow and explicitly unready.
- Source references: project-relative path, relevance, authority (`requirement`, `reference`, or `implementation`), and current fingerprint where evidence depends on the source. Preserve material exceptions rather than extracting favorable summaries.
- Explicit initial files with contents, plus references to existing files to adopt. Separate native output from generated context and state paths.

Do not require every possible semantic dimension for every domain. A concise contract can explain units, ordering, mutation, lifetime, or chronology when relevant. Missing source material is an unresolved prerequisite, not a fabricated example. Reject duplicate IDs, missing dependency targets, dependency/parent cycles, conflicting ownership, and invalid paths before writing anything.

## Small implementation boundaries

| Module | Responsibility and public boundary |
|---|---|
| `model` | `load_project(path)` and `validate_project(project, root)` produce normalized records or actionable diagnostics. No writes or command execution. Centralize path normalization and ownership semantics here. |
| `frame` | `plan_frame(project, root)` returns every proposed file action and collision. `apply_frame(plan)` writes only a wholly valid plan; `render_context(project, module_id=None)` produces whole/area/assignment views linking originals. |
| `records` | `snapshot(project, module_id)`, `record_delivery(...)`, `record_acceptance(...)`, and `status(...)` bind evidence to artifact, contract, source, and dependency fingerprints. Preserve earlier records. |
| `cli` | Parse commands, call those boundaries, print concise errors and next actions, return meaningful exit codes. No duplicate business logic. |

The exact Python types can stay ordinary dictionaries/dataclasses. Freeze these cross-module inputs before parallel construction. Keep tests at behavior boundaries rather than creating a framework of abstractions.

## Commands that earn their existence

1. `check PROJECT`: validate the declared graph, readiness, ownership, and paths; report unresolved prerequisites.
2. `frame PROJECT --root TARGET [--dry-run]`: inspect collisions, materialize declared native foundations and context, and save the adopted identity. Default to preserving existing bytes; an identical rerun succeeds without rewriting.
3. `context PROJECT [MODULE]`: show the relevant view, owned artifacts, direct neighboring contracts, source links, and first useful action. Context selection must not prohibit further investigation.
4. `deliver PROJECT MODULE --evidence FILE`: snapshot concrete outputs with the observation, expectation basis, limitations, and next action. The host records actual checks; this command does not turn a claimed pass into verified truth.
5. `accept PROJECT MODULE --delivery ID --evidence FILE`: record the accountable acceptance decision for the still-current delivery. Permit standalone acceptance; integration acceptance additionally identifies the exercised consumer flow and relevant dependency versions.
6. `status PROJECT`: derive current, stale, blocked, and unimplemented states; show accepted versions separately from working bytes. Include a compact continuation view so a fresh agent can resume without transcripts.

## Adoption and evidence pitfalls

Preflight all writes. Reject traversal, absolute/drive/UNC paths, case-insensitive collisions, reserved tool-state paths, and links/junctions that escape or make ownership ambiguous. Recheck before writing. Never silently replace an existing differing file, overwrite project instructions, or move established source homes. Adoption references existing files without claiming they are generated or complete. Managed context may be regenerated only when its previous recorded bytes still match; local customization is a conflict.

Use atomic state replacement and serialize mutations for this first version; do not imply concurrent writers are safe. Preserve failed and superseded evidence. A changed output, contract, prerequisite, or dependency invalidates applicable current acceptance, including downstream consumers. Keep historical acceptance visible. Hashes establish identity, not semantics, execution, permission, or quality.

## Prior-package reuse and completion basis

Reuse `METHOD.md` and `ADOPTION.md` concepts: one authoritative state, persistent scoped authorization, collision-aware adoption, and version-specific evidence. Do not copy `verify.py` wholesale: it recognizes a fixed five-file package, checks immediate symlinks and byte identity, and has no native project graph or semantic freshness model. Its small SHA-256 helper is generic enough to reimplement directly.

Freeze one real example's requested behavior, inputs, and acceptance criteria before both builds. Record setup, construction, review, corrections, interventions, and unknown costs for foundation and ordinary workflows. Demonstrate independent parts, real assembly, and cold continuation. A single paired example establishes working feasibility and exposes overhead; it cannot establish a causal productivity multiplier, especially with shared-agent learning.
