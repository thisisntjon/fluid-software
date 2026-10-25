# Work-unit fields

**Draft v0.1.** Inline in an existing issue or assignment. Use a coherent responsibility rather than a prescribed file count.

- **Outcome / consumer:** One useful deliverable and its contribution to the project.
- **Owner / boundaries:** Outputs this worker may change; shared files, databases, ports, caches or documents it may use; who owns each shared change.
- **Inputs:** Actual source/artifact pointers and relevant versions. Required dependencies and their readiness.
- **Reference role / limits:** Where consequential, state whether the reference defines desired behavior or offers an example; record known defects, conditions and intended departures.
- **Contract:** Inputs, outputs, meaning, failure behavior and constraints that other work relies upon. Link the authoritative contract rather than duplicate it.
- **Evidence of completion:** Real input or use, expected behavior grounded in a reference or accepted requirement, and required checks. Record missing evidence explicitly.
- **Delivery:** Output location/version, result record and next consumer.
- **Status:** Proposed, ready, active, delivered, accepted or blocked; map these meanings to existing project statuses.

## Ready to build

The owner can explain the boundary, access required inputs, identify an observable result and proceed without guessing a shared design decision. Otherwise resolve that decision, investigate the gap, or regroup the unit. Split only if doing so creates independent useful responsibilities; merge units that repeatedly need each other's internal state.

## Exploration branch

When the answer or intended behavior is unresolved, replace the build contract/completion expectation with: **question; competing explanations or approaches; actual sources/inputs; discriminating observation; authorized resource limit; and decision the result will change**. Retain ownership and delivery fields. Completion is an evidence-backed answer or an explicit unresolved limit, not confirmation of the preferred hypothesis. Do not fabricate expected behavior or dispatch dependent builds before resolving their shared question.

## When reality changes

Propose the contract change to its owner with the evidence and affected consumers. Mark dependent results stale where their assumptions no longer hold. Update versions and assignments before continuing affected work; independent work may continue.

If blocked, preserve the partial output and exact failure. Recover the last accepted artifact when useful, then reassign or revise the approach. Do not overwrite accepted work just to restart.
