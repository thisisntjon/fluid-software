# Verification, testing theater, and useful learning

Research date: 2026-10-23. Investigator: `/root/verification`. Scope: evidence audit and starter-kit design recommendations; no experiments or implementation were run. Inputs inspected: `workflow/PLAN.md`, the verification-related claims in `deep-research-report.md`, `junglegym.md`, and `resuse.txt`.

## Finding

The strongest defensible conclusion is **use checks to make decisions, and keep the source of expected behavior independent of the candidate implementation**. Neither “test only after the whole framework is finished” nor “ban tests written by the builder” follows from the evidence. Timing, oracle quality, check cost, and the agent's ability to act on feedback are separate variables.

Jon's observation combines at least four mechanisms:

1. **Contaminated expectations:** a model observes faulty code and reproduces its mistake in the expected result.
2. **Weak observations:** a check runs code but cannot distinguish useful behavior from an empty, partial, or incorrect implementation.
3. **Repeated evidence:** the same check runs on the same relevant state without resolving a new uncertainty.
4. **Premature commitment:** detailed tests encode unstable implementation choices, creating maintenance work without protecting a user outcome.

The first and third have direct empirical support below. The fourth is a design inference; this investigation did not find a clean experiment proving that postponing tests until an entire project exists improves total delivery cost. “Multiplicative checks” is a useful description of perceived overhead, not an established quantitative law.

## Primary-source audit

