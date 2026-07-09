# Search Engine

Codex Engine v2.4-alpha introduces the first recursive exact-anagram solver.

Pipeline:

```text
source text
→ normalised inventory
→ lexicon entries
→ inventory pruning
→ recursive phrase assembly
→ scoring
→ candidate objects with provenance
```

The solver is deterministic and keeps search-mode implementation inside plugins.

## Current limitations

- In-memory lexicon only.
- Alpha-scale recursion.
- Minimal grammar scoring.
- No SQLite provider yet.
- No streaming iterator yet.
