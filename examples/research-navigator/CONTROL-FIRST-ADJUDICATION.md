# Control first-delivery adjudication

The original automated result remains **11 pass, 1 fail, 1 blocked** in `control-first.json`; it has not been rewritten. The adjudicated view is **13 pass**. The heading failure is a demonstrated evaluator limitation on the shared brief, resolved by separate reference-parser evidence and supplemental execution against unchanged code. Independent manual delivery review also passed and is recorded separately in `CONTROL-DELIVERY-REVIEW.md`. No product code changed and no builder repair opportunity was used.

| Case | Original result | Adjudicated result | Evidence |
| --- | --- | --- | --- |
| Clean indexing | Pass | Pass | Original source/hash checks; supplemental clean indexing also passed. |
| Markdown retrieval and context | Fail | Pass; evaluator false failure | The returned parent is a real CommonMark setext heading; complete original anchor and show obligations passed with an independent heading oracle. |
| Second Markdown source | Pass | Pass | Original anchor, locator, heading, and show checks. |
| Dense text input | Pass | Pass | Original line-16 check; manual review additionally exercised retrieval from the long first line. |
| Word heading | Pass | Pass | Original paragraph-72 check. |
| Word table content | Pass | Pass | Original paragraph-28 check; manual review additionally inspected all native source text. |
| Usable source navigation | Pass | Pass | Original checked passages; the previously rejected Markdown passage received a separate native-location check. |
| Stable persistence | Pass | Pass | Original repeat/re-index checks. |
| No-match and input errors | Pass | Pass | Original query/error checks. |
| Export | Pass | Pass | Original report checks; manual review checked relocated source links and explicit current labels. |
| Freshness | Pass | Pass | Original changed/missing/restore/re-index sequence. |
| Failed rebuild preserves usable work | Pass | Pass | Original truncated-real-DOCX fault check. |
| Delivery | Blocked | Pass | `CONTROL-DELIVERY-REVIEW.md` preserves actual command evidence and limitations. |

## The heading is supported by the original source and a reference parser

The original failure came from command 3, searching `largest coherent responsibility`. The result correctly located lines 309–321 and returned the source title, `\text{integration risk}`, and `The agent-completable unit` as its heading chain. The frozen evaluator rejects any Markdown heading absent from its ATX-only heading list.

The source contains `\text{integration risk}` at line 298 immediately followed by a single `-` at line 299. CommonMark permits setext headings underlined with dashes and assigns them level 2. Its preceding paragraph content and block rules matter; a blanket claim that all isolated dashes are headings would be incorrect. [CommonMark 0.31.2 §4.3](https://spec.commonmark.org/0.31.2/#setext-headings)

To resolve that context independently, the already-installed `markdown-it-py` 4.0.0 was run in its documented `commonmark` preset against the entire unchanged original document. It produced an `h2` at lines 298–299 with exactly `\text{integration risk}`, followed by the `h3` at line 309. Its containing chain exactly matches the control output. This reference parser is evaluator tooling, not a new product dependency. [Reference parser configuration](https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser)

The surrounding source appears intended as a LaTeX display equation delimited by `\[` and `\]`. Math-aware document navigation could treat the enclosed terms differently. However, the shared brief neither selected that Markdown extension nor prohibited setext headings. Failing this specific output on an unstated math-aware interpretation would change the acceptance target after delivery. This adjudication does not claim that the product implements every CommonMark rule or that the equation heading is the most useful possible presentation.

## Supplemental execution and preservation

`adjudicate_headings.py` first compares the original returned heading chain with the independent CommonMark parse. It verifies the frozen snapshot's manifest, creates a byte-identical execution copy, indexes untouched copies of the original four documents, and substitutes the independently parsed heading list only in a supplemental evaluator instance. The frozen evaluator file is unchanged.

It then runs clean indexing, the complete original Markdown source-anchor check including the previously skipped `show`, and native-source navigation for that passage. All three checks passed. Original source hashes, all frozen snapshot files, the preserved first-result JSON, and the frozen evaluator were verified unchanged before and after. Evidence is in `control-first-adjudication.json`, including exact source identity, reference-parser version, heading token ranges, all four actual CLI subprocess records, and the adjudicator hash.

The supplemental run started at `2026-10-23`, ended at `2026-10-23`, and took 1.016 measured seconds. Source/specification review and script authoring add coordinator overhead beyond that execution time; no unmeasured exact total is claimed. No builder feedback or code correction was needed for this adjudication.

Independent manual delivery review ran from the observed clock `2026-10-23` through `2026-10-23`, a same-day interval. Its 13 actual CLI subprocesses and source/artifact checks took 1.563 seconds. The reviewer found generic standard-library code, complete native source retention including the long first text line and all 81 Word table paragraphs, correct current labels and relocated links, and substantially supported builder logs. All 65 frozen snapshot file hashes and original corpus hashes stayed unchanged. The remaining historical-log and viewer limitations are retained in the review report. The last required verification completed at `2026-10-23`; adjudication narrative edits after that time add documentation overhead, not further product verification.
