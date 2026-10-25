# Frame module build

2026-10-23. Implemented `fluid/frame.py` against `docs/FOUNDATION-CONTRACT.md` v1, including the subsequently agreed optional module parent hierarchy and manifest mapping.

- `plan_frame` reads literal/copied native artifacts, checks source hash pins, preflights every destination and parent, and prepares stable initial context, project identity, manifest, and state. Artifact/file collisions prevent application.
- `apply_frame` rechecks the complete plan, creates missing files through complete temporary bytes followed by an exclusive hard link, skips identical bytes, and preserves matching-project runtime state. No differing existing file is overwritten. Publication is atomic per file, not a project-wide transaction; an interruption can be resumed. Filesystems must support hard links.
- `render_context` supplies the whole capability map, ancestor responsibilities, the selected contract, direct semantic/build neighbors, current source/evidence hash pointers, and declared runtime status. Derived freshness remains the state module's responsibility and is labeled accordingly. Recorded state never grants authority.

Validation so far: Python 3.11 AST parse and direct import of all three public functions succeeded. The shell's `python` alias is unavailable; used `local-path` with `-B` for import. No fabricated brief or fixture was created. Behavioral verification awaits the actual comparison brief and will be recorded below or in the integrated phase check.

Agreed v1 limit: after native implementation changes starter bytes, rerunning the original frame reports a safe conflict rather than regenerating over work. Live context uses runtime records; generated documents remain the initial frame. No migration or updater was added.
