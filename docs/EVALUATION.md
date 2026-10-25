# Evaluation plan: does the starter kit improve accepted delivery?

Status: proposed, not executed. Prepared 2026-10-23. Pilot projects, resource budgets, comparison thresholds, and repetitions remain **unapproved**. This document authorizes no runs, purchases, deployments, or changes to other projects.

## Decision to make

Determine whether the kit helps produce useful, accepted artifacts with less total effort, without lowering quality or transferring hidden work to reviewers. Separate three questions:

1. Can the kit rapidly create a whole-project frame that lets separate agents build, connect and resume real work?
2. Does it remain useful when several components must connect?
3. Which mechanisms improve outcomes compared with a capable ordinary workflow?

The local Baldies records motivate these questions but cannot answer them: early reviews found differences between green tests, reachable gameplay, fidelity, and persistence; the combined-build report withdraws an earlier overhead claim because effort and token costs were unknown. Those historical snapshots are not current-product verdicts. [Local evidence](../workflow/research/local-evidence.md)

Do not treat a faster draft, more code, more tests, or more completed task cards as the outcome. Freeze a useful capability and its acceptance criteria before beginning. Research and writing require their own acceptance judgments; they cannot inherit software's pass/fail score.

## P1 — Rapid frame, independent parts, and a genuine continuation

Choose a bounded pending outcome within a real project with multiple intended capabilities, an actual consumer, available source material, coherent boundaries, and observable value. Inspect the existing method package and project records first; avoid installing a competing tracker. Capture the starting artifact, requirements, available references, and relevant environment.

Use the [scaffold guide](../starter-kit/SCAFFOLD.md) to establish the whole capability map, actual foundations and work surfaces, public boundaries, local entrypoints and initial ready work. Detail only what the first builders need. Give separate fresh agents scoped views for two genuinely separable real responsibilities. Observe whether they can start without reconstructing the whole; retain missing-context requests and shared-decision mistakes. Connect completed parts through a consequential real boundary and obtain a non-author acceptance decision on the resulting useful artifact. Record failed checks and corrections alongside success. If acceptance depends on unavailable evidence, report the unresolved criterion; do not replace it with invented fixtures or a self-generated score.

Then perform a **cold resume**: a fresh agent/session receives the normal project entry point and saved artifacts, without the previous conversation. Give it the next genuine authorized action. Observe whether it locates the accepted state, relevant evidence, remaining uncertainty, and correct next step without rebuilding completed work. Record extra human explanations and repeated investigation as costs. Successful navigation alone does not establish successful reuse; the resumed agent must apply the saved information to useful work.

P1 closes when the frame supports independent real construction, the assembled useful outcome is accepted, the continuation produces a checked result, and frame/build/check/review/correction effort is visible. Record time to ready independent work separately from time to accepted delivery. It establishes feasibility, not productivity uplift. If any element fails, correct the smallest demonstrated problem and retain the failure record. Do not add automation to compensate for an unclear workflow.

## P2 — A modest project with connected units

Choose a real project containing multiple coherent units and at least one meaningful dependency. Freeze the parent outcome, boundaries, shared-contract owner, integration owner, available real inputs, and acceptance process. Use independent workers only where their changes can proceed without continual shared decisions. A highly coupled section may remain with one builder.

Build the units standalone, then integrate dependency-ready work through the actual consumer path. Distinguish “component checked,” “integrated,” and “accepted.” Measure contract renegotiation, integration backlog, regressions, and human supervision. Preserve the last accepted artifact and record why any repair loop changes direction.

After acceptance, observe one **subsequent genuine requirement change**. Measure how much accepted work survives and the effort to restore acceptance. Do not invent a change to manufacture a favorable maintenance result. If no genuine change arrives, leave maintenance unmeasured and limit conclusions accordingly.

