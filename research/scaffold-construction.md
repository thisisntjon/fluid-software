# Construct the scaffold, then scale the builders

Date: 2026-10-23. Investigator: `/root/practices`. Status: design extension, not implemented or piloted. Inputs: [current design](../../docs/DESIGN.md), [start guide](../../starter-kit/START.md), and the previously opened primary sources below.

## The improvement

Add an explicit **scaffold construction** stage between understanding the outcome and dispatching builders. Its deliverable is a small, navigable project that embodies the important decisions. The documents explain that structure; they are not a substitute for it.

Jon's departmental model is a useful scaling architecture: a worker needs its responsibility and neighboring agreements; a department lead needs its capabilities and dependencies; the project lead needs the whole product and cross-department decisions. The collective can address more than any one context window contains because each level preserves a useful partial view in persistent artifacts. The practical objective is to make those views sufficient and their boundaries dependable.

## Scaffold output contract

Only the first build wave needs this completeness. Later capabilities remain coarse until their dependencies become clearer.

| Output | Concrete artifact | Ready when |
|---|---|---|
| Capability map | Existing project entry links outcomes to actual module directories or document sections | A new worker can locate its contribution and consumer |
| Reused foundation | Selected existing code, project template, source corpus or prior draft, with relevant version and adaptation recorded | The chosen foundation can be inspected and its supported entrypoint used |
| Public boundaries | Actual exported types, schemas, protocol declarations or section/claim agreements | Both sides share meanings, state ownership and failure behavior |
| Owned work surfaces | Real directories/files and ownership of shared mutable resources | Workers can build without silently editing each other's decisions |
| Local working route | Module command, viewer, notebook or document rendering route plus available real inputs | A delivered component can be exercised or inspected without reconstructing the entire project |
| Ready work wave | Existing tracker identifies available dependencies, assigned owners, output locations and completion observations | Each assigned unit can proceed without inventing a missing shared decision |

An empty function, mock result or decorative screen is not a working foundation. An interface declaration is useful structure, but its implementation status remains explicit. If suitable real input is unavailable, mark the evidence dependency; do not manufacture a passing demonstration.

## Build useful structure quickly

**1. Begin from the nearest working reality.** Choose a relevant project archetype, such as an application, pipeline or manuscript, then inspect a suitable foundation and its consumer. Reuse working conventions. Resolve decisions that could invalidate several modules: state, identifiers, execution model, source authority and external interfaces. Internal choices can wait.

**2. Establish one concrete capability.** Build or adapt a small useful responsibility and make its local entrypoint work. This supplies actual examples of project conventions, error handling and delivery. Other workers can imitate inspected patterns instead of independently inventing them. Choose a capability that unlocks others; do not force a complete end-to-end application before independent construction begins.

**3. Publish shared boundaries in their native form.** Prefer the language's type definitions, existing schemas and real module exports over a second description that can drift. Add short semantic notes only where syntax is insufficient: units, ordering, ownership, lifetime and errors. For writing or research, the native form is the actual outline, continuity state, evidence index or claim register.

**4. Dispatch the first independent wave immediately.** Give each builder its owned surface, relevant sources, neighboring boundaries and real completion observation. Builders inspect the local foundation before changing it. Their task is a working component, not an arbitrary quantity of code. Unsettled downstream areas do not hold up ready work.

**5. Let delivery improve the scaffold.** Connect the first completed pair into a real cross-module example. Exercise its consumer and update boundaries when necessary. Each accepted artifact becomes an example for the next wave. Record consequential discoveries where affected workers will find them. Later structure grows from working parts rather than a perfectly predicted architecture.

## Departments and coordinators

Create a department lead when a coherent area has several independently buildable responsibilities and recurring decisions that can be settled within that area. Useful signals include a project lead repeatedly reloading the same domain details, unresolved requests accumulating, or unrelated work being delayed by one domain's coordination.

The department lead owns its public boundary, local work allocation and assembled capability. It can authorize routine internal changes within delegated scope. Escalation is reserved for changes crossing department boundaries, shared resources, acceptance criteria or authority. Builders should not need project-lead permission for every local choice.

Keep cross-department coordination narrow: publish changed interfaces, dependency readiness, accepted outputs and concrete blockers. The project lead reconciles those events rather than consuming every worker transcript. A shared foundation with many consumers deserves a clear owner, not duplicated ownership in every department.

Integration accountability should remain explicit while execution can be distributed. Department leads assemble their own outputs; an existing merge queue or designated integrator handles cross-department assembly. If integration queues grow, redirect capacity there before starting more work. Adding hierarchy should remove information and decision load from the parent, not merely insert another approval hop.

Keep incomplete construction in isolated candidate work. Use focused local checks there; do not impose a new global-green barrier on every edit. Accepted delivery still requires its agreed evidence. Existing CI and owner rules govern both boundaries.

## Why this is a credible acceleration strategy

Cursor's July report explicitly hypothesizes that context efficiency explains swarm scaling better than parallelism. Planners own decisions and prevent separate subtrees from deciding the same question. Its February account describes recursive leads and tolerating incomplete construction before preparing a clean delivery. These practitioner results support the proposed hierarchy; they do not establish unlimited capacity. [July experiment](https://cursor.com/blog/agent-swarm-model-economics), [February architecture](https://cursor.com/blog/self-driving-codebases)

Co-Coder provides a concrete dependency-and-coupling approach to grouping work; CodeTeam materializes public interfaces and ownership before implementation. Their useful design contribution is reducing what separate builders must guess. [Co-Coder](https://arxiv.org/html/2606.00953v1), [CodeTeam](https://arxiv.org/html/2606.22082v1)

Anthropic's later harness removed steps as models improved. Apply the same principle here: keep the scaffold outputs that let workers start and finish; remove ceremony that does not change execution. [Application harness](https://www.anthropic.com/research/harness-design-long-running-apps)

## Measure the multiplier

Use comparable real outcomes and include scaffold creation, supervision, assembly and correction in the accounting. Record:

- Time to the first accepted useful capability and to the complete agreed outcome.
- Human active minutes and compute/tool cost for that outcome.
- Accepted capabilities per elapsed hour, with scope and quality held comparable.
- Worker time lost to missing decisions, repeated discovery and integration queues.
- Contract changes and repair effort after assembly.
- Whether a fresh worker can complete the next real unit from saved artifacts.
- Capacity expansion: whether progressively larger real outcomes become achievable beyond the single-agent baseline, recording the extra compute and coordination required.

A speed multiplier lowers total time at preserved quality, including scaffold cost. A capacity multiplier completes previously unreachable scope, possibly at higher cost. Track these separately. The early diagnostic is more capability delivery and less rediscovery; the decisive observation is an accepted whole.
