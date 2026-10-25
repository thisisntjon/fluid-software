# Query delivery evidence

Actual command: `python check_actual.py` with the assigned Python executable; exact subprocess invocations and return codes are in `runtime/verification/commands.json`.

Observed: literal case-insensitive searches derived from real passages returned content from all four sources; each returned selected passage was fetched through public show, with equality of full text, locator, headings, hash, identity, and status. The literal query `Architectural Dimension Unconstrained Greenfield Swarm` matched across Word table paragraph newlines. `**Strong evidence**` matched the literal Markdown punctuation. `agents` with limit 1 was deterministic. An absent query returned an empty match list. Whitespace-only queries and limits 0, -2, and a noninteger produced errors with empty stdout; an unknown passage ID also failed concisely.

Private copies of actual files were changed/removed; search and show returned the preserved indexed passage text with changed/missing states, alongside current sources. No fixture index, synthetic document, or mock was used. The source files remained byte-identical. Matching is passage-local, whitespace-normalized, and literal; no ranking, stemming, fuzzy matching, or semantic retrieval is claimed.
