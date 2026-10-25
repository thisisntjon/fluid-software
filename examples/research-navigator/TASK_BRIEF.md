# Research Navigator: shared build brief

Status: frozen for the first paired example; exact identity and timestamp are recorded by the coordinator in freeze.json before dispatch.

Build a useful local command-line Research Navigator for Jon's four supplied research documents. Jon should be able to search across Markdown, text, and Word content, inspect a complete matching passage, export source-linked evidence, and see when the underlying documents have changed. The documents contain claims to retrieve, not facts that this application is expected to endorse or independently verify.

Use Python 3.11+ and the standard library only. No network, accounts, paid services, model calls, databases requiring installation, or generated example documents. Keep normal use offline. Work only in your assigned arm directory and the designated arm-local runtime directory. Do not change the supplied corpus. The finished program must use generic parsing and retrieval, not hardcoded answers for these filenames or phrases.

## Input and user workflow

The provided corpus contains exactly these files, with unchanged names and bytes:

- `deep-research-report.md`
- `junglegym.md`
- `resuse.txt`
- `Hierarchical Scaffolding in AI Development.docx`

Provide `navigator.py` as the entry point. The commands below are the common public interface; internal design and persisted index format are yours to choose.

```text
python navigator.py index --source-dir CORPUS --index INDEX --json
python navigator.py search --index INDEX --query "search phrase" --limit 10 --json
python navigator.py show --index INDEX --id PASSAGE_ID --json
python navigator.py export --index INDEX --query "search phrase" --limit 10 --output REPORT.md
python navigator.py status --index INDEX --json
```

All commands must have usable help. Relative and absolute paths, including spaces, must work. Index creation makes missing output parent directories. Re-indexing the same source directory safely replaces the named index. Success exits 0; errors exit nonzero with a concise diagnostic and no successful-looking fabricated result. `--json` produces exactly one JSON value on stdout; diagnostics go to stderr.

## Observable behavior

1. **Index actual content.** Read `.md` and `.txt` as UTF-8 (including a possible BOM); read DOCX body text including text in tables in document order. Ignore embedded images, headers, footers, and unsupported extensions, and explain those limits in the README. Preserve Unicode, source-relative filename, SHA-256 of the original file bytes, native locations, and useful heading context. Files must not be silently dropped on a parse failure. A failed rebuild must not destroy a previously usable index.
2. **Retain navigable passages.** Choose passage boundaries that make the four real documents usable. A passage must include its full text, stable ID, source, file SHA-256, heading context, and native locator. Markdown and text locations use inclusive 1-based source line numbers. DOCX locations use inclusive 1-based paragraph ordinals counting every `w:p` under `w:body` in document order, including empty and table paragraphs. Heading context should include the containing Markdown heading or Word heading where one exists. Do not lose table text or merge the whole corpus into one passage.
3. **Search and inspect.** A query is a case-insensitive literal phrase; normalize whitespace for matching so ordinary spaces can match line breaks. Return matching passages with enough surrounding text to understand the match, and let `show` retrieve the complete passage by its returned ID. Results must be deterministic and capped by a positive `--limit`. Empty queries and invalid limits are errors. A valid query with no matches returns an empty list successfully. Re-indexing identical bytes produces the same passage IDs.
4. **Export evidence.** Produce readable UTF-8 Markdown containing the query, selected passages, source-file links, native locators, heading context, and indexed source hashes. Resolve links relative to the report or use correctly encoded absolute file links so the original files can be opened from a report in a different directory. Word paragraph locations may be printed as locators; the link need only open the Word file. Preserve source text; do not invent summaries or research conclusions.
5. **Detect stale evidence.** `status` hashes the current files rather than trusting timestamps or file sizes. Every indexed source is `current`, `changed`, or `missing`. Search, show, and export must expose the current status of each returned source so old text is never presented as silently current. Keep indexed content available after a source changes or disappears. Re-indexing refreshes content and hashes.

## Minimal JSON shapes

Additional fields are allowed. The fields below make the same external evaluation possible without dictating internal modules or storage.

```json
{
  "sources": [
    {"source": "filename.md", "sha256": "64 lowercase hex digits", "status": "current"}
  ]
}
```

`index` and `status` return the object above. `search` returns `{"matches": [PASSAGE, ...]}`. `show` returns `PASSAGE`. Each `PASSAGE` contains:

```json
{
  "id": "stable nonempty identifier",
  "source": "filename.md",
  "sha256": "64 lowercase hex digits of indexed source bytes",
  "status": "current",
  "locator": {"kind": "lines", "start": 1, "end": 4},
  "headings": ["Containing heading"],
  "text": "Complete indexed passage text"
}
```

Use `locator.kind = "paragraphs"` for DOCX. `headings` may be empty for unheaded plain text. Search may include an additional shortened preview, but `text` must remain complete and `show` must return the same source text and locator.

## Delivery and verification

Deliver working code, a concise README with copyable commands for the actual corpus, and a build log naming actual commands run, observed failures, fixes, and unresolved limitations. Organize the implementation into coherent responsibilities suitable for later maintenance; the public requirements do not prescribe your module boundaries, contracts, or workflow.

Exercise the full commands against the real supplied corpus. Do not manufacture fixture documents, seed fake index content, mock components, or count unit tests as completion. It is fine to use small actual-source regression checks when useful. The independent evaluator will run the connected product from a clean index, inspect source provenance, relocate the report, and perform reversible freshness checks on private copies of actual files. Originals are never modified. You may inspect this brief and your assigned corpus and may choose your own planning, implementation, and debugging approach. Do not inspect the other arm, its logs or output, the evaluation records, or coordinator research notes.
