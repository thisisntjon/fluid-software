# The jungle-gym hypothesis — synthesis and design consequences

Date: 2026-10-23. Scope: four supplied investigations, local historical records, five research angles, and primary-source verification. This is a research/design result, not a completed causal experiment or an adopted framework.

**Follow-up design refinement:** Jon clarified that the central product is rapid construction of the frame that makes a large project understandable to bounded agents. Two focused investigations now specify [hierarchical context and responsibility](scaffold-scaling.md) and [concrete scaffold outputs](scaffold-construction.md). Design v0.2 and P1 reflect that goal. The prior proposal's small-task continuity check was insufficient on its own; the replacement pilot includes whole-project orientation, independent real components and their assembly. Capacity expansion is assessed separately from time, human effort and monetary savings. These refinements do not change the source-audit conclusions below.

## Verdict

**Refine the hypothesis.** Your experience points to a valuable operating method: make the work concrete, preserve settled decisions in inspectable artifacts, give agents coherent responsibilities, and let completed parts constrain the remaining work. Existing code is especially useful because it combines reusable implementation, interfaces, examples, history, and observable behavior. It is not the only possible scaffold; the first working parts built during a project can provide the same kinds of anchors.

The strongest universal claims do not survive: more agents are not inherently faster; smaller units are not always easier; broken parts do not inevitably converge to correctness; and early testing is not categorically wasted. Whether the method helps depends on boundary quality, reference quality, agent capability, feedback, and assembly capacity. Evidence is sufficient to design and pilot a disciplined method, but insufficient to promise a universal multiplier.

## What changed after investigating the prior investigation

| Prior claim | Finding | Consequence |
|---|---|---|
| ProgramBench shows no current model solves any whole program | True of its original May study; October 22 leaderboard reports 37/200 for its leading model | Date/version benchmark claims; do not design around a permanent incapability |
| MirrorCode versus ProgramBench proves the oracle/scaffold effect | Both supply reference binaries; budgets, scope cues and evaluation differ substantially | Separate structure, reuse, feedback and compute in causal tests |
| CAID produces universal +26.7/+14.3-point gains | Latest paper uses revised numbers, model-specific mean scores, and extra cost | Contracts/worktrees are promising; no universal shipping or speed interpretation |
| Fine-grained writing is proven worse down to words | Hierarchy is supported; no controlled modern depth sweep establishes the optimum | Stop at meaningful units and preserve author/editor judgment |
| Tests must be written by someone other than the builder | Expected-result provenance is the crucial distinction | Keep useful builder checks; protect acceptance from copied assumptions |
| A dedicated serial integrator is always best | Cursor removed one because it bottlenecked work | Require accountability; adapt the integration mechanism to capacity |
| Baldies establishes the cause of the two-day result | Historical records show multiple simultaneous changes and substantial human steering | Treat the case as mechanism evidence and motivation, not controlled attribution |

The detailed audits preserve primary links and denominators: [mechanisms](mechanisms.md), [verification](verification.md), [practice](practices.md), and [local evidence](local-evidence.md). Originals were not rewritten.

## Why the method plausibly works

Five channels must be distinguished. **Reuse** supplies already solved functionality. **Decision reduction** makes architecture and conventions observable rather than repeatedly invented. **Durable state** preserves completed work beyond a conversation. **Feedback** localizes disagreement with real requirements. **Local repair** lets an agent correct one region while retaining useful neighboring work. This decomposition is our synthesis, not a settled neuroscientific account of model reasoning.

Existing source code and an oracle serve different roles. A scaffold explains what exists and how changes connect. An oracle supplies a justified expectation. A known-bad implementation can be structurally useful while being a poor behavioral authority; a binary can reveal behavior while hiding architecture. The kit records which role a reference plays.

