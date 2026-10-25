# Construct the project frame

Draft v0.2, 2026-10-23. Use for a substantial new project or a large project whose structure is hard to navigate. Small changes can use START directly. This guide describes construction of the frame; these templates are not themselves a working project scaffold.

## Outcome

Produce a project in which a fresh agent can locate the whole, locate its responsibility, inspect the relevant real artifacts, identify neighboring obligations, and start useful work without reconstructing the project from conversation. Preserve the complete intended scope at coarse resolution. Detail only the shared decisions and work that must be ready now.

## Build the frame in one focused pass

1. **Map the finished whole.** List the capabilities or sections the requested result needs, their purpose, and their consumers. Every major requested capability has a home, including deferred and unresolved ones. Keep the overview compact and link detail. Do not equate creating a directory with implementing a capability.
2. **Inspect and select foundations.** Locate usable existing code, templates, assets, sources, or prior drafts. Read the relevant material and decide reuse, wrap, adapt, reference-only, or new work. Reuse known project shapes when appropriate; record meaningful departures rather than redesigning standard foundations every time.
3. **Resolve shared meaning.** Establish the small set of decisions that independent builders must share: terminology, owned state, public inputs/outputs, lifecycle, failure meaning and major dependencies. Assign each shared decision one accountable owner. Internal decisions stay with their area. Unresolved architecture that blocks all children becomes a focused exploration unit.
4. **Materialize the structure.** Create or identify actual source packages, public types, entrypoints, source collections, chapter homes, or analysis locations as appropriate. Put contracts next to the relevant artifacts and link existing records. Provide the commands or navigation needed to inspect and operate real implemented parts. Unimplemented areas stay explicitly unimplemented; do not add fabricated behavior or mock success to make the frame appear complete.
5. **Establish a representative real connection.** Build or reuse two small coherent parts whose connection exercises a consequential boundary. Let each work standalone, then connect them using an actual input or real reading/analysis path. This provides a concrete pattern other builders can follow. It need not wait for the rest of the product or become its only represented capability.
6. **Prepare the first independent work.** Select units with available inputs and settled-enough boundaries. Name owners, relevant versions, completion observations and delivery locations. A worker can request missing context; narrow initial context must not prohibit necessary investigation.

Steps 5 and 6 can overlap: dispatch ready independent units as soon as their required boundaries exist, while the representative connection is completed. Only work that depends on that unsettled connection waits. The numbering does not impose a whole-project synchronization barrier.

Do not wait for exhaustive leaf-level planning. Stop preparing when the next useful responsibilities are ready to build. Continue broadening/refining the frame as actual construction exposes missing decisions.

## Three context views

| View | Contains | Usually omits |
|---|---|---|
| Whole | Purpose, complete capability map, global constraints, accepted state and cross-area decisions | Worker transcripts and local debugging history |
| Area | Responsibility, neighbors, shared contracts, working artifacts, known failures and next units | Unrelated departments' implementation details |
| Assignment | Immediate outcome, owned changes, actual inputs, applicable contracts and useful completion evidence | The entire history of the project |

Each view points to originals, their versions and unresolved exceptions. Summaries are routing aids, not replacements for source evidence. An area lead maintains its view in the area's existing records. The role may persist while the agent session changes.

## Organize responsibility at the needed scale

Begin with one lead and ready builders. Add an area lead when a coherent subsystem has enough related work that root-level planning repeatedly needs its internals. Delegate the subsystem's internal decisions and local assembly to that lead. Escalate shared semantics, resource conflicts, global invariants and changes in intended outcomes to the nearest owner whose scope contains the affected areas.

Keep a dependency map across the hierarchy. Adjacent areas may need direct contract clarification; do not make every factual exchange travel up and down the full tree. No two leads should independently decide the same shared question. Add hierarchy because it reduces repeated context and decisions, not because an organization chart looks complete.

## Keep the frame current

When a shared contract or source assumption changes, record the revision and the affected consumers. Refresh their context and reconsider dependent acceptance evidence. Route that change to affected areas rather than replaying all history to every agent. Preserve material exceptions and contrary evidence in the summary.

Candidate work may be incomplete. Keep the last accepted artifact separately identifiable and preserve required CI. A local unfinished branch is not a claim that the assembled result works. Give repair work an owner, a concrete failure and a changed diagnosis or new observation; do not let unrelated defects trigger every worker to repair the same subsystem.

## Ready for builders

A fresh worker should be able to answer, using the frame and its linked artifacts:

- What is the whole trying to accomplish, and which part am I responsible for?
- What already exists, what is accepted, and what is unfinished?
- Which real inputs, interfaces and neighboring constraints matter here?
- What may I decide, and who owns a shared decision I cannot make locally?
- What useful output will I deliver, how will it connect, and what observation will establish it works?

Use those answers to start real work. This is an orientation check, not a new examination or repeated approval gate. Evaluate the frame through subsequent independent construction and assembly, not through how impressive its diagrams appear.
