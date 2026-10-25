# CLI delivery evidence

Actual commands include:

- `python navigator.py index --source-dir corpus --index "runtime/research index.json" --json`
- `python navigator.py search --index "runtime/research index.json" --query "Architectural Dimension" --limit 1 --json`
- `python navigator.py export --index "runtime/research index.json" --query "monkey bars" --limit 10 --output "runtime/reports/monkey bars.md"`
- `python navigator.py status --index "runtime/research index.json" --json`
- `python check_actual.py`, which issued 40 public CLI invocations including show, all help paths, absolute/relative paths, spaces, relocated report checks, and expected errors.

All successful JSON invocations parsed as one JSON value with no stderr. Ten deliberately invalid/failure invocations produced nonzero exits, stderr diagnostics, and no stdout. Every source was searched and its complete matching passage fetched by show. The Markdown report was inspected directly. Export preserves full source text in fenced blocks and prints source links, inclusive native locators, heading context, indexed SHA-256, and source status. A Word report was copied to another directory; its absolute percent-encoded file link still resolved to the actual original Word file. Stale exports explicitly showed changed and missing source statuses.

The first connected regression run passed. The originals remained unchanged. Actual argv, exits, and failure diagnostics are saved at `runtime/verification/commands.json`; observations are at `runtime/verification/observations.json`. Public commands and limits are documented in README.md. No claim is made about arbitrary Markdown viewers allowing file links or links surviving source relocation to another machine.
