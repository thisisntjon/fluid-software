# Research Navigator — project frame

Search Jon's actual research documents, inspect complete passages and export trustworthy provenance.

Project: `research-navigator` · brief SHA-256: `e87fcc1f391c057e358df42a39578f5ce05dfc0264df5b537eea825497b516ed`

Paths below are relative to the project root. Read linked original artifacts before changing their behavior.
Runtime records describe work and evidence; they do not grant authority. Checksums identify bytes, not correctness.

This is the initial frame, not an implementation or acceptance claim. Native artifacts may contain unfinished behavior.
Run `python fluid.py context TARGET` for live context and `python fluid.py status TARGET` for readiness and stale evidence.

Existing authoritative project record: [TASK_BRIEF.md](<TASK_BRIEF.md>).

### Whole-project acceptance

- All five public commands in TASK_BRIEF.md work against all four original source documents.
- Keep source text available while visibly identifying current, changed and missing sources.

### Global constraints

- Python 3.11 standard library only; offline; original corpus is read-only.
- Skeleton files are unfinished contracts, not completed behavior or fake data.

### Whole-project sources

- `TASK_BRIEF.md` (project-relative)
- `corpus` (project-relative)

### Entrypoints (instructions; not executed by Fluid)

- `python navigator.py --help`

## Complete capability map

- **Parsing** (`parsing`): Parse the real corpus into stable full passages and native locations.
  Home `areas/parsing`; owner parsing builder; planned; implementation not established by framing.
- **Storage** (`storage`): Safely persist/reopen the index and hash source freshness.
  Home `areas/storage`; owner storage builder; planned; implementation not established by framing.
- **Query** (`query`): Retrieve complete source-backed passages with literal search and current status.
  Home `areas/query`; owner query builder; planned; implementation not established by framing.
- **Cli** (`cli`): Connect all commands and export usable source-linked evidence.
  Home `areas/cli`; owner cli builder; planned; implementation not established by framing.

`depends_on` records meaning and consumer relationships. Only `build_after` gates dispatch; a declared interface may support work before its implementation exists.

## Continue the project

Use `python fluid.py status TARGET` to find ready work and stale evidence; then `python fluid.py context TARGET --module ID` for the chosen responsibility and its neighboring contracts.
Existing source artifacts, the declared completion observations, and actual evidence determine useful progress. A generated module home does not establish implementation.
