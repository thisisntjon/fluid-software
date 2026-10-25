# Current practice: portable structure before more orchestration

Date: 2026-10-23. Investigator: `/root/practices`. Scope: current primary documentation and research on accelerating multi-agent development. This is an evidence review and design proposal, not an implementation or a measured evaluation of FluidSoftware.

## Finding

The defensible synthesis is a small, portable coordination protocol around durable artifacts. Current products supply much of the machinery already. The kit should explain what work is ready, what may change, what evidence establishes progress, and how another agent resumes. It should not begin by implementing another agent runtime.

The investigated sources support selective parallelism and explicit boundaries. They do not establish that a fixed swarm, permanent integrator, exhaustive initial specification, or a large checklist is the fastest configuration for every project. Three separable outcomes matter: quality, elapsed time, and total cost. A method can improve one while worsening the others.

## What was verified

### 1. Anthropic: persistent progress and removable scaffolding

The November 26, 2025 engineering report describes an initializer, a feature list, incremental implementation, Git history, and a progress record to bridge sessions. It is practitioner evidence about a specific harness, not a controlled estimate of universal productivity. Adopt durable state and explicit unfinished behavior; do not infer that every project needs a 200-item backlog. [Effective harnesses](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)

The March 24, 2026 follow-up is especially relevant to the timing question. It used planner/generator/evaluator roles, then removed context resets and later forced sprint decomposition as stronger models made them unnecessary. Evaluation shifted later for work the model could already handle. The author explicitly used component removal to learn which harness parts mattered. This supports adaptive scaffolding rather than permanently installing every successful intervention. Its application examples do not isolate the causal effect of each role. [Application harness](https://www.anthropic.com/research/harness-design-long-running-apps)

### 2. Cursor: hierarchy helps; a dedicated integrator can hurt

Cursor's January 14, 2026 report says equal-status agents coordinating through a shared file suffered locking and responsibility problems. Planners and workers improved the setup. However, the same report says a dedicated integrator was removed because it introduced a bottleneck. The browser experiment's million lines are output volume, not proof of a production-ready browser or net labor savings. This directly qualifies the inherited implication that all successful systems converge on a permanent serial integration agent. [Cursor experiment](https://cursor.com/blog/scaling-agents)

### 3. Google Antigravity: many desired mechanics are already product features

Current Projects documentation distinguishes direct local execution from new Git worktrees, including a caveat that non-Git folders remain shared. Worktree isolation is therefore not complete environment isolation. [Projects](https://antigravity.google/docs/projects/)

Teamwork documentation describes exclusive file ownership, per-agent scratch areas, structured handoffs, request/plan/progress artifacts, and independent auditors. It also distinguishes development, demo, and benchmark integrity modes. Ordinary development permits reuse; benchmark restrictions should not be copied into every project. These are documented capabilities, not independent evidence that they caused the Baldies outcome. [Teamwork](https://antigravity.google/docs/teamwork)

### 4. Claude Code: teams are one option, with concrete limits

Official guidance recommends independent modules, research, and competing debugging hypotheses as good fits. It cautions against teams for tightly sequential work and overlapping edits. Current limitations include experimental status, lagging task records, and inability to restore in-process teammates through normal session resume. The kit therefore needs artifact-based recovery that does not assume a live teammate still exists. [Agent teams](https://code.claude.com/docs/en/agent-teams)

### 5. GitHub Spec Kit: reuse the template/adaptor layer

The current repository presents structured processes, reusable templates, project overrides, and agent integrations. Its feature-building, bug-fixing, and idea-assessment routes are independent entry points rather than mandatory stages of every task. This is useful packaging precedent. It is not empirical evidence that specification-first beats a capable baseline, and importing its entire machinery would be an untested choice. [Spec Kit](https://github.com/github/spec-kit)

### 6. Dynamic concurrency: a useful option, not a default speed multiplier

The October 7, 2026 preprint compares native concurrency enabled/disabled across three coding agents, 354 tasks and 2,124 executions. Tokens rise 1.41–3.31 times; runtime rises in 14 of 15 agent/benchmark combinations. Some longer workloads benefit, including a maximum 14.3 percentage-point task-pass gain on LoopsBench. The favorable trajectory patterns are complementary work, alternative solutions, and independent validation. Aggregate benefits vary by agent and task. Repeated stochastic runs are limited, so these are configuration-specific results. [Dynamic concurrency v1](https://arxiv.org/html/2610.10263v1)

### 7. CAID: branch/merge structure improves scores, at extra cost

CAID v2, July 8, 2026, combines dependency-aware delegation, isolated worktrees and structured integration. The largest reported mean-score improvements are **25.6 percentage points on PaperBench Code-Dev and 14.7 on Commit0-Lite**, for MiniMax 2.5; they are not universal task completion gains. Sonnet gains are 6.1 and 6.0 points. PaperBench uses an LLM judge and a reduced Code-Dev protocol, not full scientific reproduction. The paper reports consistently higher API cost and no substantial runtime reduction. The inherited 26.7/14.3 figures match earlier material and should be version-labeled or replaced. [CAID v2](https://arxiv.org/html/2603.21489v2)

### 8. CodeTeam: concrete contracts, incomplete end-to-end success

The June 20, 2026 preprint separates architectural alternatives, selection, ownership/interfaces/dependencies, bounded-context implementation and repair. Its 34.6% prompt-engineered and 42.3% fine-tuned results are **average test pass rates** on NL2Repo-Bench, not percentages of complete production projects. Retrieval and allocation ablations mainly support a structural similarity metric, so those improvements should not be relabeled as shipping speed. The useful transferable idea is a buildable contract rather than a vague delegation prompt. [CodeTeam v1](https://arxiv.org/html/2606.22082v1)

### 9. Co-Coder: group by coupling rather than arbitrary file counts

The May 31, 2026 preprint evaluates 28 tasks. Its interface blueprint supports dependency-based grouping and scheduling. Average test pass rates rise from 56.8% to 68.1% on DevEval and 20.1% to 34.1% on CodeProjectEval; reported wall-clock and API-cost benefits are specific to these comparisons. These are percentage-point changes, despite loose percent notation in the prose. The blueprint is inferred from requirements and refined, not an infallible recovered architecture. Adopt cohesion-aware grouping; do not require a graph-partitioning engine before a first useful build. [Co-Coder v1](https://arxiv.org/html/2606.00953v1)

## Adopt, adapt, avoid

This matrix is a proposed design synthesis, not a claim that the combined kit has been tested.

| Practice | Decision for the kit | Limit or cost |
|---|---|---|
| Persistent feature/progress artifacts | Adopt one current state entry and linked evidence | Duplicate trackers become contradictory |
| Planner/worker separation | Adapt when a task exceeds one agent's reliable scope | Planning can become a serial bottleneck |
| Dedicated integration authority | Adopt accountability; make a dedicated agent optional | Cursor and CAID demonstrate different trade-offs |
| Native worktrees/team tools | Reuse through adapters | Shared services, caches and non-Git files remain possible collision points |
| Explicit ownership and contracts | Adopt for parallel writes | Interfaces must remain changeable through an explicit revision |
| Detailed design before all work | Limit to consequential boundaries and the next ready units | False early precision propagates mistakes |
| Multiple independent prototypes | Use only for a named material uncertainty | Competing implementations spend extra budget and require selection |
| Continuous checking of everything | Avoid; run checks tied to changed assumptions or artifacts | Unchanged reruns consume time without new evidence |
| Automatic endless repair | Avoid; require a changed diagnosis or new evidence | Activity can conceal stagnation |
| Custom orchestration platform | Defer | Existing harnesses already provide much of the execution layer |

## Minimal portable protocol

The following recommendations are engineering proposals derived from the combined evidence. Their exact thresholds need real-project calibration.

**Keep a project map and an execution map distinct.** A hierarchy explains how parts contribute to the whole. A dependency graph explains which parts can proceed now. A book can have a chapter hierarchy while its later chapters depend on earlier character decisions; a research report can have parallel evidence streams but one shared claim set. Confusing the hierarchy with the schedule produces false independence.

**Use a small task card.** It needs the useful outcome; owned artifacts; inputs and their versions; public outputs or state transitions; dependencies; relevant examples or source pointers; a completion observation; and a handoff location. Implementation details stay with the builder unless they are shared constraints. A card that cannot name a consumer or meaningful result is probably too small or insufficiently understood.

**Separate readiness from progress.** A proposed task is not ready just because it has a title. Ready means its dependencies and permissions are available, the boundary is understandable, and the builder can observe success. A builder's completion claim means ready for integration or review. Product acceptance requires the actual consumer flow. These distinctions can be represented in existing issues or a Markdown table; a database is unnecessary initially.

**Treat interfaces as versioned agreements.** A worker discovering a bad contract records the mismatch and a proposed revision. The owner identifies affected consumers and refreshes their assumptions before parallel work resumes on that seam. Do not silently adapt opposite sides in separate branches. Freeze enough to start; preserve a cheap route to change.

**Control work in progress by the bottleneck.** Select concurrency from ready, sufficiently independent work and available integration/review capacity. If completed modules accumulate unassembled, reduce new assignments and help integration. If many workers request the same missing information, resolve the shared decision instead of producing more branches. Avoid an invariant rule such as “always use six agents.”

**Make integration responsibility explicit without hard-coding its implementation.** Initially, one lead owns the authoritative assembled state and resolves cross-module decisions. That lead can delegate independent reviews or use an existing merge queue. A single accountable owner does not require every merge to wait for a lengthy serial review. Expand integration capacity only when the observed queue justifies it.

**Prefer completed, dependency-ready increments.** Build a coherent component against agreed boundaries, establish its local behavior, then connect it when its partners are ready. Assemble useful flows frequently enough to expose incompatibility. This avoids both speculative wiring of empty parts and a final big-bang assembly after all contracts have drifted.

**Preserve a checkpoint with a small evidence receipt.** Record the output version, commands or observations used, result, known limits and next action. Associate a check with the artifact it actually examined. After an unrelated change, do not automatically rerun every expensive check; after a changed dependency, do not reuse a stale pass. The kit can express this manually before automation is justified.

**Recover from artifacts, not presumed conversation memory.** A new worker reads the state entry, relevant card, actual output and latest failure evidence. It verifies that its base version and ownership are current. If the previous session disappeared, it resumes the incomplete unit or returns it for reassignment. Neither a transcript replay nor blind trust in a stale “done” label is sufficient.

**Record learning as a changed operating decision.** Preserve what was tried, what observation changed the diagnosis, the action that followed, and conditions under which the lesson should be reopened. A test count or an agent's favorable review is not a reusable lesson. This connects work to future performance without requiring an elaborate memory system on day one.

## Harness adapters, not harness dependencies

| Surface | Optional adapter behavior | Portable fallback |
|---|---|---|
| Antigravity | Map task cards to project artifacts and native subagents/worktrees | Cards, explicit ownership and manual delivery |
| Claude Code | Map to task list/subagents or teams only when communication is useful | One session per card, durable handoffs |
| Cursor | Use native planner/worker execution and inspect output evidence | Any agent reads the same task contracts |
| GitHub Spec Kit | Reuse templates, overrides and agent integration when they fit | Plain files and existing project conventions |
| Git-based project | Use isolated branches/worktrees and existing CI/merge mechanisms | Separate artifact copies with a named assembler |
| Writing/research | Shared outline/claim register, source inventory, owned sections and editorial assembly | Human-managed files with version history |

No adapter should become the sole owner of essential project state. Switching tools should preserve outcomes, boundaries, ownership, evidence and unfinished work.

## Outstanding questions and assumption candidates

1. **Artifact benefit versus better specification remains unresolved.** These workflow sources bundle decomposition, state, feedback and extra compute. None isolates the exact scaffold-versus-equivalent-prose hypothesis. Compare them separately in the proposed evaluation.
2. **The right integration policy is contextual.** CAID supports centralized coordination; Cursor reports removing a bottlenecking integrator. Start with explicit accountability, measure queue delay and repair, and change the mechanism when evidence warrants it.
3. **Boundary quality is load-bearing.** The kit assumes a lead can identify coherent responsibilities. Failed or changing interfaces should trigger regrouping, not just more retries.
4. **Portability beyond software is a design hypothesis.** The mechanisms appear transferable, but the sources reviewed here chiefly evaluate code. A real writing or research pilot must establish whether cards and assembly preserve global coherence and reduce total effort.
5. **Scaffolding can become stale.** The method should include removal trials after model/tool changes, comparing accepted outcomes and total cost. A once-useful ceremony is not automatically permanent.
6. **Tool documentation establishes capability, not local adoption.** No source proves the installed local versions expose every current feature, nor that those features were used in the reported Baldies build. Inspect the chosen harness during implementation.

## Source ledger

All links above were opened on 2026-10-23. No remote software was installed or executed.

| Source | Evidence type/version | Use and boundary |
|---|---|---|
| Anthropic effective harnesses | Vendor engineering report, 2025-11-26 | Persistent state; no universal effect estimate |
| Anthropic application harness | Vendor experiment, 2026-03-24 | Adaptive removal of scaffolding; examples are not controlled factorial trials |
| Cursor scaling agents | Vendor experiment, 2026-01-14 | Coordination failures and integrator counterexample |
| Antigravity Projects / Teamwork | Current official documentation | Available mechanisms; not measured causal outcomes |
| Claude Code agent teams | Current official documentation | Fit, overhead and recovery limitations |
| GitHub Spec Kit | Current official repository README | Reusable process packaging; no comparative productivity proof |
| Dynamic concurrency | arXiv:2610.10263v1, 2026-10-07 | Native concurrency comparison; configurations and stochastic limits matter |
| CAID | arXiv:2603.21489v2, 2026-07-08 | Version-corrected scores; Code-Dev and partial test metrics |
| CodeTeam | arXiv:2606.22082v1, 2026-06-20 | Contract architecture; average test pass rather than finished products |
| Co-Coder | arXiv:2606.00953v1, 2026-05-31 | 28-task coupling-aware comparison; no universal speed claim |

## Handoff

Design around durable artifacts, coherent work units and controlled assembly. Keep extra agents, strict review cadence, exhaustive plans and runtime automation optional until a real project demonstrates their value. The immediate useful next step is a minimal manual kit with an explicit real-project pilot and a capable baseline, not installation of another large framework.
