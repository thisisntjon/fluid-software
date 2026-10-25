# Mechanisms, decomposition, and cross-domain transfer

Date: 2026-10-23. Researcher: `/root/mechanisms`. Scope: primary-source audit of the supplied `junglegym.md` and `deep-research-report.md`; focused research on source scaffolds, behavioral references, decomposition, and writing. No benchmark was executed and no reported experiment was independently reproduced.

## Finding

The hypothesis is promising but should be **refined**, not declared proven. Existing software combines several interventions: reusable implementation, resolved architectural choices, discoverable interfaces, observable behavior, and persistent state. A code scaffold and a behavioral oracle are different things. A useful starter kit should preserve both where available, while recording which one is missing. The evidence does not establish that either alone explains the Baldies or Consumption Engine timelines.

The operational target is a coherent responsibility with a bounded change surface, sufficient local context, and observable completion. Neither a universally optimal task size nor a guaranteed-success recursion depth has been established. A model's confidence that it can build a component is insufficient evidence of readiness.

## Corrections to the inherited investigation

**ProgramBench's zero is historical.** The initial May 5, 2026 paper evaluated nine models on 200 reconstruction tasks and reported zero fully resolved tasks. That faithfully describes that experiment. The project's primary leaderboard, updated October 22, now reports 18.5% resolved for Claude Opus 5.5, or 37/200. Its contemporaneous FAQ still contains broader zero-success language, so the dated result table should control the current numerical claim. This remains a difficult benchmark, but it no longer supports “current models cannot fully solve a single task.” [May paper](https://arxiv.org/abs/2605.03546), [current project leaderboard](https://programbench.com/).

**MirrorCode versus ProgramBench is not an oracle ablation.** Both supply reference executables without original source. MirrorCode's July paper explicitly documents different scope visibility and much larger resources: mean Opus 4.7 cost was $106 versus $3.81, a 28-fold difference. Its visible-test ablation hurts complex tasks, but also changes scope cues and submission gating. Its 56% headline is a dated paper result; the current leaderboard uses a different subset/configuration. The gotree result was 2,000/2,001 tests, near-perfect rather than complete. The paper also acknowledges memorization and code-quality limitations. None of this isolates the causal value of original source code. [MirrorCode paper, especially §§2.2, 3.4 and Appendix E](https://arxiv.org/html/2606.30182v2), [current benchmark definition](https://epoch.ai/MirrorCode).

**The “word-level decomposition is contradicted” claim overstates the writing evidence.** The cited studies support hierarchical planning and show costs of some fine-grained or parallel procedures. They do not run a controlled chapter-versus-paragraph-versus-sentence-versus-word depth sweep on current models. Treat unlimited refinement as unsupported and potentially costly, rather than claiming the precise optimal depth is experimentally settled.

**An 80% task horizon is not a component-sizing calculator.** Human task duration on a benchmark does not directly convert to the permissible duration of a particular component in a new domain. Use relevant observed completion and handoff experience. Record uncertainty when there is no comparable history.

## What the empirical studies establish

### Decomposition needs an execution mechanism

Parsel combines hierarchical descriptions with implementation search and executable constraints. Its APPS comparison reported 25.5% versus 6% when high-level plans were translated directly into Python instead of using its synthesis pipeline. The direct-Python ablation used 100 sampled problems; the headline pipeline result used a larger evaluation. The authors matched generated-program budgets, but this is not an information-identical comparison of existing source versus prose. It supports the combined mechanism of decomposition, constrained composition, and search. It does not show that merely creating more task cards improves repository delivery. [Parsel, §3](https://proceedings.neurips.cc/paper_files/paper/2023/file/6445dd88ebb9a6a3afa0b126ad87fe41-Paper-Conference.pdf).

Commit0 supplies specifications, skeletons, and interactive tests across 54 Python libraries. Its generation-unit ablation reports average test pass rates of 17.80 for module-level filling and 12.42 for pass-statement filling. The local generation procedure sometimes missed surrounding implementation responsibilities. This is direct evidence that smaller units can lose necessary context in that setup; it is not a universal claim that functions are bad work units. [Commit0, Appendix D](https://arxiv.org/html/2412.01769v1).

CodeS separates repository sketching, file sketching, and function filling. Its evaluation includes a structural similarity metric, SketchBLEU, and a study with 30 participants. It supports scaffolding as a practical design pattern, but structural similarity is not equivalent to accepted product behavior. Repo0 maintains aligned requirement and component graphs, evolving boundaries before generation; its reported comparison covers six repositories with two models. These are useful proposals and bounded evidence, not validation of a universal starter kit. [CodeS](https://arxiv.org/abs/2403.16443), [Repo0](https://arxiv.org/abs/2608.19854).

### Newly found evidence: adaptation and packaged boundaries

The October 6 LEGO/CodeFace preprint is directly relevant. Across 522 Python-package reconstruction tasks, its normalized delivery score rises from .3180 with execution feedback to .5134 with reusable, adapted components. This is a score, not a project-success percentage. Supplying a generic editor with carried tests, contract/provenance, and dependency closure reaches .5039; its difference from the full mechanism is not statistically clear in that comparison. The authors explicitly warn that sequential field additions do not identify independent causal contributions. Default library provenance can overlap benchmark-related construction; disjoint controls retain smaller gains. Cost accounting excludes infrastructure and counts successful adaptation calls, and reported median runtime increases. This is preliminary support for usable reusable components, not a demonstrated speed multiplier or clean prose-versus-code experiment. [LEGO, Tables 5–6, Appendix G.4, J and L](https://arxiv.org/html/2610.09079v1).

### Writing confirms hierarchy, while preserving sequence matters

Re3 combines planning, contextual reprompting, reranking, and editing; human evaluation reports a 14-point absolute coherence gain and a 20-point premise-relevance gain over comparable-length direct generation. Those gains belong to the combined pipeline. DOC adds detailed outlines and control, reporting human preference gains over Re3. Its 58.5% leaf-faithfulness result versus 37.8% without control is a controller ablation, not a test showing that deeper outlines inherently harm writing. It instead shows that creating detailed plans does not guarantee execution follows them. [Re3](https://aclanthology.org/2022.emnlp-main.296/), [DOC, especially Table 6](https://aclanthology.org/2023.acl-long.190.pdf).

LongWriter's AgentWrite produces long outputs by planning then writing sections sequentially with prior text available. Its parallel variant loses about six points of coherence in the reported evaluation; GPT-4o supplied the quality judgments. That supports caution about independently drafting interdependent prose, with evaluator and model-era limits. DOME later combines dynamic hierarchical outlining with memory for changing story state. This reinforces keeping plans revisable rather than freezing every future sentence before drafting. [LongWriter, §3.2](https://proceedings.iclr.cc/paper_files/paper/2025/file/59f278de1619bdb6b53fd04e8e0976e0-Paper-Conference.pdf), [DOME](https://aclanthology.org/2025.naacl-long.63/).

Long-context retrieval studies establish that information can be present yet poorly used. The classic Lost in the Middle study concerns question answering and key-value retrieval, not a modern multi-day software build. Using it to justify local context packets is a design inference, not a measured effect size for this kit. [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/).

## Mechanistic synthesis — an inference to test

The scaffold appears to work through five separable channels:

1. **Reuse:** solved implementation need not be generated again.
2. **Decision reduction:** established interfaces and conventions reduce unresolved design choices.
3. **External state:** an inspectable artifact preserves what exists and where unfinished work remains.
4. **Feedback:** execution or an independent evaluator makes specific failures observable.
5. **Local repair:** bounded changes can preserve previously accepted work.

Parallelism exploits these channels when separate work can advance independently. It does not create independence. A decomposition tree records purpose; a dependency map records constraints on concurrency. Shared state, narrative causality, or a scientific assumption may couple distant branches of the tree.

The common failure is moving ambiguity rather than resolving it: an unclear product becomes unclear module cards, then incompatible components, then tests that validate each component's own assumptions. More artifacts do not necessarily mean less uncertainty. The kit should ask what decision each artifact settles and what independent observation could overturn it.

## Operational rule: when to stop splitting

Stop at the **largest coherent responsibility** for which all these answers are available:

- A named parent outcome explains why this unit exists.
- Inputs, outputs, relevant state, and failure behavior are concrete enough for another builder to use.
- One owner can make the change without simultaneously renegotiating unrelated components.
- Required sources and neighboring constraints are accessible within a practical working context.
- A real example, reference behavior, source-backed criterion, or agreed human judgment can establish useful completion.
- The output can be handed off, connected, and selectively revised.

Split an unresolved unit when different responsibilities can satisfy those conditions separately. If a proposed split requires frequent bilateral design decisions, shared edits, or a large repeated context packet, retain one owner or coarsen the boundary. Resolve high-fan-out shared contracts before scheduling dependents. These are proposed decision rules, not validated numerical thresholds.

Do not “split until confidence is high.” Ask the worker to identify its consumer, completion evidence, dependencies, and unknowns. An unanswered boundary question routes to a small investigation or contract decision. An implementation difficulty within a coherent boundary routes to a prototype or repair. A new discovery can justify merging units again.

## Project-agnostic adaptations

| Domain | Useful unit | Shared constraints | Completion evidence | Assembly |
|---|---|---|---|---|
| Software | Capability/component with owned state | APIs, units, errors, lifecycle | Real inputs and independent expected behavior | Actual consumer path |
| Book | Scene/chapter or research contribution | Voice, chronology, character knowledge, motifs | Author intent and reader/editor judgment | Consecutive reading and revision |
| Research | Answerable question, analysis, or evidence synthesis | Definitions, source versions, assumptions | Original evidence and reproducible reasoning | Argument and contradiction reconciliation |

For a book, parallelize source gathering, alternate outlines, or bounded scenes only when their dependencies are explicit. Keep a single editorial owner for voice and causal continuity. The final word can be intentional through revision; it need not have been a separately planned work package.

For research, do not replace uncertainty with fabricated executable oracles. Preserve contrary evidence and confidence limits. A source-backed answer that changes the plan is more useful than many consistent summaries. For greenfield products, agree observable user outcomes and use real examples; an unrelated reference implementation is evidence to inspect, not the authority on what the new product should do.

## Discriminating evaluation design

The inherited factorial is a good starting point but its “scaffold” treatment bundles implementation and oracle access. Separate two estimands:

**Practical reuse benefit:** Does giving builders a suitable real implementation improve accepted delivery, counting discovery, adaptation, verification, and integration? The artifact intentionally contains more solved work. This answers the business question without pretending information content is equal.

**Representation benefit:** Do materialized interfaces/layout improve work relative to a prose description conveying those same decisions, with behavior and reusable implementation held constant? This is harder to equalize; report remaining information differences explicitly.

For an initial real-project pilot, choose comparable pending capabilities and freeze owner-approved acceptance before assignment. Compare a capable ordinary workflow against the portable kit at the same model/tool settings. Preserve failures, all preparation effort, interventions, and time to accepted capability. Do not randomize away indispensable safety or integrity checks. A pilot establishes feasibility, not causality.

If the pilot warrants a controlled follow-up, use real historical snapshots with independent outcome evidence. Cross structural scaffold availability with behavioral-reference availability while holding the specification, model, tools, budgets and final evaluator constant. Block by task family, randomize assignments, use fresh sessions, and predeclare how external source access is handled. Then investigate decomposition and parallelism separately instead of expanding immediately to a huge factorial. Choose repetitions from observed variance and the decision's required precision, not an arbitrary universal sample count.

Primary outcomes: accepted usable capabilities, total human effort, total compute expense, and wall time. Mechanism measures: repeated implementation, first assembly failures, boundary renegotiations, and regression/recovery effort. Equal token budgets and equal cost budgets answer different questions; report both where practical. Include setup and unsuccessful runs. A faster local build that creates a larger integration backlog is a failure of the strategy.

Disconfirmation would include: no practical improvement after full costs; gains disappearing when reference behavior is controlled; fine-grained decomposition consistently worsening accepted outcomes; or a lightweight single-agent workflow matching the kit with less administration. The kit must permit deleting ineffective mechanisms.

## Assumption candidates and open questions

- **M1:** Reusable artifacts help through several channels; their independent effect sizes remain unresolved. Status: plausible synthesis, partially supported by controlled studies. Affects: reuse policy and experiments.
- **M2:** A coherent-unit stopping rule transfers better than fixed file, token, or hour limits. Status: proposed operational policy supported by bounded counterexamples. Affects: component template.
- **M3:** Boundary evidence may matter more than a bespoke multi-agent framework. Status: promising recent preprint result, requires replication. Affects: keep the initial kit manual and portable.
- **M4:** Cross-domain portability requires different acceptance and assembly procedures. Status: supported distinction; kit transfer untested. Affects: adapters.
- **M5:** The local two-day/one-day histories do not isolate the cause of improvement. Status: confounding established from the user account; contribution sizes unknown. Affects: public claims and evaluation.

Outstanding: minimum useful scaffold; cost of maintaining boundary records; best unit size by model/domain; when references anchor a poor architecture; whether recovery avoids enough rework to justify its bookkeeping; and how much of the reported speed came from prior project learning. These require task-level local evidence, not more general literature alone.

## Source ledger

All links above were opened on 2026-10-23. Dates/versions: ProgramBench May 2026 v1 and October 22 live leaderboard; MirrorCode July 17 v2 and current project page; Parsel NeurIPS 2023; Commit0 December 2024 v1; CodeS March 2024 v1; Repo0 August 2026 v1; LEGO October 6 2026 v1; Re3 EMNLP 2022; DOC ACL 2023; LongWriter ICLR 2025; DOME NAACL 2025; Lost in the Middle TACL 2024. New preprints were inspected as author-reported evidence, not independent replications. Dynamic pages require rechecking before later reuse.
