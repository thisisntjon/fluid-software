# Control first delivery: independent manual delivery review

Verdict: **delivery review passes within its scope**. The README workflow runs, production code uses generic parsing and retrieval with standard-library dependencies, complete actual source text is retained, and the recorded builder verification claims are substantially supported by delivered receipts. This does **not** waive or decide the separately reported Markdown heading-context failure, and is not an overall acceptance of every capability.

Reviewed the frozen `snapshots/control-first` delivery, `control-first-snapshot.json`, `control-first.json`, and the shared brief/protocol. No live arm files or other arm implementation were inspected. The original four source files were read only after checking their hashes against the frozen manifest; all execution outputs went into `manual-control-review-2026-10-23`.

## Recorded time and immutable evidence

- Manual review started at the observed clock: `2026-10-23`.
- This review concluded at `2026-10-23`; observed review interval: `recorded on 2026-10-23`.
- The actual verification script ran `2026-10-23` through `2026-10-23`, taking `1.563 seconds` for 13 real CLI processes and independent source/artifact checks. This is execution time, not the entire review effort.
- Checked all **65 snapshot file hashes** before and after execution. Snapshot, original corpus, private corpus copies, and original evaluator result remained unchanged. No product changes or builder feedback were made.
- Reproducible coordinator script: [review.py](manual-control-review-2026-10-23/review.py).
- Exact argv, cwd, UTC timestamps, stdout, stderr, and return codes: [commands.json](manual-control-review-2026-10-23/commands.json).
- Independent observations: [observations.json](manual-control-review-2026-10-23/observations.json).

## Delivery findings

| Check | Finding |
| --- | --- |
| README workflow | PASS. The documented `architectural mismatch` index/search/status/export workflow returned four sources, 92 base passages, and eight matching passages. The documented one-result search followed by `show` returned the same complete passage and metadata. All six help invocations worked. |
| Relative paths and spaces | PASS for exercised inputs/outputs. Commands ran from the private review directory with relative `corpus`, `runtime/research index.json`, and `runtime/reports/evidence.md` paths; the immutable entry point was given by absolute snapshot path. The README's explicitly documented Python interpreter fallback was used. |
| Source retention | PASS. Independently compared complete indexed document text with the four actual source files after the disclosed newline normalization and native Word extraction. Every stored range collectively covers that complete text. Word coverage included all 223 body paragraphs and all 81 table paragraphs. |
| Dense text | PASS. The original text file's first line has 6,768 characters. A phrase selected directly from that line was retrieved through the CLI with a locator covering line 1. The full indexed source text also matched the original, so this did not merely check one isolated anchor. |
| Evidence export | PASS for the README query. The report contains all eight selected complete passage texts and hashes. Each has an explicit `Source status: **current**` metadata line. Copied the report into a different directory and resolved all eight encoded absolute file links to the matching original private source files; their bytes match the frozen corpus hashes. |
| Generic implementation | PASS from source inspection. Production modules enumerate source files, parse text/XML, construct offsets/ranges, and perform literal normalized string matching. No branches or constants for the supplied filenames, frozen anchor phrases, or precomputed query answers were found. The CLI also retrieved a newly selected phrase from the real long text line. This is evidence from inspected code and observed behavior, not a universal proof against every conceivable hidden behavior. |
| Dependencies and responsibilities | PASS. All production imports resolve to Python standard-library modules or the three local modules. CLI, source parsing, persistence/freshness, and retrieval/export responsibilities are separated. No installation, network client, model call, or runtime service is used in the inspected production path. |
| Documentation and log disclosure | PASS with the evidence limits below. README explains literal matching, normalization, source-relative provenance, heading/Word limitations, in-memory storage, absolute source roots, and file-viewer limitations. Build log distinguishes actual commands, expected errors, corrections, unavailable cost data, and builder checks from independent evaluation. |
| Markdown heading-context correctness | **Adjudicated separately.** The coordinating reviewer reports a pass in `control-first-adjudication.json`, supported by actual-source CommonMark parsing and four supplemental CLI calls. This delivery review does not replace or independently repeat that finding; its own scope is documentation, generic implementation, source retention, and the documented workflow. |

## Code examined

Read the four complete production modules. `nav_sources.py` decodes original bytes and parses Word body paragraphs, including table paragraphs; `nav_index.py` discovers actual files, parses all supported sources before atomic index replacement, and hashes current bytes for freshness; `nav_search.py` maps normalized matches back to actual character ranges and formats source-backed reports; `navigator.py` supplies the public CLI and diagnostics. Source-specific terms occur in the builder's verification material as real-source checks, not as production lookup answers.

The generic implementation finding does not depend on the heading adjudication: an ordinary parser defect could exist in generic code. Heading-context correctness remains a distinct capability verdict with its own evidence record.

## Builder claim reconciliation and limits

The final saved builder receipts contain **41 actual CLI argument lists**, **303 named builder assertions**, and **10 expected nonzero error exits**, matching README/build-log counts. Every final numbered stdout artifact exists; expected errors have stderr and empty stdout. The documented first failed `CodePlan` cross-document assumption is preserved in `first-attempt-result.json` and its two command receipts; the final query is `agent`. The code does not special-case either query.

The first-attempt command receipts point to numbered stdout paths reused by the final run. Consequently, the first failure's command list and error description are preserved, but its original numbered stdout files are not independently preserved. The build log promises the first command receipts and failure, which exist; this limitation should remain visible in any detailed audit.

Interactive inspection commands and the initial cp1252 exception are summarized in the builder log, with a clear statement that its angle-bracket descriptions are not literal executable commands. Those historical actions are not independently established by the stored CLI receipts. The log also discloses a small loaded-index validation change after the 41-command suite and records later `status`/export checks rather than pretending to have rerun the entire suite. The present 13-command review exercises the delivered bytes.

No renderer/browser was opened to click a `file:` URI; link decoding, target identity, existence, and byte hashes were checked directly. No claim is made about large-corpus performance, every Markdown extension, every malformed input, or the truth of the retrieved research claims. No score is inferred from the number of builder assertions.

The original automatic result remains untouched. This document supplies the previously blocked manual **delivery** evidence only; the separately reported heading-context case must retain its own recorded adjudication or repair outcome.
