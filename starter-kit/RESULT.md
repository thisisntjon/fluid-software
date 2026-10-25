# Result fields

**Draft v0.1.** Attach to the existing unit or delivery record. This records evidence; it does not manufacture acceptance.

- **Outcome and version:** Exact delivered artifact, source revision or document version; author and work-unit link.
- **What now works:** Concrete behavior or useful content produced.
- **Check:** Actual input/source, command or observation, expected basis, observed result, and evidence location. Record failures and not-run checks separately.
- **Limits:** Missing behavior, uncertain claims, environment constraints and affected dependencies.
- **Disposition:** Locally checked; assembled and checked; accepted by named consumer/reviewer; or blocked. Record only stages that occurred and their basis.
- **Next action:** Consumer, owner and continuation pointer; last accepted artifact if recovery is needed.

Optional learning: what evidence changed a decision, the resulting action, where it applies, and when to reopen it. A green suite alone is not a lesson.

Do not repeat an unchanged check without a reason: changed output, dependency, environment, unresolved uncertainty or required policy. A contract or source correction invalidates only the results that depend on it, but those results must be refreshed before reuse. Builder checks remain useful; consequential acceptance needs evidence beyond the builder's confidence.