P2 identifies workable boundaries and instrumentation. Contemporaneous observations of ordinary work can provide context, but unmatched tasks are not a causal control. Advance to comparison only when the method is usable, the outcome is measurable, and remaining uncertainty would change an adoption decision.

For larger actual scope, observe a hierarchical configuration: area leads own local decisions and assembly; root retains global constraints and cross-area changes. Track repeated root-level investigation, escalation frequency, affected-module context size and queue delays. These are mechanism diagnostics, not substitutes for acceptance. The working prediction is that growth in local work need not cause comparable growth in the root's active context.

## P3 — Freeze a comparison before spending on it

The owner must select the real task population, legitimate acceptance evidence, quality margin, worthwhile efficiency improvement, resource ceilings, intervention policy, stopping rules, and precision needed for a decision. Unknown values remain blank and unapproved. Use P1/P2 variability to propose repetitions or an adaptive sampling rule; do not invent a universal sample size or calendar deadline.

Use two distinct experiments rather than a single claim about “scaffolding”:

| Experiment | Comparison | What it can establish |
|---|---|---|
| Practical scaffold plus reuse | Capable ordinary workflow versus kit with suitable existing implementation and references | Whether discovery, adaptation, integration, and bookkeeping repay their full cost |
| Representation mechanism | Materialized interfaces/layout versus prose conveying the same decisions, with reusable behavior held constant | Whether inspectable structure helps beyond information and completed functionality |

Also distinguish **capacity expansion** from efficiency: compare accepted real scopes at stated resource ceilings for a capable single-agent workflow and a hierarchical one. A configured baseline failure/timeout alongside successful hierarchical completion supports a capability gain for that setting; report all resources and do not call it infinite speedup. Progressively larger authorized project outcomes may be used as separate cases, preserving their different difficulty and acceptance criteria. Equal-budget comparisons identify different questions from purchasing additional compute to complete otherwise unreachable work; neither is the sole definition of value.

The ordinary workflow may plan, inspect code, and check its work normally; do not weaken it to create a win. In the representation experiment, inventory information and functionality in both arms. Code often supplies executable behavior that prose does not: where equivalence cannot be achieved, document the difference and decline the pure representation claim. [Mechanism analysis](../workflow/research/mechanisms.md)

Keep the independent behavioral oracle, final criteria, genuine input set, model/version, permitted tools, and outside-source access constant across each comparison. Separately compare single-agent and bounded multi-agent execution with the **same aggregate resource ceiling**; concurrency does not multiply the budget. Record actual spend and utilization. A larger-budget swarm arm may be informative, but label it exploratory and do not attribute its gain solely to parallelism. Equal monetary and equal token budgets are different conditions and must not be silently substituted.

If check costs or acceptance escapes remain a material uncertainty, add a **separate conditional checking-policy comparison**: adaptive decision-triggered checks versus the project's current permissible routine, holding final acceptance, real inputs, implementation setting and aggregate resource ceiling constant. Preserve mandatory CI and integrity controls in both arms. Freeze assignment, interventions and stopping rules before running it; compare actionable findings, total checking/repair cost and accepted quality. Do not infer a timing effect from check-event counts alone. Defer this experiment if the pilot exposes no decision-relevant uncertainty about checking.

Use matched real tasks or isolated historical snapshots with independent outcome evidence. Randomize condition and order; block by domain, coupling, and reference availability. Fresh agent sessions cannot erase human carryover: a person who has already solved the same task must not provide solution-informed coaching to a later arm and have the runs counted as independent. Keep evaluator feedback and implementation hints separate; standardize allowed interventions, record deviations, and analyze contaminated runs explicitly. Retain failures, timeouts, and withdrawals.

For writing and research, run **separate strata** using real briefs and source material. Writing acceptance includes whole-work coherence and target-reader/editor judgment; research acceptance includes source validity, contradictory evidence, and the argument's usefulness. Blind comparative judgments where feasible and preserve disagreement. Do not pool chapter ratings and software behavior into one universal score.

## Metrics and event records

