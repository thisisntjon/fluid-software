# Research Navigator

Offline Python 3.11+ tool for searching the supplied research documents. No dependencies or installation required. Run from this directory; all commands accept `--help` and `--json`. Paths may be absolute or relative and may contain spaces.

```powershell
python navigator.py index --source-dir corpus --index "runtime/research index.json" --json
python navigator.py search --index "runtime/research index.json" --query "architectural mismatch" --limit 10 --json
python navigator.py show --index "runtime/research index.json" --id PASSAGE_ID --json
python navigator.py export --index "runtime/research index.json" --query "monkey bars" --limit 10 --output "runtime/reports/monkey bars.md"
python navigator.py status --index "runtime/research index.json" --json
```

Replace `PASSAGE_ID` with an ID from search. If `python` is unavailable on this machine, use PowerShell's `& "local-path"` in its place. Missing index/report parent folders are created.

The actual corpus comprises `deep-research-report.md`, `junglegym.md`, `resuse.txt`, and `Hierarchical Scaffolding in AI Development.docx`. Indexing recursively reads supported extensions and retains source-relative names and SHA-256 hashes of original bytes. Unsupported extensions are ignored. A decoding or parsing error aborts the entire rebuild, preserving the previous index. Saving uses a temporary file and atomic replacement. Outputs cannot overwrite an indexed source or, for export, the index itself.

Search is a case-insensitive **literal phrase** match over each passage, with Unicode whitespace collapsed to ordinary spaces. Markdown punctuation remains literal; this is neither semantic nor fuzzy search. Results follow deterministic source filename and native-location order. A positive limit caps matching passages; an empty query or invalid limit is an error. No matches is a successful empty result. `show` returns the complete stored passage. IDs remain stable when source bytes, relative names, and parsing behavior are unchanged.

Passages group adjacent blocks under the same heading, usually up to 3,000 characters. Long paragraphs and Markdown tables remain complete, so some passages are larger. Plain text groups native lines; Markdown uses ATX (`#` through `######`) headings, ignoring heading syntax inside fenced code. UTF-8 BOMs are removed for text display. Internal source line endings and Unicode are retained; a passage's final line terminator is omitted. Locators use inclusive, 1-based source lines.

DOCX parsing reads `word/document.xml` body paragraphs in XML order, including every paragraph in tables. Empty paragraphs count toward native ordinals. Text runs, tabs, and explicit line breaks are retained; paragraphs are joined with newlines. Heading styles, inherited styles, and outline levels provide heading context. Paragraph locations are inclusive and 1-based. Embedded images, headers, footers, comments, footnotes, formatting, automatic numbering labels, and rendered page layout are not extracted. Tables are searchable paragraph text rather than a reconstruction of their visual grid. Markdown setext headings and rendered inline markup are not interpreted.

Every read operation hashes the current sources. `current` means bytes match the indexed hash; `changed` means they differ; `missing` means the indexed path no longer holds a file. Unreadable files produce an error. Old indexed text remains searchable and inspectable, with its current status attached. Re-run `index` to refresh snapshots. Status covers indexed sources, not newly added files; rebuild to discover additions. Freshness is checked at command time and cannot prevent a file changing immediately afterward.

Export contains the literal query, complete source text in fenced blocks, headings, native locations, indexed hashes, and status. Correctly encoded absolute `file:` links continue to point to the originals if the report moves to another directory on this machine; the sources themselves must stay at their indexed locations. Some Markdown viewers restrict local-file links; open the report in a local viewer that permits them. Word links open the file, while paragraph ranges remain printed provenance. Research claims are reproduced without verification or endorsement.

Responsibilities: `nav/parsing.py` owns extraction and stable identities; `nav/storage.py` owns atomic persistence and freshness; `nav/query.py` owns search/show; `nav/cli.py` owns command handling and report formatting. The index is an inspectable JSON snapshot, not a database. `BUILD_LOG.md` and `evidence/` record actual connected verification.