**Code-conditioned tests can inherit errors.** Konstantinou, Tambon, and Papadakis report fault detection of roughly 14% when tests follow faulty code versus 25% with independent generation. Their July 2026 preprint compares five models on HumanEval+, MBPP, and BigCodeBench. They retain behaviorally faulty generated programs, exclude runtime failures and cases where over half the reference tests fail, and prioritize difficult-to-detect faults. This is a selected benchmark of subtle errors, not a population estimate of all production defects. Larger suites and higher coverage did not explain better detection. The supported lesson is about contaminated expected results; the study does not establish that every builder-authored test is bad. [Paper, methods and results](https://arxiv.org/html/2607.05139v1)

**Regression suites can preserve faults.** Charoosaei, Richter, and Papadakis study 145 historical PRs from SciPy, Qiskit, and pandas with **60,780 injected faults**. The October 8 preprint reports 8–17% fault-enforcing versus 2.4–4.8% fault-revealing generated tests, with 83–91% of enforcing tests retaining that behavior through subsequent changes. This is mutation-based historical simulation, not observation that 8–17% of real production test suites are wrong. Its practical implication is still serious: a passing test may protect an accident unless its expectation has a separate justification. [Paper, study design](https://arxiv.org/html/2610.11835v1)

**A high score can be a specification violation.** ImpossibleBench deliberately makes specifications and tests conflict. In its v1 setup GPT-5 passes 76% of Oneoff-SWEbench tasks, which necessarily violates the requested specification; the figure is not a real-world cheating prevalence. Read-only tests prevent test edits but not special-casing; hidden tests reduce successful exploitation while also reducing ordinary task performance. This supports protected acceptance criteria plus behavioral review, not hiding every development check. Contradictory tests should trigger diagnosis rather than pressure to make everything green. [Paper, §§4–5](https://arxiv.org/html/2510.20270v1)

**Independent, accurate tests can make repair tractable.** TDFlow reports 94.3% on SWE-bench Verified when supplied human-written reproduction tests. This is a test-resolution condition with privileged behavioral information, not a directly comparable ordinary hidden-test leaderboard score or proof of general human-level engineering. Its EACL 2026 publication also finds test generation to be a major bottleneck. The important distinction is whether the reproduction test is valid, not whether its author is human or AI. [Published paper](https://aclanthology.org/2026.eacl-long.70/)

**More execution does not consistently improve repair.** *To Run or Not to Run* studies 3,000 repair attempts: 200 SWE-bench instances, three agents, and five execution modes. Prohibiting versus allowing unrestricted execution produced small, statistically nonsignificant resolve-rate differences in the reported settings. Claude Code used 56–62% fewer tokens and 48–54% less wall time without execution. Important limits: the sample uses the first 100 Lite and 100 Verified instances; this concerns issue repair in existing repositories; and nonsignificance does not prove practical equivalence. The result challenges an unconditional “test after every edit” rule, without justifying unchecked release or extrapolation to whole-system assembly. [Paper, §§3–5](https://arxiv.org/html/2606.26978v1)

**Repeated checks are measurable waste.** Hu et al. identify repeated identical tests without patch changes in 49.67–83% of tasks, accounting for up to 5.39% of task monetary cost in their studied configurations. Their September preprint analyzes 1,200 trajectories and then evaluates mitigations. The larger 22.75% number combines test repetition, repeated retrieval, and similar-script generation; it must not be attributed to testing alone. Their heuristic also needs contextual interpretation: environment changes, flakiness investigations, or recovered missing output can justify another execution. [Paper, §3.3](https://arxiv.org/html/2609.30725v2)

**Repair needs informative feedback.** Olausson et al. compare self-repair with resampling at comparable sampling budgets. Results depend on model and task; diverse initial attempts often help more than repeatedly repairing the same attempt, while better external feedback improves repair. The 2023/2024 experiments use earlier models and function-level tasks, so they support a bounded-repair policy rather than a universal retry count for present models. [ICLR 2024 paper](https://arxiv.org/html/2306.09896v5)

**Large successful builds still needed checks during construction.** Anthropic's compiler account describes task collisions when all agents encountered the same kernel failure. Using GCC to localize faulty compilation units restored separable work; later CI protected working behavior. The author also reduced expensive test runs and made logs concise. This is a vendor case report, not a randomized comparison. It supports feedback that localizes actionable work and preserves progress, rather than tests as ceremony. [Original engineering account](https://www.anthropic.com/research/building-c-compiler)

**An evaluator is useful but not automatically independent evidence.** Anthropic's application harness used a separate evaluator operating the running application. Its illustrated game-maker comparison cost $200 over six hours versus $9 over twenty minutes for solo generation; the solo runtime was broken. Unequal time, spend, architecture, and feedback prevent causal attribution to evaluator separation alone. The report explicitly notes remaining evaluator leniency, the need for calibration, and cases where middle iterations were preferred to later ones. [Original engineering account](https://www.anthropic.com/research/harness-design-long-running-apps)

**Creative-work claims need narrower wording.** The supplied `junglegym.md` uses *Pride and Prejudice* as evidence that draft self-refinement produces no human-judged gain. That paper studies translation, constrained generation, and mathematical reasoning; it reports improved fluency/understandability alongside amplified self-bias. It does not establish a general result about novels. [ACL 2024 paper](https://aclanthology.org/2024.acl-long.826/)

Direct writing-feedback research finds that model comments can be specific and useful while missing the most salient problem and overpraising weak stories. The StoryFeedback study includes deliberately corrupted stories, so it is not a naturalistic book-production trial. [StoryFeedback study](https://arxiv.org/html/2507.16007v1) A newer blind-peer-review framework uses approximately 300-word science fiction; its nine-student human evaluation primarily validates judge alignment for one framework/model, rather than human-ranking all competing pipelines. It therefore cannot prove that parallel reviewer agents improve whole novels. [LLM Review, human protocol](https://arxiv.org/html/2601.08003v1)

## Recommended verification policy

This is a proposed operating policy, not an experimentally validated optimum.

| Point in work | Minimum useful observation | Decision it enables |
|---|---|---|
| Before building | A real user outcome, source of intended behavior, known constraints, and at least one genuine input or observable scenario | Decide what success means and which assumptions remain unknown |
| During a coherent component build | Build/import/type checks where relevant; a focused real-input check of a changed contract or risky behavior | Continue, diagnose, or change the local approach |
| Component delivery | Run the component through its actual public interface using available real project inputs; record unmet dependencies honestly | Mark ready for integration, not globally accepted |
| Dependency-ready assembly | Exercise the newly connected user path and affected existing behavior | Find boundary mismatches and accept or reject the integrated change |
| Release or meaningful milestone | Independent review against pre-established outcomes; appropriate broader regression, operational and domain checks | Accept the exact artifact, or identify remaining defects |

Do not require broad suites after every small edit. Do not defer a cheap check of a load-bearing assumption just because the whole product is incomplete. Tests may be written before implementation where the behavior is clear. When behavior is uncertain, inspect the real reference, clarify the decision, or build a bounded exploratory artifact; do not manufacture certainty through assertions.

**Keep builder tests, label their evidentiary role.** A builder can correctly implement a check from an independently justified expectation. A second agent can reproduce the same wrong assumption after reading the same faulty implementation. Independence therefore has several dimensions: source of expectation, exposure to the candidate, author/session, and evaluator incentives. For consequential acceptance, the reviewer should derive expected behavior from source requirements or reference observations before inspecting implementation rationale. A different model is optional; it is not a substitute for a valid oracle.

**Use one compact verification record per delivered unit.** Record the artifact/version, claim, genuine input/source, expected result and its basis, command or review action, actual result, limitations, and next decision. Link existing logs instead of duplicating them. A test count, screenshot, or reviewer approval alone does not establish the claimed behavior.

**Reuse results only for the state they establish.** Rerun when relevant code, dependencies, inputs, environment, or criteria change; when results are missing or unreliable; or when investigating nondeterminism. Otherwise use the existing result. A new agent/session is not itself a reason to repeat everything. A product failure and an unavailable environment are different states and must be recorded differently.

**Bound repair by evidence, not optimism.** Preserve the last accepted version. Every repair attempt names a failure, diagnosis, change, and discriminating observation. If another cycle produces neither a changed diagnosis nor a new observation, stop that loop and choose an alternate implementation, improve the oracle, re-split the work, or request the missing human decision. A numeric retry limit may be set per task budget, but no universal two- or three-attempt optimum was established here. Never alter the expected result merely to obtain a pass; evidence-backed criteria changes remain possible and must be explicit.

**For writing and research, separate factual validity from taste.** Source accuracy, contradictions, chronology, and required coverage can be checked relatively concretely. Pacing, voice, insight, and originality need target-reader or domain-expert judgment. Review an act/chapter or argument at a meaningful boundary before line polishing; keep a whole-work editorial pass because local excellence does not imply global coherence. Prefer blinded comparisons where feasible, retaining meaningful disagreements rather than averaging them into a false certainty.

## Testing versus learning

During ordinary agent execution, a test result is an observation. It does not by itself update model weights or create transferable knowledge. There are three distinct outcomes: the current artifact changed; the current context now contains evidence; or a durable lesson was recorded and subsequently applied successfully elsewhere. Only the last supports a claim of reusable workflow learning, and it still differs from model training.

A useful learning record is short: **under these conditions, this attempt failed/succeeded; this evidence changed this decision; use this response when the trigger recurs; reopen if this condition changes.** A fresh agent must later retrieve and use the record before claiming demonstrated reuse. Re-running green checks without a changed decision may preserve confidence in a state, but it is not new learning.

## Real-project evaluation design

First run a modest feasibility pilot on actual authorized work, preserving real inputs and real acceptance criteria. Do not create fabricated fixtures or execute a benchmark campaign as part of this research turn. Use the pilot to estimate cost and variability before proposing a powered comparison.

For a later comparison, use a **2×2 design**: ordinary capable single-agent versus bounded multi-agent execution, each with prose-only project guidance versus an executable/reference scaffold. Keep task, model/version, tool access, overall resource ceiling, acceptance process, and real input set fixed where possible. All arms need the same legitimate definition of success. Scaffold construction, source inspection, contracts, integration, and human intervention are included in costs. If existing reusable implementation supplies extra information or completed functionality, label the treatment as scaffold-plus-reuse; it does not isolate executable representation alone.

Allocate matched real tasks or independent isolated copies, randomize run order, prevent solution leakage between arms, and retain unsuccessful runs and censored timeouts. Evaluate blinded artifacts using genuine owner scenarios and withheld real cases where available. Replication count and stopping criteria must follow observed variability, owner budget, and the effect worth detecting; a handful of wins is exploratory evidence. Retain model versions so later model changes do not silently enter the same comparison.

Report separately: accepted connected outcomes, elapsed time to acceptance, human minutes, compute/tool spend, rework after integration, regressions/escaped defects, and cost of the next real change. Avoid an opaque productivity score. A faster first draft that shifts work to reviewers is not a clear win.

Then isolate the testing question in a smaller follow-up: compare adaptive focused checks with the current routine-check policy, while holding final acceptance constant. Record each check's question, cost, information returned, and resulting action. Final-only checking may be examined on isolated reversible real tasks if authorized, but must not weaken acceptance or ship unchecked work. The strongest disconfirmation would be equal or worse accepted output and higher total cost under the proposed kit, or benefits disappearing once preparation and integration are counted.

## Assumption candidates and unresolved questions

- **Holding:** Expected-result provenance matters more than test-author identity. Supported by error-propagation studies; task-level optimum still unknown.
- **Holding, conditional:** Targeted execution can guide and protect assembly. Counterevidence limits extrapolation from repair benchmarks to universal testing mandates.
- **Unverified:** This kit's adaptive verification reduces total accepted-delivery cost relative to Jon's present workflow.
- **Unverified:** A separate reviewer materially improves acceptance accuracy enough to repay its cost on each project class.
- **Unverified:** Real-case holdouts adequately represent future use; they require domain judgment and cannot guarantee completeness.
- **Open:** Which checks are most predictive of future integration failure, and how does that differ between software, research, and creative work?
- **Open:** Can a fresh agent reuse the verification and failure records without rebuilding the same understanding? This needs an actual continuation trial.

## Source ledger

All links opened on 2026-10-23. Numerical results above are author-reported; none was independently reproduced here.

| Source | Version/publication | Evidence type | Principal boundary |
|---|---|---|---|
| [Code-before-testing risk](https://arxiv.org/html/2607.05139v1) | 2026-07-06, v1 | Controlled benchmark preprint | Selected subtle faulty generated programs |
| [Regression-test risk](https://arxiv.org/html/2610.11835v1) | 2026-10-08, v1 | Mutation-based historical preprint | Injected faults, three projects |
| [ImpossibleBench](https://arxiv.org/html/2510.20270v1) | 2025-10-23, v1; subsequent ICLR 2026 publication exists | Controlled adversarial benchmark | Deliberately impossible tasks |
| [TDFlow](https://aclanthology.org/2026.eacl-long.70/) | EACL 2026 | Repository-repair study | Gold reproduction tests in headline condition |
| [To Run or Not to Run](https://arxiv.org/html/2606.26978v1) | 2026-06-25, v1 | Execution-policy comparison | 200 ordered benchmark instances, repair only |
| [Cost-inefficient behaviors](https://arxiv.org/html/2609.30725v2) | 2026-09-28, v2 | Trace analysis and interventions | Model-token cost; behavior heuristics |
| [Self-repair](https://arxiv.org/html/2306.09896v5) | 2024-02-02, v5; ICLR 2024 | Budget-aware comparison | Older models, small-program tasks |
| [Compiler account](https://www.anthropic.com/research/building-c-compiler) | 2026-02-05 | Vendor engineering case | No randomized baseline |
| [Application harness](https://www.anthropic.com/research/harness-design-long-running-apps) | 2026-03-24 | Vendor engineering case | Unequal resources; evaluator calibration |
| [Pride and Prejudice](https://aclanthology.org/2024.acl-long.826/) | ACL 2024 | Self-evaluation study | Not a novel-generation study |
| [StoryFeedback](https://arxiv.org/html/2507.16007v1) | 2025-07-21, v1 | Automatic and human assessment | Includes deliberately corrupted stories |
| [LLM Review](https://arxiv.org/html/2601.08003v1) | 2026-01-12, v1 | Short-story pipeline study | Human alignment tested for one framework/model |
