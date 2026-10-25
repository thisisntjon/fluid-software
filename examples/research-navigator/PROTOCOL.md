# Research Navigator comparison protocol

Status: protocol finalized for the first paired example. Exact artifact identities, arm directories and dispatch prompts are recorded in freeze.json before dispatch. Final resource policy: one fresh builder per arm, no child agents, a bounded initial pass per initial build; one repair opportunity of up to a bounded repair pass per arm after both first-pass evaluations are preserved. Model/reasoning settings are inherited equally, with exact backend version and token/dollar telemetry unavailable. No aggregate-token matching is claimed.

## Question and scope

Can the working foundation help a fresh agent deliver a usable multi-component research CLI on Jon's actual documents, compared with a capable ordinary agent given the same product requirements? This is one descriptive matched example, not a statistical estimate, proof of speedup, or isolated measurement of every foundation mechanism. A tie or a control win is useful evidence.

The foundation arm receives the generated project frame and its normal usage guidance. The control arm begins without those artifacts and may plan, create its own architecture or scaffolds, inspect Python's standard library, and use ordinary native tools. Do not make the control intentionally disorganized or prohibit useful engineering practices. Both arms receive byte-identical copies of `TASK_BRIEF.md` and the four original source documents. The extracted `research/input-docx.txt` is coordinator inspection evidence and is not a substitute for the actual DOCX input.

## Frozen inputs and separation

Before dispatch, the coordinator must:

1. Finalize and hash this protocol, the common task brief, `SOURCE_EXPECTATIONS.json`, and the generated foundation frame. The source expectations were derived independently from source bytes before implementation, not from either builder's output.
2. Copy the four originals into each arm's input directory and compare every copied file's SHA-256 and byte length with the manifest. Never edit the originals. Each builder's writable scope is its own project/runtime directory.
3. Use fresh agent contexts with the same model and reasoning settings, the same native tool availability, the same brief and source bytes, the same declared active-builder limit, and the same wall-clock cap. Recommended for this small run: one builder per arm and no builder subagents, because the shared platform has four total agent slots. Record actual settings or say when they are inherited but not exposed. This design evaluates a foundation-assisted builder, not a larger swarm advantage.
4. Keep the build prompts identical except for arm path and access to foundation artifacts and usage instructions. Preserve both prompts. Both must explicitly permit ordinary planning/debugging and bar access to the other arm or coordinator/evaluation files. Shared filesystem separation is an instruction boundary, not an operating-system sandbox; report that limitation.
5. Keep source-only expectations outside builder editable scopes. Builders know the acceptance categories and interface in the brief. No evaluator expectation may be derived from a builder's own implementation.
6. Record the freeze and dispatch UTC timestamps. Launch the two builders in close succession. If they overlap, report possible CPU/tool contention. Do not give one arm extra unsolicited hints or shared discoveries from the other.

The root may select the final use-case before freeze. After dispatch, changes to requirements or corpus invalidate the matched run unless applied equally and explicitly recorded. Keep pre-change evidence; do not silently restart a losing arm.

## Measures and repair policy

Capture first delivery before independent evaluation or repairs. Run the same external checks against each first-delivery artifact and report each acceptance item as pass/fail/blocked with command evidence. Record missing features explicitly, not as an overall success inferred from a green command.

Record UTC build start, first delivery, evaluation start/end, repair requests and responses, and final verified delivery; derive elapsed durations only from observed timestamps. Record every substantive human/coordinator intervention. Preserve original outputs and builder completion messages. Tool-call counts, tokens, and dollar cost are reported only if directly available and comparable; otherwise mark them unavailable. File count, LOC, self-reported confidence, and number of tests are not quality scores.

Separate reusable foundation authoring time from the example's per-arm work. Report that one-time investment even though it is outside the two build clocks. Target-specific frame generation/setup is foundation-arm preparation and must be shown separately and included in any total time comparison. Shared brief/oracle/corpus preparation is shared evaluation setup, not free work credited to either arm. Include actual repair and review effort; do not compare an unrepaired first control delivery against a repaired foundation delivery.

If an arm fails, return only concrete observed failures and repro commands from its own run. Apply the same repair opportunity and time cap to both arms. Freeze first-pass results before sending feedback. Report both first-pass and final results; do not hide failed attempts. If one arm remains incomplete, report the surviving usable artifact and the failure without claiming a reliable method advantage.

## Independent real-input acceptance

