# Working foundation and the first with/without build

2026-10-23. **The foundation is working, and both fresh builders delivered independently accepted Research Navigators.** Both unchanged first deliveries satisfy the shared acceptance criteria after transparent evaluator adjudication and manual review. The comparison is one descriptive example, not a causal estimate of a universal multiplier.

## What exists

The [local CLI](../../fluid.py) validates agent-authored briefs, previews and materializes real native files, renders whole-project and scoped module context, tracks ownership/readiness, and binds delivery/review to current output and evidence bytes. It runs with Python 3.11 standard library and no installation, network, model backend or agent scheduler. The host agent supplies architectural judgment and literal native artifacts; the existing harness supplies workers.

The foundation was built by separate model/CLI, frame and state responsibilities and assembled into a [portable real copy](../../workspaces/foundation-v1/FRAME.md). Four modules received distinct recorded review and acceptance; [final verification](../../workspaces/foundation-v1/evidence/foundation-final-verify.json) reports zero stale receipts and no integrity issues. Actual checks covered preview without writes, materialization, scoped context, repeat application preserving active work, ownership/lock rejection, consumer staleness and renewed delivery. An initial Windows output-encoding failure was preserved and fixed. Path-race and every malformed-input case were not exhaustively exercised; operational limits are in the [README](../../README.md).

The two examples are independently usable offline products:

- [Foundation-assisted navigator](runs/foundation/README.md), [entry point](runs/foundation/navigator.py).
- [Ordinary-workflow navigator](runs/control/README.md), [entry point](runs/control/navigator.py).

Both ingest the four actual supplied Markdown/text/Word documents, retrieve complete passages with source hashes and native locations, include Word tables, export source-linked evidence, identify changed/missing sources, preserve old indexed text, and protect a previous usable index when a rebuild fails. Their passage counts and internal structures differ; those are not quality scores.

## Matched setup and observed time

The [brief](TASK_BRIEF.md), [protocol](PROTOCOL.md), independent [source expectations](SOURCE_EXPECTATIONS.json), evaluator, initial treatment frame and prompts were [frozen](freeze.json) before dispatch. Each arm received byte-identical documents and requirements, one fresh builder, the same inherited native-agent settings/tools, a bounded initial cap, no child builders and one potential bounded repair opportunity. The control could create its own plans, contracts and scaffolds. No task hints or repair feedback were sent to either builder.

| Measure | With foundation | Ordinary workflow |
| --- | --- | --- |
| Builder started, UTC | 2026-10-23 | 2026-10-23 |
| First delivery, UTC | 2026-10-23 | 2026-10-23 |
| Recorded builder elapsed | Same-day single-pass delivery (2026-10-23) | Same-day single-pass delivery (2026-10-23) |
| Final shared acceptance | All 13 protocol rows satisfied | All 13 protocol rows satisfied |
| Builder source repair after independent evaluation | None | None |
| New dependencies/model services | None | None |
| Original input bytes | Unchanged | Unchanged |
| Durable module state | Four delivered, later independently accepted | Builder log and delivery record; no imposed Fluid state |

These are actual recorded delivery-clock intervals, not matched token budgets or active-compute measurements. The assisted interval was about a small single-run interval shorter in this run. Do not turn that into a total productivity ratio: target-specific contract/frame authoring was performed before its builder started and was not separately timed. The [setup execution](setup.json) took about 0.825 seconds, including copies, with about 0.696 seconds for brief serialization plus frame preview/application; these numbers exclude authoring deliberation. Reusable foundation development, shared brief/oracle preparation, and root coordination also lack complete active-time accounting. Tokens, comparable full tool-call counts and dollar costs are unavailable.

