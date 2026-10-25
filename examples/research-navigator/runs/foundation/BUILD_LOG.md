# Build log

- started_at: 2026-10-23 (actual clock read)
- Assignment: foundation arm only; stdlib Python, no network or installs, immutable corpus, no subagents; initial delivery cap a bounded initial pass.
- Initial command read the frozen prompt and actual UTC clock. Next inspected TASK_BRIEF.md, FRAME.md, nav/contracts.py, and assigned file inventory.

## Implementation and observations

- Read the assigned FRAME.md, nav/contracts.py, unfinished native modules, and actual corpus. Executed the allowed Fluid status, per-module context, and claim commands with actor navigator-builder. All four modules were initially ready; no subagents were used.
- Actual source inspection: Markdown files have 1,048 and 177 native lines; resuse.txt has 17 lines, including a 6,768-character first line. The Word document has 223 body paragraphs and three tables.
- Implemented parsing, storage, query, and CLI in their owned paths; kept the frozen function signatures and index schema. Added atomic_write_text/protect_sources storage helpers used by CLI; no consumer contract break or .fluid/project.json change was needed.
- First parser probe returned 85 passages with resuse.txt in one 10,480-character passage. This usability observation led to line-grouping for plain text. Final index has 87 passages: 36 Markdown report, 29 Word, 19 junglegym, 3 resuse. Stable IDs passed in both parser and CLI rebuild probes.
- Actual initial product commands: `python navigator.py index --source-dir corpus --index "runtime/research index.json" --json`; search for `Architectural Dimension` with limit 1; export `monkey bars` with limit 10 to `runtime/reports/monkey bars.md`; status on that index. These succeeded. The Word table search returned paragraphs 14-30 with the containing heading chain.
- Wrote and ran `python check_actual.py` using `local-path`. The first connected regression run passed. Its 40 subprocess commands are recorded verbatim in runtime/verification/commands.json. Observations are recorded in runtime/verification/observations.json.
- Checked all five public commands, every help path, JSON stdout purity, absolute/relative paths with spaces, native source-slice equality for every passage, complete nonblank-line/paragraph coverage, all 81 Word table paragraphs, source hashes, stable IDs, mixed case, whitespace across table paragraph boundaries, literal Markdown punctuation, deterministic positive limit, no matches, and show equality.
- Copied actual inputs only within runtime/verification. A same-size/same-mtime byte edit and a missing Word file were detected as changed/missing; indexed text remained available through search/show/export. A corrupted private Word copy caused a failed rebuild without changing the old index. Restoring the document and rebuilding refreshed content/hashes. Originals were never modified, and all four original hashes were checked unchanged.
- Export reports preserve source text, provenance, and freshness. Parsed encoded absolute Word file links still resolved after relocating the report to another runtime subdirectory. Inspected the generated Markdown directly; did not open a GUI viewer.

## Observed failures and corrections

No unexpected runtime exception or connected regression failure occurred. Ten expected negative-path commands failed: blank query; zero, negative, and noninteger limits; unknown passage ID; missing index; missing source directory; exporting over the index; exporting over an original source; and rebuilding from a truncated private DOCX. Each produced nonzero exit, stderr diagnostic, and empty stdout. The plain-text segmentation correction above preceded connected verification.

## Foundation continuation observation

The persisted frame and contracts helped establish the complete four-part product, clear ownership, return-value agreement, and provider/consumer delivery order in this fresh session. The generated module scopes repeated the frame and did not supply parsing algorithms, passage granularity, validation details, or an actual product-flow oracle; those still required reading real files and making implementation decisions. There was some repeated context output but no blocker. The skeletons correctly remained visibly unfinished until implemented. Readiness was useful work tracking, not proof of behavior. Provider deliveries are recorded before consumer deliveries, with immutable evidence files; no self-acceptance is requested or recorded.

## Remaining limits

- Markdown ATX headings only; source markup remains literal. DOCX text includes body/table paragraphs, tabs, and breaks but not rendered formatting, automatic numbering, embedded images, headers, footers, comments, or footnotes.
- Matches are literal and passage-local; no semantic relevance ranking. Long source paragraphs remain long.
- Status checks indexed files at command time; additions require re-indexing, and subsequent external file changes can occur after a check.
- Export links are absolute file URIs for this machine. Moving the report works; moving the original sources requires rebuilding. Markdown viewer file-link policy was not tested.
- No network, installs, generated domain documents, mocks, other-arm access, or self-acceptance. Tokens and monetary cost are unknown.

## Initial delivery

- completed_at: 2026-10-23 (actual UTC clock read).
- Executed provider deliveries parsing, storage, then consumer deliveries query, cli, all as navigator-builder with immutable evidence files.
- Final allowed command: fluid.py verify TARGET --json. Observed four delivered, zero accepted, zero stale, no blockers, and no integrity issues. Frame/project/contract files remain unchanged.
- DELIVERY.json records actual commands, expected failures, limits, and outcome. First delivery is frozen pending explicit repair feedback.
