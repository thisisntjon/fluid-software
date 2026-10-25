# Rapid scaffolding and bounded context at project scale

Date: 2026-10-23. Researcher: `/root/mechanisms`. Follow-up to Jon's clarification: rapidly create the frame in which many agents can work effectively, analogous to specialized departments. Reviewed `docs/DESIGN.md` and `workflow/PLAN.md`. Design recommendations only; no implementation or pilot performed.

## Assessment

The current design underweights that objective. It explains disciplined local execution well, but makes the project map optional, routes greenfield work toward a first capability, and leaves most cross-project reasoning with one lead. That can improve individual tasks without solving the user's larger scaling problem.

The stronger proposed mechanism is **building an environment in which each agent can act correctly without reconstructing the whole project**. A department is a durable responsibility, knowledge boundary, and authority boundary; it need not be a permanently running agent. The artifact and its boundaries persist while sessions rotate. Five changes make this concrete.

## 1. Add a rapid whole-project scaffold stage

Before broad implementation, construct a shallow map covering the intended whole: capabilities, major responsibilities, owned state, external interactions, shared vocabulary, and dependencies. Resolve the shared choices that would otherwise make workers incompatible. Materialize agreed boundaries in the project's actual medium: package/module locations, public schemas, dependency declarations, build/run entry points, existing source anchors, or a book's outline and continuity record. Use real foundations where suitable; visibly mark missing implementation.

Do not fully specify every function. Expand uncertain, highly connected boundaries first; leave local implementation open. The exit criterion is that ready responsibilities have actual homes, known consumers, sufficient sources, and an observable handoff. Unresolved areas remain explicitly blocked while independent ready work starts. This stage produces a usable construction environment, not merely a plan and not a claim that the product works.

**Bottleneck removed:** every worker separately inventing architecture, conventions, or shared meanings. Anthropic's initializer prepares an environment and durable progress artifacts before subsequent coding sessions. That is practitioner support for initialization as distinct work, not proof of this exact whole-project recipe. [Initializer report](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents).

## 2. Pair broad structure with one representative connected path

A first vertical slice and a whole-project frame answer different questions. The frame establishes where all major responsibilities belong; a connected path exposes whether important boundaries actually work. Build that path using completed real parts while other independent modules develop. Choose a path that crosses a consequential seam, rather than whichever isolated feature is easiest.

This avoids two mistakes: spending the entire beginning perfecting one feature while later workers lack structure, or creating a large hollow skeleton that proves nothing about connection. The frame can remain incomplete in implementation while complete enough in responsibility coverage. Do not add fake implementations to make every branch appear operational.

**Bottleneck removed:** delayed architectural discovery and local optimization around the first feature. This pairing is a design inference, not a directly established optimal sequence. Repo0's bounded repository experiments support explicit, revisable architectural state; its structural refinement results do not justify endless upfront modeling. [Repo0](https://arxiv.org/html/2608.19854v1).

## 3. Organize context at several abstraction levels

Use project → subsystem → module → current change as contextual levels when the project warrants them. The project lead retains purpose, global constraints, external commitments, and unresolved cross-subsystem decisions. A subsystem owner retains its public obligations and the coordination among its modules. A builder loads its module, relevant neighbors, inherited constraints, and current change.

Each level exposes a compact public view with links to authoritative detail. Explicit delegation determines which decisions can be made locally. Escalate a changed boundary or unresolved conflict; do not send every implementation detail upward. Cross-cutting invariants remain directly linked at every affected level so repeated summarization cannot silently erase them. Subsystem-level assembly can proceed under agreed contracts; central accountability need not mean one central merge operation.

**Bottleneck removed:** the coordinator becoming the next oversized context window. Cursor's July follow-up explicitly proposes context efficiency as a larger contributor than parallelism. It separates planners from implementation detail and prevents sibling subtrees from independently deciding the same question. This is a vendor mechanism hypothesis, not an isolated causal result; its experiment changes several harness mechanisms together. The January report also found a dedicated integrator bottleneck. Add a level only when its coordination responsibility is real. [July follow-up](https://cursor.com/blog/agent-swarm-model-economics), [January report](https://cursor.com/blog/scaling-agents).

## 4. Give modules durable knowledge and replaceable sessions

Extend the existing work-unit record into a persistent module home where needed: purpose, public contract/version, source locations, dependencies, current accepted artifact, known limitations, and current work. Keep transient task history separate from the module's current truth. Reuse the project's existing record locations rather than requiring another store.

A new worker reads that entry, verifies relevant actual artifacts, and resumes. A returning worker reloads changed boundary information rather than relying on conversation memory. Preserve rejected approaches only when their reason and reopen condition affect future decisions. The module record should point to code and evidence, not retell them in a second specification likely to drift.

**Bottleneck removed:** repeated discovery and knowledge lost when an agent ends or compresses context. This extends established artifact-based handoff practice; its net savings and maintenance burden remain empirical questions. Success means a replacement agent completes useful work, not merely that a handoff document exists.

## 5. Propagate semantic changes through affected boundaries

Record provider/consumer relationships and the meaning of dependencies. When behavior changes, capture the old/new contract, reason, and affected users. Notify or refresh those responsibility owners, mark relevant acceptance evidence stale, and reassess only dependent work. Purely internal changes need not invalidate every neighbor. Integration acceptance must identify compatible artifact/contract versions, rather than treating “latest” independently in each module as compatible.

Static imports provide hints; they miss shared data meanings, runtime registries, chronology, and scientific assumptions. Allow manually declared semantic edges and conservative escalation when impact is unknown. A book's changed character knowledge can affect later chapters just as altered identifier semantics affect software consumers.

Cursor's July report describes compile-checked links from code to design decisions and reconciliation that propagates changed decisions downstream. Borrow the principle of explicit decision dependencies; the kit does not yet need their custom version-control system or permission for workers to break unrelated code. [July follow-up](https://cursor.com/blog/agent-swarm-model-economics).

**Bottleneck removed:** correct local changes leaving remote components confidently wrong, or every change triggering a project-wide re-review. CodePlan combines incremental dependency analysis, impact analysis and adaptive planning, reporting validity-check success on five of six migration/edit repositories versus none for its baselines. This is bounded empirical support for impact-aware planning, not proof of automatic semantic invalidation across domains. [CodePlan](https://www.microsoft.com/en-us/research/publication/codeplan-repository-level-coding-using-llms-and-planning/).

## What would establish the multiplier

Measure time and human effort until several genuinely independent responsibilities can start, coordination effort as active modules increase, useful cold continuation, boundary churn, integration backlog, and final accepted delivery. These diagnose the mechanism; ready-card counts are not product success. The central prediction is that most growth in local work does not require comparable growth in the root's active context or supervision. That depends on sparse, stable boundaries. If every subsystem continually renegotiates with every other, reorganizing the frame is more promising than adding agents.