Review also cost time. The original automated foundation evaluation ran 2026-10-23–2026-10-23; control ran 2026-10-23–2026-10-23. Manual review intervals were 2026-10-23–2026-10-23 (recorded on 2026-10-23) for foundation and 2026-10-23–2026-10-23 (recorded on 2026-10-23) for control. Their last required verifications completed at 2026-10-23 and 2026-10-23 respectively; later reporting and bookkeeping add overhead. Supplemental check execution took about 2.0 seconds for foundation and 1.0 second for control, excluding diagnosis/reviewer deliberation. Review tasks overlapped and the arm checks exercised different interrupted obligations, so adding those intervals is not an estimate of total labor. Detailed timestamps remain in the evidence. Both builds shared one machine, and foundation evaluation began while control was still building; resource contention is a possible confound. Filesystem separation was instruction-based, not an OS sandbox.

## First-pass failures and their resolution

Both immutable original evaluator reports contain **11 passing rows, one failing row and one manual-review blocker**. Those records were not rewritten:

- [Foundation original](foundation-first.json): freshness stopped at a raw full-text export comparison. The actual report contained the exact complete passage bytes, including three CRLF pairs. The evaluator's text read converted CRLF to LF before comparing against unconverted passage text. [Supplemental review](FOUNDATION-FIRST-ADJUDICATION.md) verified the original bytes, then reran the entire interrupted freshness sequence on an unchanged snapshot: changed/missing search, show and export, explicit status labels, restoration, and refreshed text/hash after re-indexing. No product change was needed.
- [Control original](control-first.json): heading validation rejected a returned parent heading from the source's displayed equation. The oracle recognized only ATX headings. A primary CommonMark reference and installed reference parser recognized the same setext heading in the original document. The brief specified no math-aware Markdown dialect. [Supplemental review](CONTROL-FIRST-ADJUDICATION.md) preserved the failure, independently verified the heading chain and native source, and executed the interrupted search/show/navigation obligations on unchanged code. A different math-aware presentation could be a future preference, but was not retroactively imposed as a failed requirement.

The [prospective evaluator review](EVALUATOR-REVIEW.md) established symmetric, append-only adjudication before either product was inspected. Neither arm received a product repair, hidden restart or relaxed functional requirement. Independent delivery review inspects generic parsing, source fidelity, README commands, limitations and historical claims; a green CLI exit alone does not close that row.

The [foundation manual review](FOUNDATION-DELIVERY-REVIEW.md) and [control manual review](CONTROL-DELIVERY-REVIEW.md) both passed. Historical builder logs remain authored records, not complete independent tool telemetry. The control retained its initial verification failure and command list, but reused some numbered stdout files in a later successful check; that limitation is preserved in the review. Neither review claims that a GUI viewer was opened or that the retrieved research assertions are true. The foundation example now also has [four independently accepted module records](foundation-acceptance.json), all fresh; acceptance changed workflow state and added review evidence, not product source.

## What this teaches the kit

1. **The structure is usable.** A fresh assisted builder read the persisted whole, scoped contracts and actual documents, completed the product and delivered providers before consumers without root task hints. Its log says the frame clarified ownership and return-value agreements, while parsing algorithms and granularity still required judgment. Repeated context output was an observed cost. This supports feasibility and continuation, not unlimited scale.
2. **An ordinary agent remains a strong baseline.** It also chose coherent responsibilities, planned and checked real behavior. The benefit is not established by counting files, tests or module cards. One pair cannot separate useful interface decisions, representation, extra preparation, random variation or model behavior.
3. **Checks need an accountable source of truth.** Here the two independent red results came from the evaluator. Fixing product code merely to turn them green would have taught the wrong lesson. The starter workflow now explicitly compares a failed expectation against original sources/requirements before requesting repairs and preserves evidence of any evaluator correction.
4. **Keep the core small and adapt effort.** Native interfaces, bounded context and durable handoffs are useful defaults for substantial projects. The extensive comparison apparatus is research overhead, not a requirement for every project. A tiny change should use the existing project's simpler workflow.

Recommended next experiment, outside this completed local scope: repeat on a larger genuine project with multiple independently owned subsystems, multiple builders, and a later real change. Time frame authoring and review from the beginning, record root interventions and aggregate resources, and compare accepted connected capabilities. That would address department-style scaling and maintenance; this one-builder-per-arm example does not test a swarm multiplier or non-code domain transfer.
