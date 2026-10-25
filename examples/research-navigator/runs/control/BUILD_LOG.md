# Research Navigator build log

- started_at: 2026-10-23 (read from the actual clock)
- Scope: assigned control arm only; Python 3.11 standard library; original corpus remains unchanged.
- Initial commands: `Get-Content -Raw examples/research-navigator/PROMPT-control.md`; `Get-Content -Raw TASK_BRIEF.md`; `rg --files` from the assigned arm.
- Implementation plan: inspect real document structure, implement lossless native-location parsers, atomic JSON index persistence, literal whitespace-normalized retrieval and freshness reporting, then exercise every public command against actual sources.
- Initial uncertainties: passage sizes and Word heading/table structure will be selected after inspecting the supplied content.

## Inspection and implementation

- Inspected only the assigned brief and the actual assigned corpus. Used the assigned Python executable with `-c` to read source excerpts, line lengths, Word styles, and all `w:p` ordinals. The Word file contains 223 body paragraphs, including empties, and 3 tables; its first table starts at paragraph 17. The long plain-text opening line is 6,768 characters, so fixed line-only partitioning would make it awkward to navigate.
- Initial inspection command failed with `UnicodeEncodeError` under the default Windows cp1252 stdout encoding when printing a private-use citation glyph. Re-ran inspection with Python `-X utf8`. The delivered CLI explicitly configures stdout and stderr for UTF-8.
- Implemented `nav_sources.py`, `nav_index.py`, `nav_search.py`, and `navigator.py` using only the standard library. Chose complete-document matching with reversible character offsets and adjacent-range joining to prevent passage boundaries from hiding a literal query. Native provenance is derived from unnormalized text; whitespace normalization affects matching only.
- Persistence uses a temporary file in the target directory and `os.replace` after parsing all sources. Sources are never modified by normal commands. Freshness hashes bytes and retains indexed text even when the current source is stale.

## Commands actually run

The interpreter for all Python commands was `local-path`.

```text
python -X utf8 -c <actual-source excerpt inspection>
python -X utf8 -c <actual-source line lengths, Word paragraph ordinals and styles>
python navigator.py index --source-dir corpus --index "runtime/working index.json" --json
python navigator.py search --index "runtime/working index.json" --query "architectural mismatch" --limit 3 --json
python verify_real.py
python verify_real.py
Get-Content -TotalCount 50 "runtime/verification/reports with spaces/evidence.md"
python navigator.py status --index "runtime/working index.json" --json
python navigator.py export --index "runtime/working index.json" --query "architectural mismatch" --limit 10 --output "runtime/reports/architectural-mismatch.md"
```

The inline inspection scripts and outputs were executed in the build session; the angle-bracket descriptions above are summaries, not copyable literal shell commands. Exact connected CLI argument lists, exit codes, stderr, and stdout-file paths are preserved in `runtime/verification/commands.json`. The first verification attempt's two command receipts and failure are preserved in `first-attempt-commands.json` and `first-attempt-result.json`.

## Observed failures and corrections

1. Source inspection initially hit the cp1252 Unicode error described above. Corrected the inspection invocation and made UTF-8 explicit in product output.
2. The first connected verification incorrectly assumed `CodePlan` appeared in all four documents. The search result disproved that assumption. Changed the cross-document verification query to `agent`, which the actual sources share; did not change retrieval behavior to fit the assumption.
3. The final run intentionally supplied empty/whitespace queries, invalid limits, an unknown ID, a nonexistent index, source-overwriting output paths, and a truncated private copy of the actual DOCX. These produced expected nonzero exits, concise stderr and no stdout. The failed rebuild preserved the previous index byte-for-byte and its indexed passages remained usable.

## Observed verification outcome

- Final `verify_real.py`: passed, 41 connected CLI commands, 303 builder assertions. This count is a verification receipt, not an independent performance score.
- Indexed all four original files with independently checked SHA-256 hashes; 92 base passages.
- Retrieved source content across Markdown, text, and Word; checked Markdown/text line spans, Word table text, paragraph ordinals counting empty paragraphs, and Word heading context.
- `show` reproduced complete search passages, including a phrase crossing an internal passage boundary. Case and whitespace normalization worked across actual source line breaks. Limits, empty results, deterministic order, and repeated-index ID stability passed.
- Exported real source text and hashes; copied the report to a different directory and resolved its encoded absolute source links. Inspected the generated Markdown's opening passages directly.
- A private text copy changed bytes while keeping file size and nanosecond mtime unchanged; status, search and show marked it changed while preserving old text. A moved private Word copy was marked missing and remained inspectable. Export visibly marked both stale states. Re-index refreshed modified bytes and hashes.
- Original corpus byte hashes were unchanged after verification. No generated documents, fixtures, mocks, network calls, installs, or subagents were used.
- Final small review tightened loaded-index timestamp and ignored-file metadata validation. Re-ran `status` successfully on the actual index after that change, and exercised the public plain-output export command successfully (8 real matching passages, limit 10).

## Remaining limits

- No independent evaluator result is claimed; only the actual connected builder checks above.
- No OCR or document layout rendering; Word images, headers, footers and non-body ancillary parts are intentionally excluded. Advanced Word field/equation rendering and rich formatting are not implemented.
- Markdown is literal source text. Queries do not remove inline formatting markers or perform semantic search. Heading recognition handles ordinary ATX/Setext headings and fenced code, not every extension.
- In-memory JSON storage suits this corpus; no large-corpus performance claim. Source-root paths are absolute, so relocating sources requires re-indexing. Freshness is an observation at command time and does not lock files against concurrent external changes.
- Token use and cost are unknown.
