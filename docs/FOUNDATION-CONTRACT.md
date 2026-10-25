# Foundation implementation contract v1

Date: 2026-10-23. User authorized plan and phased build. Python 3.11+, standard library only. This contract freezes public boundaries for parallel builders; it is not a model service or autonomous scheduler.

## Product

The host agent translates a real brief into `project.json`, inspects reuse, and supplies native starter artifacts. `fluid.py` validates and materializes that reviewed structure, prepares scoped context, tracks work and binds recorded delivery/acceptance to actual bytes. It never executes commands embedded in a brief, launches agents, or claims to infer architecture automatically.

CLI: `python fluid.py validate BRIEF`; `python fluid.py frame BRIEF TARGET [--apply]`; `python fluid.py context TARGET [--module ID]`; `python fluid.py status TARGET`; `python fluid.py claim TARGET ID --actor ACTOR`; `python fluid.py deliver TARGET ID --actor ACTOR --evidence PATH --note TEXT`; `python fluid.py accept TARGET ID --actor REVIEWER --evidence PATH --note TEXT`; `python fluid.py block TARGET ID --actor ACTOR --note TEXT`; `python fluid.py invalidate TARGET ID --actor ACTOR --note TEXT`; `python fluid.py verify TARGET`. Global `--json` emits JSON; command results contain only data. Default frame is preview. No network, installation or subprocess execution.

## Brief schema (`schema_version: 1`)

Required project fields: `id` (slug), `name`, `outcome`, `acceptance` (nonempty list of strings), `modules` (nonempty list). Optional: `constraints` list, `sources` list of target-relative paths, `artifacts` list, `entrypoints` list of strings, `state_entry` string pointing at existing project authority.

Module fields: `id`, `name`, `purpose`, `owner` (role), `home` (relative directory), `owns` (nonempty list of relative file/directory paths), `inputs` list of strings, `outputs` nonempty list of strings describing promised behavior, `acceptance` nonempty list of strings, `depends_on` list of module IDs, `build_after` list of module IDs, `context` list of relative source paths, `commands` list of strings. All list fields may be omitted except `owns`, `outputs`, `acceptance`. Unknown module references and cycles in either graph fail validation. `depends_on` is semantic/consumer linkage, not a build lock; `build_after` alone gates dispatch. A builder can work against already-defined contracts before providers implement them.