Record events in the existing project log, linking full evidence only when needed. Use actual timestamps, artifact versions, input/source versions, actor/session, action, outcome, and cost where available. Unknown cost stays unknown. Separate active human minutes, elapsed time, and monetary spend; concurrent agent durations must not be summed as wall time.

| Metric/event | Measurement | Rule it informs |
|---|---|---|
| Acceptance | Frozen criteria, exact artifact, independent decision, unresolved defects | Quality gate before any speed claim |
| Time to accepted result | Start includes preparation; finish includes review and correction; separately label blocked/queue time | Delivery comparison, not first-draft speed |
| Human effort | Setup, direction, intervention, review, integration, correction minutes | Detect shifted supervision burden |
| Compute/tool cost | All workers, retries, failed runs, preparation, and paid tools | Total economics; no successful-run-only denominator |
| Integration/recovery | Boundary changes, first assembly failures, regressions, rollback and repair effort | Revise decomposition or ownership |
| Cold continuation | Extra context requests, repeated investigation, useful result using saved evidence | Simplify or repair handoff records |
| Frame readiness | Time/effort until real independent responsibilities can start; later missing-boundary requests | Improve the constructor; ready-task counts alone do not prove value |
| Scope and hierarchy | Accepted outcome size/complexity described by real capabilities, root escalations, local decision/assembly load, resources | Detect useful capacity expansion or a relocated context bottleneck |
| Next genuine change | Accepted behavior retained, new defects, time and cost to acceptance | Maintenance benefit remains unproven until observed |
| Check execution | Question, relevant state, result, next decision | Rerun only for a changed relevant state, missing/unreliable evidence, or a named diagnostic reason |

Include timeout and failure costs in cohort totals. Report completion rate alongside time and cost; a timeout is neither a successful fast run nor zero effort. For cost per accepted outcome, include unsuccessful attempts in the numerator; if none are accepted, report no accepted outcomes and total cost rather than a misleading ratio. Compare fixed, meaningful capabilities within a stratum; task-card counts are easy to inflate.

## Stop, adopt, and reopen

**Quality first.** Predeclare an acceptable quality margin and critical-defect rule. Claim efficiency only after meeting the planned noninferiority requirement on accepted quality and regressions. A nonsignificant difference does not establish equivalence. If the available sample cannot resolve the quality question, report uncertainty and withhold the speed claim. [Verification evidence and limits](../workflow/research/verification.md)

**Stop an affected run** at its approved resource ceiling, a material integrity failure, unavailable required evidence, or a blocked dependency that needs an external decision. Preserve the result and incurred cost. Repeated repair without a changed diagnosis or new observation triggers diagnosis, an alternative approach, or re-scoping—not automatic continuation. Any sequential early-stop rule for the comparison itself must be declared before inspecting results.

**Adopt selectively** when predeclared quality conditions hold and either the specified efficiency improvement or the specified capacity expansion is demonstrated within the accepted resource and human-burden limits. Capacity adoption may legitimately cost more compute; its criterion is a larger accepted useful scope, not an implied cost saving. The next genuine-change check must support any maintainability claim; absent that evidence, adoption remains provisional with maintenance unmeasured. Adopt only for the demonstrated task class. P1/P2 may justify limited provisional use; they do not justify a universal multiplier claim. Remove kit artifacts that add burden without informing decisions.

**Adjust or reject** when gains disappear after full costs, integrations accumulate, reviewers carry more work, or a capable lightweight workflow matches outcomes more cheaply. A failed comparison is a failed claim with an actionable correction, not evidence that the kit succeeded by learning.

**Reopen** after a material model/harness change, a new domain or coupling pattern, stale reference behavior, repeated acceptance escapes, or evidence that bookkeeping costs exceed benefit. Preserve old observations with their versions. The next authorized action is to select the P1 real task and approve its concrete scope and resource boundary; no evaluation run has occurred under this plan.
