# Parsing delivery evidence

Commands actually run from the assigned arm:

- Python inline inspection of the actual UTF-8 text files and `word/document.xml`/`word/styles.xml` via stdlib `zipfile` and `ElementTree`.
- `python -c "from nav.parsing import parse_corpus; ..."` on `corpus/` twice: deterministic IDs and the actual table phrase `Architectural Dimension` were found.
- `python navigator.py index --source-dir corpus --index "runtime/research index.json" --json`.
- `python check_actual.py` (actual executable: `local-path`).

Observed connected result: four real sources; 87 passages (deep-research-report.md 36, Word 29, junglegym.md 19, resuse.txt 3). The independent source-slice traversal in `check_actual.py` verified every passage text against its exact indexed native range and original file hash. Every nonblank text line and Word body paragraph is covered exactly once. The actual Word document has 223 paragraphs, including 81 table paragraphs across three tables; all table text is covered. Native paragraph positions include empty paragraphs. Re-indexing unchanged bytes preserves every passage ID.

Initial observation/correction: paragraph-only plain-text chunking left resuse.txt as one 10,480-character passage. The parser now groups its native lines up to the target size and preserves its single 6,768-character first line whole; the document has three passages. There was no failing regression assertion.

Detailed public command records: `runtime/verification/commands.json`; complete checks: `check_actual.py`. Original source hashes were unchanged after verification. No shared contract revision was required. Limits: ATX Markdown headings only; no rendered DOCX numbering, page layout, image, header, footer, footnote, or comment extraction. Table text is paragraph text, not rendered table layout.
