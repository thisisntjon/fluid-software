# Foundation first-delivery adjudication

The unchanged foundation delivery satisfies the 13 protocol rows after supplemental evaluation and manual delivery review. The original automated result remains **11 pass, 1 fail, 1 blocked** in `foundation-first.json`; it has not been rewritten. The adjudicated view is **13 pass**, with the two decisions below recorded separately. No product code changed and no builder repair opportunity was used.

| Case | Original result | Adjudicated result | Evidence |
| --- | --- | --- | --- |
| Clean indexing | Pass | Pass | Original evaluation; supplemental fresh indexing also passed. |
| Markdown retrieval and context | Pass | Pass | Original source-anchor, locator, heading, and show checks. |
| Second Markdown source | Pass | Pass | Original source-anchor, locator, heading, and show checks. |
| Dense text input | Pass | Pass | Original line-16 anchor; manual review additionally checked all nonblank native content. |
| Word heading | Pass | Pass | Original paragraph-72 check. |
| Word table content | Pass | Pass | Original paragraph-28 check; manual review additionally checked all 81 table paragraphs. |
| Usable source navigation | Pass | Pass | Original native-range checks. |
| Stable persistence | Pass | Pass | Original separate-process and unchanged-reindex checks. |
| No-match and input errors | Pass | Pass | Original five query/error observations. |
| Export | Pass | Pass | Original current exports; manual review checked current status annotations and links. |
| Freshness | Fail | Pass; evaluator false failure | Complete raw source text was present. The full original freshness procedure was rerun with byte-preserving report reads. |
| Failed rebuild preserves usable work | Pass | Pass | Original truncated-real-DOCX fault and retained-index retrieval. |
| Delivery | Blocked | Pass | Independent manual source review and five README CLI commands. |

## Freshness diagnosis

Original commands 29–31 retrieved, showed, and exported the indexed `resuse.txt` passage at lines 14–17. That passage contains three CRLF line endings. The exported `changed-evidence.md` contains the exact complete passage bytes, all three CRLF pairs, its indexed hash, native locator, and an explicit `Source status: **changed**` metadata line. Its SHA-256 is `b20241bb645ad73ceb5934bfdc08e5fb7a48fe184ca031ec96763367e566ee91`.

The frozen evaluator read the report with `Path.read_text`, which performs universal newline translation, and then searched that LF-normalized string for the unchanged CRLF-containing JSON passage. That raw substring comparison failed. Reading the actual report bytes proves that no passage content was omitted. This is an evaluator defect, not a product repair.

`adjudicate_newlines.py` preserves the frozen evaluator and product files. It creates a byte-verified execution copy of the saved delivery, uses byte-identical real corpus copies, and reruns the entire frozen freshness sequence with only the report-read newline behavior corrected. It also explicitly checks status metadata rather than counting a status word inside research prose. The clean-index and full freshness cases both passed, including changed-byte detection despite preserved size/mtime, changed and missing search/show/export, restoration to current, and changed-source re-indexing with refreshed text/hash.

The original failure had interrupted missing-source and later re-index checks; these receive credit only from that supplemental execution, not from an assumption about the earlier successful status command. Snapshot files, original corpus bytes, original result JSON, original report, and frozen evaluator were checked unchanged.

## Delivery and effort

`FOUNDATION-DELIVERY-REVIEW.md` records independent source inspection and five documented CLI commands. It found generic parsing/search, standard-library dependencies, 87 passages preserving every nonblank native unit, all 81 Word table paragraphs, and correct exported links/status annotations. Historical builder logs are internally consistent but remain builder-authored evidence; the review does not claim to independently prove their past execution.

Manual delivery review ran from `2026-10-23` to `2026-10-23` (recorded on 2026-10-23). Its five-command/check execution took 4.264 seconds. The supplemental freshness execution ran from `2026-10-23` to `2026-10-23` and took 1.984 measured seconds; its 16 real CLI subprocess records are in `foundation-first-adjudication.json`. These are reviewer/evaluation costs, not builder repair time. The broader diagnosis and adjudicator-authoring work is additional coordinator overhead; its complete start was not independently clocked, so no precise total is invented. The first explicit coordinator clock during this review was `2026-10-23`.

A reviewer shell invocation initially could not resolve `python`; using the documented installed-interpreter path succeeded. This was an evaluation environment issue and is disclosed separately from product behavior.

Reproducible artifacts:

- `foundation-first.json`: preserved original automated result.
- `foundation-first-snapshot.json` and `snapshots/foundation-first`: frozen delivery identity and files.
- `adjudicate_newlines.py` and `foundation-first-adjudication.json`: diagnosis, unchanged-artifact checks, supplemental command transcript, outcomes, and timings.
- `FOUNDATION-DELIVERY-REVIEW.md` and its linked runtime records: manual review, command evidence, and remaining limits.
