# Operational baseline

Standard local CLI, Python 3.11 stdlib, no network or long-running service. User authorized implementation; these reversible safeguards are within that scope. Implement before claiming working foundation.

| # | Feature | Verdict | Rationale |
|---|---|---|---|
|1|Errors|Implement|Actionable validation/conflict/stale-state errors and exit codes|
|2|Preflight|Implement|Validate complete brief, paths and collisions before apply|
|3|Structured logging|Implement|JSON command results and state events; no daemon logger needed|
|4|Status|Implement|Ready/active/delivered/accepted/stale and next action|
|5|Cancellation|Implement|Atomic files, lock finally cleanup, clear Ctrl+C|
|6|Timeouts|Not applicable|No remote or subprocess execution|
|7|Retries|Not applicable|Local ownership conflicts must be diagnosed, not blindly retried|
|8|Config|Implement|Explicit portable brief and target; no credentials/env layering needed|
|9|Preview|Implement|Frame defaults read-only; --apply explicitly materializes|
|10|Idempotency|Implement|Identical creation skipped; changed existing files refused|
|11|Machine output|Implement|--json with clean stdout|
|12|Sample|Document|Use actual bounded example brief; no fabricated sample evidence|
|13|Progress|Not applicable|Short local commands return counts and elapsed time|
|14|Checkpoint|Implement|Atomic versioned project state and hash-bound receipts|
|15|Resume|Implement|Context/status expose accepted state and remaining real work|
|16|Rate limits|Not applicable|No external API|
|17|Batching|Not applicable|Small project briefs; no bulk crawler|
|18|ETA|Not applicable|No credible long-job ETA; actual elapsed only|
|19|Audit|Implement|State events record actor/action/reason/time and output/evidence hashes|
|20|Fallback|Document|Missing inputs remain errors; ordinary project files remain usable without CLI|
|21|Profiling|Document|Standard Python profiler available if observed performance warrants it|
|22|Parallelism|Document|Agents own separate outputs; brief distinguishes build and semantic dependencies; state writes locked|

New dependencies: none. Normal usage, preview, real example, continuation and output guidance will be in README once commands are exercised. No remote retry/rate-limit handling or destructive operations are introduced. No changes to installed global skills.

## Observed implementation result

Phase I implemented the applicable rows above. The actual portable package at `workspaces/foundation-v1` runs offline with Python 3.11 and no dependencies. Zero-write preview, actual materialization, repeat application preserving state, idempotent claims, scoped continuation, dependency staleness, renewal, distinct recorded review and final verification were observed. Lock contention and another actor's active claim failed clearly without changing state. Initial Windows output encoding failed once, was corrected to UTF-8, and the failed command record is preserved.

Final phase-I evidence: `workspaces/foundation-v1/evidence/foundation-final-verify.json`: four accepted modules, zero stale, no brief integrity issues. This validates the exercised local workflow; source review covers remaining path/graph branches without claiming exhaustive race or malformed-input testing.

README documents normal execution, read-only preview, the actual portable sample (no fabricated sample mode), resume through status/context, JSON output and state-event audit trail. No install/config secrets are introduced. There are no network retries or rate limits; exclusive state updates and disjoint file ownership support cooperative parallel agents. Whole-project atomicity, schema migrations and hostile-process isolation are outside v1. The reviewed falsey-parent validation limitation is documented. Every option's semantics are in help/README; actual lifecycle commands are in the evidence logs, not manufactured examples of results.
