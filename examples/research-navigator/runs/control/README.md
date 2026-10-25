# Research Navigator

An offline command-line navigator for the four actual documents in `corpus/`. It retrieves literal source passages, keeps their provenance, and checks whether current file bytes still match the indexed evidence. It does not endorse or independently verify the documents' claims.

Requires Python 3.11 or newer; all dependencies are in the standard library. Run commands from this directory. No installation, network, accounts, or external services are needed.

```powershell
python navigator.py index --source-dir corpus --index "runtime/research index.json" --json
python navigator.py search --index "runtime/research index.json" --query "architectural mismatch" --limit 10 --json
python navigator.py status --index "runtime/research index.json" --json
python navigator.py export --index "runtime/research index.json" --query "architectural mismatch" --limit 10 --output "runtime/reports/evidence.md"
```

Copy a returned passage ID into `show`, or use PowerShell to select one directly:

```powershell
$results = python navigator.py search --index "runtime/research index.json" --query "architectural mismatch" --limit 1 --json | ConvertFrom-Json
python navigator.py show --index "runtime/research index.json" --id $results.matches[0].id --json
```

If `python` is not on PATH, the verified interpreter on this machine is:

```powershell
& 'local-path' navigator.py --help
```

Every command has `--help`. Omit `--json` for readable terminal output. All output uses UTF-8. With `--json`, success emits exactly one JSON value on stdout; errors emit a diagnostic to stderr and exit nonzero. JSON is also available for `export`.

## Retrieval and provenance

- Source discovery is recursive for `.md`, `.txt`, and `.docx`, case-insensitively. Relative source names retain subdirectories. Unsupported files are listed as `ignored` in index/status output; directory symlinks are not traversed.
- Markdown/text decode as UTF-8, accepting a BOM. Newlines become `\n`; other text, Unicode and source Markdown are preserved. Locations are inclusive, 1-based source line numbers. Long lines can span multiple passages with the same line locator.
- DOCX reads body `w:p` elements in document order, including empty and table paragraphs. Empty paragraphs count toward inclusive, 1-based paragraph ordinals. Text runs, hyperlinks, tabs and line breaks are retained. Table paragraphs become successive text lines, rather than a visual grid. Word heading styles, inherited styles, and paragraph outline levels supply heading context.
- Markdown ATX and Setext headings supply containing heading paths. Fenced code does not create headings. Heading context comes from the first content in the returned passage; a phrase spanning sections can return text from more than one heading.
- Passages follow heading sections and nearby paragraph, line, or sentence boundaries, with a target around 2,400 characters. Every source remains separately navigable. Search scans complete indexed documents and joins adjacent passages when needed, so a phrase crossing a stored boundary is still found and `show` can retrieve that same complete range.
- Queries use Unicode case folding and collapsed whitespace. Ordinary spaces match line breaks. Everything else is literal, including punctuation and Markdown markup; there is no stemming, semantic matching, regex syntax, or relevance scoring. Results are deterministic by source-relative filename, then position. Repeated occurrences within the same selected passage return that passage once. A positive limit caps passages, not raw occurrences.
- IDs depend on source-relative name, original file SHA-256, and passage character range. Re-indexing unchanged bytes with this parser preserves IDs. Changed source bytes produce new IDs; old IDs remain available in the old index until replacement.

## Freshness, reports, and persistence

`status` hashes every indexed source's current bytes. `search`, `show`, and `export` hash each returned source and expose `current`, `changed`, or `missing`. They keep returning indexed text if its source has changed or disappeared. An unreadable source produces an error, because its freshness cannot honestly be classified. Freshness describes the observation at command execution time; no watcher runs between commands.

Re-run `index` to refresh content and hashes. New source files are picked up during re-indexing; `status` describes the sources already in the index. The index is a portable JSON artifact containing an absolute source-root path: moving the index alone works on the same machine, but moving source files requires re-indexing at their new root.

Index and report writes create missing parent directories, write a temporary file in the destination directory, then atomically replace the destination. Parsing must succeed for every supported source before an index is replaced. The program rejects output paths that would overwrite an indexed source; export also protects the index itself.

Reports contain the literal query, selected source text in fenced blocks, source links, native locators, heading context, indexed hashes, and source status. Absolute `file:` links are URI encoded (including spaces), so moving the report to another directory preserves its source links. Browser or Markdown-viewer policy can affect whether local file links are clickable; the links identify the original local files, not copies packaged with the report.

## Limits

Embedded images, image-only formulas, headers, footers, comments, footnotes, endnotes and unsupported extensions are not indexed. DOCX extraction preserves text, not Word layout, list numbering generated by Word, or rich formatting. It reads standard WordprocessingML `w:t` text and does not render fields, OCR images, or reconstruct equations encoded outside text runs. Markdown is searched as authored source text, not rendered HTML. The application loads documents and their JSON index into memory and is intended for a local research corpus, not a large search service.

## Implementation and actual verification

`navigator.py` handles the public CLI; `nav_sources.py` parses and partitions sources; `nav_index.py` handles persistence and freshness; `nav_search.py` implements matching, complete passage reconstruction and export.

The supplied corpus produced **4 sources and 92 base passages**. The connected verification executed all commands, checked native locations and Word table content, repeated indexing for stable IDs, relocated a report, and changed/moved/truncated private copies of actual files to check freshness and failed-rebuild preservation. Original corpus hashes stayed unchanged. Verification does not assert that source research claims are true.

```powershell
python verify_real.py
```

The latest run completed 41 real CLI invocations successfully, including expected error cases; its 303 assertions are builder checks, not an independent evaluation score. See `runtime/verification/result.json` for checks, `runtime/verification/commands.json` for exact argument lists and exits, and numbered stdout files for real outputs. The earlier failed verification assumption is preserved in `first-attempt-result.json` and documented in `BUILD_LOG.md`. All runtime artifacts stay under `runtime/`.