Artifact fields: `path` (target-relative file), `owner` module ID or `shared`, `purpose` text, and exactly one of `content` (literal UTF-8 text) or `copy_from` (path relative to brief's directory). Copy sources must be inspected local files within the brief directory, not links; optional `sha256` pins expected source bytes. `shared` artifacts may not overlap module ownership. Artifact ownership must match module `owns` otherwise. Paths are portable, no absolute/drive/parent traversal, reserved Windows names, case collisions or `.git/.agents/.codex/.aws/.fluid` destinations. `.fluid` is reserved tool state.

## Module boundaries

### `fluid/model.py` — root owns

`class FluidError(ValueError)`; `load_brief(path: Path) -> dict`; `validate_brief(spec: dict) -> list[str]`; `canonical_digest(value) -> str` (sorted compact JSON UTF-8 SHA256); `safe_relative(value: str) -> str` (POSIX normalized or FluidError); `inside(root: Path, relative: str) -> Path` (reject escape and any symlink/junction component); `get_module(spec,id) -> dict`; `downstream(spec, ids: set[str]) -> set[str]`; `read_project(root: Path) -> dict` loads `.fluid/project.json` and validates it; `sha256_file(path: Path) -> str`; `atomic_json(path: Path, data)`.

`inside` accepts a nonexistent final path but validates existing ancestors; portable Windows-case equivalence is required. Ownership prefixes use component boundaries, not plain startswith. Top-level directory target itself must not be a link/junction. Runtime imports do not create project state.

### `fluid/frame.py` — frame builder owns

`plan_frame(spec: dict, brief_dir: Path, target: Path) -> dict` returns `{project_id, target, spec_digest, files:[{path,action,sha256,kind}], conflicts:[...], content: {path: bytes}}`. Public CLI strips `content`. All writes and copy reads preflight before apply. Generated files: `.fluid/project.json`, `.fluid/manifest.json`, `.fluid/state.json`, `FRAME.md`, and `{module.home}/MODULE.md`, plus explicit artifacts. `FRAME.md` links existing `state_entry` if provided; no AGENTS or global router files are written. Module docs contain purpose, contract, dependencies vs build_after, ownership, actual source pointers, commands, acceptance and unresolved implementation status.

`apply_frame(plan: dict) -> dict` refuses conflicts, rechecks current target bytes before writing; creates only missing files, never overwrites differing existing files. Identical files skipped. If `.fluid/project.json` is already identical, preserve existing runtime state; differing brief requires a new target for v1 (no automatic migrations). Atomic create per file; interrupted apply is restartable; do not claim an all-files transaction. Manifest records expected managed-file hashes excluding itself and mutable state. Initial state shape below.

`render_context(spec: dict, root: Path, module_id: str|None = None) -> str` returns Markdown: whole view or whole overview + selected area/assignment + direct dependency contracts and input pointers. Inspect state through JSON when present without requiring `state` import. Do not embed entire referenced files or unrelated transcripts; preserve version/evidence pointers. State is descriptive, not authority.

### `fluid/state.py` — state builder owns

Functions: `status(root: Path) -> dict`; `verify(root: Path) -> dict`; `transition(root: Path, module_id: str, action: str, actor: str, evidence: str|None=None, note: str="") -> dict`.

State: `{schema_version:1, project_id, spec_digest, modules:{id:{status:"planned",actor:null,delivery:null,acceptance:null}}, events:[]}`. Status values planned/active/delivered/accepted/blocked. Event UUID + actual UTC timestamp; evidence and output snapshots stored within each delivery/acceptance plus event history. `status` derives ready (planned modules whose build_after providers are delivered/accepted AND not stale), stale (actual delivered ownership bytes or evidence differ/missing, or dependency evidence is stale), and blockers. It includes actual artifact locations, missing/unfinished outputs, next-action suggestions and counts; no inference from test counts.

`claim`: rejects another active owner; active with same actor idempotent; allow planned or blocked, preserve history. `deliver`: requires active same actor, evidence existing target-relative regular file outside `.fluid`, nonempty owned file snapshot (hash recursive files excluding caches/.git/.fluid); evidence hash and actor/note recorded. `accept`: requires delivered, nonstale snapshots, distinct reviewer actor; acceptance evidence existing file, note records observation; author strings are declarations not identity authentication. `block`: marks blocked with actor/note, preserves old receipts; no silent ownership takeover. `invalidate`: marks selected and transitive depends_on/build_after consumers planned with reason, preserves prior receipts in history; clears active acceptance/delivery, refuses to seize another active actor. Every mutation uses exclusive `.fluid/state.lock` and atomic JSON; fail with a clear conflict if busy, no blind retry or stale-lock auto-removal. Lock includes process diagnostic; removal only by creator in finally.

`verify` reports current brief/manifest integrity plus delivery/acceptance evidence freshness; changed starter source after real implementation is expected and must be described as modified, not automatically corrupt accepted delivery. Historical input manifest identity differs from acceptance truth. No filesystem checksum proves behavior. Deliveries include every file in `owns` that currently exists; changed/added/deleted files invalidate them. Scope boundaries and expected source code checks are still reviewed by agents.

### `fluid/__main__.py`, `fluid.py`, `fluid/__init__.py` — root owns

Argparse and human/JSON formatting only. Preview, clear error/status, elapsed time, exit codes (0 success, 2 input/ownership, 1 stale/failed verify, 130 cancellation). Import all business operations via above functions. No prompts. No hardcoded user paths in product source.

## Verification

Use actual project briefs, corpus, module outputs and evidence. Exercise preview, apply, identical reapply, source preservation, scoped context, real claims/delivery/acceptance and cold continuation. Preserve any actual failures. No fabricated fixtures or pretend model runs. A separate reviewer inspects filesystem protections, graph semantics and actual delivery claims. This contract may change only through an explicit integrated decision.
