# Prospective review of the frozen evaluator

Prepared after the evaluator was frozen and both builders were dispatched, but before inspecting either implementation or its delivered outputs. The root reported a freeze time of `2026-10-23`; the authoritative timestamp and artifact identities remain in `freeze.json`. This review changes neither the shared brief nor the evaluator. It identifies possible mismatches between the fixed product requirements and the evaluator's formatting assumptions so any later adjudication can be symmetric and transparent.

Reviewed only `TASK_BRIEF.md`, `PROTOCOL.md`, and `evaluate.py`, plus the source expectations already checked before the builds. Neither arm was run or inspected for this review. Frozen evaluator SHA-256 remains `7c908f1c2ef849318fa11e1a8887c7f57ded69060802773c58fc557bb6dfe984`.

## Finding

Yes: a failed export-format assertion may require manual, format-aware adjudication. The shared brief requires readable Markdown that preserves complete source text, source links, native locators, headings, indexed hashes, and freshness status. It does not prescribe Markdown block structure, link syntax, or the spelling of a printed locator. The protocol similarly asks the evaluator to read the report and resolve its links. The frozen program sometimes substitutes a narrower string/regex check for that observable behavior.

This is a limitation in the evaluator I wrote. It must not become a requirement for a builder to weaken its report formatting merely to satisfy an accidental parser convention. At the same time, a formatting explanation cannot excuse missing text, incorrect provenance, broken links, or hidden stale evidence.

## Known candidates for false failures

| Frozen check | Possible legitimate output it can reject | Manual decision required |
| --- | --- | --- |
| `export_one`: `hit['text'] in text` | A complete multiline passage quoted with a Markdown `>` prefix on each line; an indented/code block; source text escaped so Markdown displays its original characters. The source text remains complete, but its serialized bytes are interrupted by presentation syntax. | Is the complete selected passage recoverable from a clearly identified report block, in its original order and without omission or invented content? Remove only that report's documented presentation syntax; do not remove real source punctuation or infer missing text. |
| `export_one`: `anchor['text'] in text` | Markdown escaping or line wrapping within a frozen anchor can break its raw substring even though the same source text is displayed. All frozen anchors are single source lines/paragraphs, so a plain prefix at the beginning of an anchor line alone will usually still pass this check; multiline wrapping/escaping can fail it. | Compare the recovered source text with the independently frozen anchor and source locator. A raw JSON passage losing source text is a different issue; export presentation does not justify changing the JSON contract. |
| `linked_paths` | Valid Markdown reference links, autolinks, or inline links with an optional title. The regex recognizes only a subset of inline links and can treat a title as part of the path. | Resolve the actual link according to its Markdown form, percent-decode correctly, and prove that the destination is the intended original file from the report's own directory. A printed path that is not a functioning Markdown link is insufficient. |
| `export_one` locator regex | A clearly labelled `L311–319`, a `#L311-L319` link fragment, or a range laid out across table cells/lines. The regex expects the word `line` or `paragraph` with both endpoint numerals in the following 100 characters. | Verify that the report unambiguously identifies the native kind and inclusive range for its complete selected passage. Do not accept a page number in place of a DOCX body-paragraph ordinal, or an unrelated number elsewhere in the report. |
| `export_one` heading substrings | The source heading displayed with escapes or inline formatting can be correct without containing its raw string contiguously. | Recover the actual displayed heading context and compare with the source. A filename alone is not a containing source heading. |
| `navigation`: heading at locator start | A passage locator may legitimately include a leading blank line before its heading, or span more than one section while identifying the matched text's containing section. The evaluator checks for a heading active at the first native position. | Inspect the stated range and matched text. Accept only if the report's heading context correctly locates that text and the passage remains understandable; do not accept invented or unrelated headings. |
| `delivery`: root-only README discovery | The brief asks for a README without explicitly freezing its directory. A clearly discoverable project README in a documented subdirectory could be missed. | Confirm actual discoverability and runnable instructions. This does not excuse absent documentation or inaccurate claims. |

The query text and source hash normally need no format interpretation in these concrete queries. If either is absent, do not assume that passage content implicitly supplies it.

## Do not turn an interrupted case into a pass

`run_case` stops on its first failed assertion. `exports` checks Word first and Markdown second. `freshness` checks changed-source export before missing-source export, restored-current status, and refreshed content/hash after re-indexing. An export-format false failure can therefore prevent later obligations from being exercised.

If this occurs, preserve the original failed row and its command transcript. Adjudicating the formatting assertion alone does not establish that the whole row passed. The later commands must be run against the same delivered artifact in a new coordinator runtime, with private copies of the same actual source files. Record their timestamps, exact commands, results, source hashes, and any fault injection. A case whose remaining obligations were not run stays blocked in the adjudicated view.

## Known limits of a green automated result

The frozen program provides strong direct evidence for the source anchors and exercised CLI path, but it is not a complete specification proof. These limits should be handled through the already-planned manual delivery review, not by adding unequal post-delivery requirements:

- The stale-export check finds the word `changed` or `missing` anywhere in the report. That word could occur inside quoted research prose. The reviewer must confirm an explicit freshness annotation attached to the relevant source or passage. Likewise, current exports must expose current status as required by the shared brief; the frozen export check does not independently enforce that label.
- Link checks prove at least the intended anchor's source link resolves. They do not comprehensively validate every link in a multi-result report.
- Five real anchors establish useful coverage, including Word tables, but do not prove that every source passage was retained. The dense-text anchor is on line 16; a pass there alone does not establish retention of the long first line.
- Stable-persistence checks cover the exercised query. The evaluator does not exhaustively test all passage IDs, all search phrases, or every whitespace-spanning query.
- Corpus copies and the index paths contain spaces, but the executable path is absolute. The automated run does not establish every relative-path invocation promised in the brief.
- No-match and error checks exercise four specified errors; they do not audit all failure modes.
- CLI behavior alone cannot prove that parsing is generic, that no query is hardcoded, that implementation dependencies are exclusively standard-library, or that builder logs accurately report actions. Those remain explicit delivery-review responsibilities.

No passing row should be promoted into a broader claim than its transcript supports.

## Symmetric append-only adjudication procedure

1. Preserve the frozen evaluator bytes and both initial result JSON files unchanged. Do not rerun a repaired implementation and call it a first-pass result.
2. Review an actual failure against this prospective list and the original shared requirement, without considering which arm produced it. Apply the same interpretation to both arms, including an arm that happened to pass the narrower automated check.
3. Add a separate adjudication record containing: arm; delivered artifact identity; original case and command ID; original reason; actual report path/hash; governing brief/protocol text; observed source-backed formatting; precise recovery/link-resolution procedure; and decision.
4. Where the automated failure stopped later obligations, record additional real CLI executions on the unchanged delivered artifact before declaring that complete capability usable. Use only private copies of the actual corpus for faults. Do not invent fixture documents or edit a report into correctness.
5. Report original automated outcome and adjudicated outcome side by side. Distinguish `evaluator-format false failure`, `product defect`, and `not yet established`. Do not delete failures or silently recalculate the first-pass tally.
6. If the program itself needs a fix, that is an arm repair under the same one-opportunity policy, not evaluator adjudication. Record the repair separately. Pure evaluator misclassification should not consume an arm's repair opportunity.

This review does not pre-approve any artifact, waive any acceptance requirement, or prescribe a winning formatting choice. It establishes how to distinguish a product defect from a frozen evaluator limitation if the actual evidence warrants it.
