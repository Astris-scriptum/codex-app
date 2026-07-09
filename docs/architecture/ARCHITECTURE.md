# Codex Architecture

```text
Codex Studio
  -> Studio Service Layer
    -> Local Engine Adapter / Local REST Adapter / Cloud Adapter
      -> Codex Engine Core
        -> Plugins / Language Packs / Scoring / Providers
          -> SQLite / PostgreSQL / Airtable / External APIs
```

## Principles

1. Studio is backend-adaptive.
2. Engine is UI-independent.
3. Language rules live in language packs, not hard-coded logic.
4. Every result must preserve provenance.
5. Release artifacts are reproducible.
6. Airtable is operational metadata, not the only source of truth.
