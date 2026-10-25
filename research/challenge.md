# Adversarial assessment: adoption must be conditional

Date: 2026-10-23. Investigator: `/root/challenge`. Reviewed: `PLAN.md`, `local-evidence.md`, `practices.md`, and `verification.md`. No implementation or experiment was performed. **Verified** below means checked against an available primary source or an explicitly identified local record; it does not mean independently reproduced. **Inference** identifies proposed design consequences.

## Verdict

The strongest version of the hypothesis is not established: existing artifacts, recursive decomposition, and more agents do not jointly guarantee fast, reliable completion. They can also accelerate commitment to the wrong reference, fragment a coupled problem, and overwhelm acceptance capacity. The defensible product is a small decision protocol that sometimes chooses a scaffold and a swarm, and sometimes chooses one investigator or builder.

**Verified locally:** the recorded early Baldies build began without supplied code; initial reviews also found behavior missing despite substantial construction. Later success does not identify which intervention caused the speed. The local method package already exists, so another mandatory orchestration layer has a burden of proof. See [local evidence](local-evidence.md).

## Strongest failure modes and required responses

### 1. A precise reference can be precisely wrong

**Verified:** ESA's Ariane 501 account reports simultaneous inertial-system failure, specification/design errors, and insufficiently representative equipment and system tests. Its inquiry recommendations explicitly require checking implicit assumptions against use restrictions and using realistic inputs in complete system testing. This is an engineering counterexample to treating previously reviewed equipment as valid in a changed context; it is not an estimate of AI-project risk. [ESA account](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report), [recommendations](https://www.esa.int/esapub/bulletin/bullet89/recom89.htm)

**Inference:** a reference is evidence within a use envelope, not a universal oracle. Record its version, relevant operating conditions, intended behavior, known defects, and unresolved conflicts only where consequential. Distinguish “reproduce this behavior” from “improve this behavior.” Where reference and owner intent disagree, resolve the acceptance rule before replicating it across modules. A reference mismatch should invalidate affected assumptions and checks, not trigger endless repairs to imitate the wrong answer.

### 2. Decomposition assumes the answer is stable enough to divide

**Inference:** novel research may not yet have a useful output contract. Whether an approach works, which variable matters, or even how to measure success can be the task itself. Recursive decomposition into implementation cards can conceal that uncertainty under invented precision. The same problem occurs when architecture depends on an unmeasured performance constraint.

**Requirement:** support an exploration unit alongside a build unit. It names a question, competing explanations, real evidence or input, a discriminating observation, a resource limit, and the decision its result changes. A failed hypothesis can complete exploration successfully. Do not recursively split an uncertainty when all children still depend on the same unanswered question. Resolve that question or keep the coupled unit together.

### 3. Local contracts do not establish global behavior

**Inference:** ownership of different files does not make work independent. Modules can share schema meaning, transactions, timing, resource limits, deployment state, or error recovery. Chapters can satisfy an outline while breaking an argument or character arc. Fully specifying these interactions up front may cost as much as solving them.

**Requirement:** name cross-cutting invariants and the owner of their decisions. Before broad parallel construction, establish the smallest useful assembled path that exercises the most consequential seam; do not require an empty architecture for its own sake. Allow contract revision and regrouping. If changes repeatedly cross the same boundary, treat the split as suspect. Standalone demonstrations establish local readiness; they cannot substitute for a consumer using the assembled result.

### 4. More reviewers can amplify the same mistake

**Verified:** the [verification investigation](verification.md) documents code-conditioned expectation errors and evaluator leniency; author separation alone does not make evidence independent. ESA's duplicate-system failure also illustrates why redundancy does not eliminate shared failure causes, without establishing a numerical analogy to agents.

**Inference:** many agents reading the same mistaken report can create apparent consensus without new evidence. Distinct models may still share sources and framing. The lead can remain a common point of failure by selecting every hypothesis and interpreting every result.

**Requirement:** separate critical acceptance expectations from the candidate's rationale where feasible. Preserve conflicting evidence and trace claims to original sources. Use a fresh observation or a materially different hypothesis for consequential challenges. Never count agreement as multiple independent confirmations. If no independent oracle exists, report the uncertainty and use an appropriate empirical or owner judgment; do not manufacture certainty through votes.

### 5. Throughput can move the bottleneck to review

**Verified:** Cursor reports removing a dedicated integrator because it became a bottleneck. This is a vendor experiment, not a universal recommendation against integrators. [Cursor report](https://cursor.com/blog/scaling-agents)

**Inference:** a queue of completed modules can increase elapsed time, stale assumptions, and human attention while agent activity looks productive. Planning and review work may grow faster than useful output.

**Requirement:** choose concurrency from ready independent work and actual assembly capacity. When unaccepted deliveries accumulate or the same decision blocks multiple workers, pause new assignments and resolve that bottleneck. Measure accepted connected outcomes, human minutes, queue delay, compute cost, and repair. No default agent count or arbitrary utilization target is justified. Accountability for assembly need not mean a permanent serial integration agent.

### 6. Subjective quality is not reducible to contract coverage

**Verified:** Doshi and Hauser's short-story experiment reports improved individual evaluations with AI ideas alongside greater similarity between outputs. It concerns human writers receiving ideas, not autonomous book production. It supports treating quality and diversity as separate outcomes. [Author manuscript](https://arxiv.org/abs/2312.00506)

**Inference:** a shared scaffold can preserve continuity while suppressing alternatives. Chapter-level approval cannot establish the whole work's pacing, originality, or force. Rubric optimization can reward technically compliant but uninteresting work.

**Requirement:** distinguish factual checks from taste; define the audience and intended effect; retain a whole-work editorial decision. Use bounded independent alternatives when originality is a material uncertainty, and select before homogenizing them through exchange. Do not claim writing portability from coding results alone.

## Simplest competing design

Use one capable lead, one current-state entry, one next useful increment, actual project inputs, versioned output, and direct acceptance feedback. The entry names the outcome, current artifact, important unknown, evidence, and next action. Reuse existing project conventions. Add helpers only for a separable bottleneck or an uncertainty worth comparing; add task cards only when delegation needs them. A single coherent builder can still use references, focused checks, checkpoints, and occasional independent review.

This baseline retains the likely benefits of context continuity and fast feedback while avoiding mandatory recursion, artifact bureaucracy, and assembly queues. It should receive competent setup and the same legitimate acceptance conditions in evaluation. Comparing the full kit only against an underspecified one-shot prompt would not test whether the kit earns its overhead.

## Assumptions and disconfirmation

- **C1, unverified:** enough stable boundaries exist for parallel work to outweigh contracts and integration. Reopen when repeated cross-boundary changes or assembly delays dominate.
- **C2, conditional:** acceptance can distinguish useful progress from convincing output. Where no adequate oracle exists, limit claims and budget exploration explicitly.
- **C3, unverified:** durable records reduce future effort. Check a real fresh-agent continuation and the next genuine change, including reading/setup cost.
- **C4, unverified:** a portable core helps research and writing. Require a real non-code pilot before claiming cross-domain effectiveness.

The kit loses its case for a project class if it produces no better accepted outcomes while increasing total cost, supervision, or later change cost. A faster first artifact is insufficient. Report failures and abandoned runs. If the full kit appears beneficial, remove one costly component at a time on subsequent comparable real work; otherwise its causal explanation remains bundled. Preserve useful optional practices even when the universal hypothesis fails.