The most directly relevant new finding is the October LEGO/CodeFace preprint: it studies packaged reusable components with contracts, dependencies, provenance and carried tests. Its controls suggest much of the benefit can be obtained through ordinary editing supplied with those artifacts. Cost and provenance limitations prevent a speedup claim. This favors useful packaging over a bespoke orchestration platform. [LEGO v1](https://arxiv.org/html/2610.09079v1)

The local early Antigravity build began without supplied source code, according to its historical review. That matters: the useful structure may emerge rapidly during construction and then support repair. The same review records broken user flows despite broad construction; later combined work documents bounded repairs and integration. We did not rerun those products, and the early snapshots are not judgments about the later combined result. [Local case analysis](local-evidence.md)

## Decomposition should reduce dependency, not just size

A capability tree answers why a part exists. A dependency map answers what it needs and which work can run together. Those are different structures. Splitting by folder, file, or sentence does not establish independence.

Use the largest coherent responsibility with a concrete consumer, usable inputs, owned state, understandable neighbors, and observable completion. Split when it creates separable decisions; regroup when the proposed boundary demands constant negotiation. A worker's confidence is not a readiness measure. Where the answer is unknown, assign exploration with a discriminating observation rather than pretend an implementation contract exists.

Commit0 provides a bounded counterexample to “smaller is always better”: module-level filling outperformed pass-statement filling in its particular setup. It does not imply all function-sized tasks are wrong. [Commit0](https://arxiv.org/html/2412.01769v1)

The book analogy survives at the right level. Synopsis, outline, continuity state and meaningful drafting units support coherence. Revision can make every word intentional without preassigning each word. Chapters that share character knowledge or argument development are coupled work; whole-work editing remains necessary. Re3/DOC support structured generation, while LongWriter's parallel variant illustrates coherence costs under its evaluated setup. [Writing evidence and limits](mechanisms.md)

## What testing theater is—and what learning would mean

Testing theater is not defined by the presence of tests. It occurs when checks inherit the candidate's wrong assumptions, cannot discriminate useful behavior, repeat unchanged evidence without a decision, or lock in unstable detail that does not protect a user outcome.

One controlled study reports lower fault detection when tests follow faulty generated code than with independent generation. That supports separating the expected answer from the candidate's reasoning; it does not justify banning tests by author identity. [Error-propagation study](https://arxiv.org/html/2607.05139v1)

Evidence also challenges ritual execution. A repository-repair study found small nonsignificant success differences across execution policies, with substantial cost differences. This is not proof of equivalence and does not transfer automatically to new-system assembly. It supports asking which observation a check supplies. [Execution-policy study](https://arxiv.org/html/2606.26978v1)

The practical schedule is: clarify success and important assumptions first; run cheap, discriminating checks during construction; check each meaningful boundary with real inputs; exercise normal user flows as completed parts connect; apply broader independent acceptance at a meaningful milestone. Avoid broad repeated suites after every minor edit unless project requirements demand them. Keep already required checks intact.

A test result is an observation. During ordinary inference it does not itself train the model. Useful workflow learning requires an evidence-backed change of decision, a durable record of when the correction applies, and later successful reuse. A growing test count is none of those things by itself.

## Best-of-worlds synthesis

Borrow persistent progress and removable scaffolding from Anthropic; bounded planner/worker responsibilities and capacity awareness from Cursor; native ownership/worktrees from Antigravity and existing harnesses; template portability from Spec Kit; semantic contracts and dependency-aware work from CAID/CodeTeam/Co-Coder; and the user's quick standalone-build practice. Their studies and reports have different tasks and resources, so combining the practices is a design proposal, not a newly proven effect. [Source comparison](practices.md)

The resulting core is deliberately small:

1. Define the useful whole and its acceptance basis.
2. Inspect existing artifacts and decide what to reuse, change, or merely reference.
3. Establish just enough shared meaning and ownership for the next buildable units.
4. Build independent units quickly, preserving concrete progress.
5. Assemble completed, dependency-ready parts and use the normal product path.
6. Repair from new evidence, preserve the accepted state, and make the next action recoverable.

Extra agents, deeper plans, custom validators and memory infrastructure are options whose costs must earn their place. The counterdesign is competent: one lead, one current-state entry, one useful increment, and real feedback. The kit must beat that baseline where it asks for more process. [Adversarial investigation](challenge.md)

## Outstanding questions: answered enough to design, or still empirical?

| Question | Current answer | How to resolve the remainder |
|---|---|---|
| Is code itself the cause? | It bundles several useful channels; no clean local isolation | Separate practical reuse from equal-information representation comparisons |
| How deep should decomposition go? | Coherent and handoffable; no universal hours/files/tokens | Observe boundary churn, assembly failure and rework; adjust on actual tasks |
| When should tests happen? | At decision-relevant points; expectation quality and timing are separate | Compare adaptive checking with current practice under the same final acceptance |
| How many agents? | Limited by independent ready work and acceptance capacity | Compare aggregate budgets; record costs, quality and queue delay |
| Will later passes fix everything? | No guarantee; correlated mistakes and bad oracles can persist | Require changed diagnosis/evidence, bounded alternatives and stop criteria |
| Is a new framework necessary? | No demonstrated need; existing local method and native tools overlap | Pilot the manual core; automate only repeated measured friction |
| Does it generalize to books/research? | The core maps conceptually; acceptance differs | Separate real-domain pilots with whole-work judgment |
| Did Baldies/CE prove a multiplier? | No controlled attribution or complete comparable costs | Prospective real work with capable baseline and full cost accounting |

Further literature alone cannot answer the remaining local effect-size questions. The next useful investigation is a real task pilot, not another unbounded search or a large framework build.

## Deliverables and next decision

- [Design](../../docs/DESIGN.md): operating rules, artifacts, recovery, boundaries and domain adaptation.
- [Starter templates](../../starter-kit/START.md): a small draft users can inspect before adoption.
- [Evaluation](../../docs/EVALUATION.md): real useful work first, then comparisons capable of rejecting the theory.
- [Roadmap](../PLAN.md): phased sequence, assumptions, open conditions and current status.

The recommended next phase is rapid frame construction on a real project, followed by independent components, real assembly and fresh-agent continuation. Wider adoption and automation should follow useful outcomes. No framework installation, benchmark campaign, or global workflow replacement occurred in this investigation.
