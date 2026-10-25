# Research Navigator — project frame

Search Jon's actual research documents, inspect complete passages and export trustworthy provenance.

Project: `research-navigator` · brief SHA-256: `e87fcc1f391c057e358df42a39578f5ce05dfc0264df5b537eea825497b516ed`

Paths below are relative to the project root. Read linked original artifacts before changing their behavior.
Runtime records describe work and evidence; they do not grant authority. Checksums identify bytes, not correctness.

This is the initial frame, not an implementation or acceptance claim. Native artifacts may contain unfinished behavior.
Run `python fluid.py context TARGET` for live context and `python fluid.py status TARGET` for readiness and stale evidence.

Existing authoritative project record: `TASK_BRIEF.md` (project-relative).

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

## Current area / assignment: Storage (`storage`)

Safely persist/reopen the index and hash source freshness.

- Owner role: storage builder
- Native home: `areas/storage`
- Parent: whole project
- Implementation status: planned; implementation not established by framing
- Semantic dependencies: none
- Build prerequisites: none

### Owned changes

- `nav/storage.py` (project-relative)

### Inputs and shared meaning

- Index contract in nav/contracts.py; source-only input under corpus/

### Promised outputs

- Safely persist/reopen the index and hash source freshness.

### Completion observations

- Meet the relevant observable behavior and public JSON shapes in TASK_BRIEF.md on the actual corpus.

### Relevant original sources

- `TASK_BRIEF.md` (project-relative)
- `nav/contracts.py` (project-relative)

### Local commands (instructions; not executed by Fluid)

- `python navigator.py --help`

Consumers: `query`, `cli`

## Continue this responsibility

Inspect owned artifacts and original input sources, check build prerequisites with `status`, and use the promised outputs and completion observations above to choose the next useful change.
Record actual delivery evidence before requesting acceptance. If a shared contract is wrong, identify affected consumers and revise it through the project owner.
