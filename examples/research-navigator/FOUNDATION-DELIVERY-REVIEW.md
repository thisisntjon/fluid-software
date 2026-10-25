# Independent manual delivery review: foundation first delivery

**Verdict: delivery PASS on the unchanged first-delivery snapshot.** This resolves the frozen evaluator's `delivery` manual-review blocker. It does not alter `foundation-first.json` or decide the separately adjudicated freshness row.

Reviewed `snapshots/foundation-first` against `foundation-first-snapshot.json`. The snapshot was delivered at 2026-10-23. All 37 manifest-listed snapshot file hashes matched before and after the review. No snapshot file, product source, original document, or first-pass evaluation result was changed. No control-arm material was read.

Review began at the first recorded shell clock, `2026-10-23`. End time and total observed review interval are recorded in `manual-foundation-review-2026-10-23/review-timing.json`. The independent public-command run began `2026-10-23` and ended `2026-10-23` (4.264 seconds, including source/hash/import checks). Review and adjudication time is separate from the builder's delivery time.

## Commands and observed result

The snapshot intentionally omits the input corpus. Following coordinator direction, I verified the four original root documents against the snapshot manifest's corpus hashes and copied them into the separate review runtime. I ran the frozen snapshot entry point with its Python module path unchanged and `PYTHONDONTWRITEBYTECODE=1` / `-B` to avoid writing bytecode in the snapshot. Runtime outputs stayed in `manual-foundation-review-2026-10-23`.

I reproduced all five README workflow commands, changing only the entry-point location and using the private runtime's relative input/output paths:

1. Index `corpus` into `runtime/research index.json`.
2. Search `architectural mismatch` with limit 10.
3. Show an actual ID returned by that search.
4. Export `monkey bars` with limit 10 to `runtime/reports/monkey bars.md`.
5. Query current source status.

All five commands exited 0 with empty stderr. Relative paths containing spaces worked, missing output directories were created, search returned actual passages, and `show` reproduced the chosen search result. Current status was correct for all four files. The report contained ten complete selected source passages, source hashes, native locations, and ten explicit `Source status: **current**` annotations. Every source link resolved to its intended actual document from the report directory. Reading report bytes directly confirmed that complete source passage text, including original internal line endings, was preserved.

The first reviewer shell attempt could not resolve `python` from PATH. The README explicitly documents this possibility and gives the installed interpreter path. Using that documented fallback succeeded; no product change was required. The resulting public command argv lists record the actual installed Python executable.

Complete subprocess argv, cwd, timestamps, exit codes, stdout and stderr are preserved in `manual-foundation-review-2026-10-23/commands.jsonl` and `results.json`. The review script is `review_commands.py` in the same directory.

## Source and architecture review

Read the delivered entry point and all five product modules. The implementation is generic for supported documents:

- `nav/parsing.py` discovers files by supported extension, reads original bytes, derives SHA-256 values, extracts native text/Word XML, groups passages by real heading context and size, and derives stable IDs from source identity and actual content. It contains no special-case corpus filenames or expected query answers.
- `nav/storage.py` validates persisted records, writes via a temporary file plus atomic replacement, prevents overwriting indexed sources, and computes freshness by reading current source bytes. A rebuild parses before replacing the existing index.
- `nav/query.py` performs normalized-whitespace, case-insensitive literal matching over persisted passage text and returns real stored records. It contains no canned passages or search answers.
- `nav/cli.py` implements the documented public commands, emits JSON through `json.dumps`, routes errors to stderr, and creates complete fenced source-text reports with explicit source status and file URIs. `navigator.py` is the entry point; `contracts.py` holds the shared error type and public integration description.

The responsibilities form a coherent small program and match the README. Static AST inspection found only Python standard-library imports and the project's own `nav` modules: `argparse`, `hashlib`, `io`, `json`, `nav`, `os`, `pathlib`, `re`, `sys`, `tempfile`, `xml`, and `zipfile`. The product code performs no network or external model calls. No installation was needed for the independent run.

This review is a bounded source review of the delivered application, not proof of every possible behavior or the builder's prior browsing/actions.

## Independent provenance and coverage checks

The fresh index contained 87 passages: 36 from `deep-research-report.md`, 29 from the DOCX, 19 from `junglegym.md`, and three from `resuse.txt`. Independent raw-byte/XML extraction established:

- Every passage exactly equalled its stated native source slice, preserving Unicode and source hashes.
- Every nonblank source line or Word body paragraph was covered exactly once.
- The Word document contained 223 body paragraphs; all 81 table paragraphs were represented by the relevant native ranges.
- The dense text file's long first line was retained completely; coverage did not rely only on its short line-16 anchor.
- All four original corpus hashes and all four private copied corpus hashes remained unchanged.

These checks substantiate the current delivered result, including the builder's broad coverage claim, independently of its self-authored observations.

## Documentation and historical claims

The README includes copyable actual-corpus commands, the placeholder-ID substitution, an interpreter fallback, public behavior, extraction exclusions, passage granularity, path behavior, freshness semantics, report-link limitations, and module responsibilities. Its stated limits are candid: literal passage-local search; ATX Markdown headings; body/table Word text without images, headers, footers, comments, footnotes, automatic numbering, or rendered layout; additions requiring re-indexing; and untested GUI file-link policy. No GUI opening is claimed.

`BUILD_LOG.md`, `DELIVERY.json`, `runtime/verification/commands.json`, `runtime/verification/observations.json`, and `check_actual.py` are mutually consistent. The command log contains 40 subprocess records with ten nonzero negative-path results, exactly matching `DELIVERY.json`; those failures contain stderr diagnostics and zero stdout bytes. The recorded verification program exercises real source files and private copies, not a fabricated navigator or seeded answer index.

Those historical logs are builder-authored evidence, not independent telemetry proving every past execution. The intermediate 85-to-87 passage refinement, absence of past unexpected failures, and historical workflow/tool-access statements remain self-reported where no independent transcript is available. The five README commands, current source coverage, static dependencies, report fidelity, and file integrity were independently checked here. Freshness, restored-source behavior, and failed-rebuild obligations are assessed separately by the frozen evaluation and supplemental freshness adjudication; this delivery review does not borrow credit from a merely green status string.

## Case disposition

| Item | Disposition |
| --- | --- |
| Frozen automated `delivery` row | Preserved as `blocked` in the original JSON. |
| Manual delivery adjudication | PASS: documented workflow runs; source is generic; current result and log claims are appropriately qualified; limits and responsibilities are clear. |
| Product edits or repair opportunity used | None. |
| Review runtime interpreter correction | Used the README's documented absolute Python fallback after PATH lookup failed. |
| Frozen automated `freshness` row | Outside this review's verdict; preserved for separate supplemental adjudication. |

No conclusion about comparative method superiority follows from this delivery verdict.