The evaluator may inspect the brief and original sources now, but must not inspect foundation internals or either implementation before freezing source expectations. After builds, evaluation uses real CLI processes and independent source byte/XML reads. Test artifacts are copies or reports of these real documents, not fabricated domain fixtures.

| Check | Procedure and observable acceptance |
| --- | --- |
| Clean indexing | From a new runtime directory, index all four copied originals. JSON names exactly the four sources with their manifest hashes. Every current status is correct. No dependency installation or network is required. |
| Markdown retrieval and context | Search the exact phrase `largest coherent responsibility` with a generous limit; a match from `deep-research-report.md` must contain the original text at line 313, cover that line in its native locator, and include `The agent-completable unit` in its heading context. Verify against original line bytes, not index internals. |
| Second Markdown source | Search `Parallelize only across independent, separately gradable units`. A `junglegym.md` match covers line 119, preserves its text, and includes `Recommendations` in heading context. |
| Dense text input | Search `Measure usable connected capabilities`. A `resuse.txt` match covers line 16 and preserves that real line. The long first line must not cause the file to be skipped or truncated into a token placeholder. |
| Word heading | Search `The Over-Mocking Epidemic`. A DOCX match includes original paragraph 72 and its full text. `show` resolves its returned ID and returns the same text and locator. |
| Word table content | Search `Strictly bounded by AST dependency graphs`. A DOCX match includes paragraph 28, which is inside a table; its text includes the independently frozen exact paragraph text and locator covers 28. This catches body-only extraction that drops tables. |
| Usable source navigation | For returned hits, independently re-read the stated line/paragraph range from the named original. Verify the displayed content is source-backed and heading context is appropriate. Do not require the evaluator to inspect internal index format or arbitrary passage counts. |
| Stable persistence | Reopen the index in new CLI processes; repeat one query and `show`. Re-index unchanged bytes and verify corresponding passage IDs remain unchanged. Confirm the corpus hashes remain untouched. |
| No-match and input errors | Search an actual source document's SHA-256 string, first independently verifying that string does not appear in any source text: zero matches and exit 0. Empty query, zero limit, nonexistent index, and invalid passage ID must produce nonzero errors, without fake success. |
| Export | Export the DOCX table phrase and a Markdown phrase to reports outside the corpus directory. Read each report: relevant complete text, source hash, native locator and heading context are present; decode each source link and confirm it resolves to the original file. The report's file link need not navigate inside Word. |
| Freshness | On a private copy only, index the true corpus and confirm all current. Change one real text file in place with a same-byte-length case edit of an existing real word, restoring its original mtime. Status must report changed despite equal size/mtime; search/show/export must mark its indexed passages changed and retain old indexed text. Temporarily move a different copied source outside its indexed location; status and retrieved evidence must say missing. Restore both copies and verify current, then re-index the edited copy and verify the new hash/content becomes current. Never modify originals. |
| Failed rebuild preserves usable work | On a private copy only, make an actual copied DOCX unreadable by truncating its existing bytes; run index against an already good index. Expect nonzero failure identifying the source, followed by successful retrieval from the previous index. This is a fault injection into a real artifact, not fabricated content. |
| Delivery | README commands are runnable with the actual filenames and explain limitations. The builder's log distinguishes actions it actually ran from unverified claims. No hardcoded query answers or fake passages substitute for parsing. |

Each row is reported separately. A shorter report may group related rows for presentation, but must retain the evidence and failures. The stated source counts are provenance facts; passage count and internal module shape are intentionally not graded.

## Pre-build source observations

Original byte sizes and SHA-256 values are recorded in `SOURCE_EXPECTATIONS.json`. Independently read using Python `pathlib`, `hashlib`, `zipfile`, and `xml.etree.ElementTree` on the source files. These observations do not depend on either implementation:

- `deep-research-report.md`: 1,048 source lines; section `The agent-completable unit` begins at line 309 and the bounded-unit definition is line 313.
- `junglegym.md`: 177 source lines; `Recommendations` begins at line 113 and the independent-units recommendation is line 119.
- `resuse.txt`: 17 source lines; useful-product measurement statement is line 16. Line 1 is unusually long; do not mistake it for an empty or invalid document.
- DOCX: 223 body paragraphs including empty and table paragraphs; 216 have nonempty text. Paragraph 72 is a `Heading3`; paragraph 28 is in a table. Count/body text extraction is document-order `.//w:body//w:p` and concatenated descendant `w:t` text. This is a native XML locator, not a rendered page number.

These documents contain unverified research claims and citation markers. Retrieval fidelity does not establish those claims as true; the comparison evaluates software behavior, not the research assertions.
