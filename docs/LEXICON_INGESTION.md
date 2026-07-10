# Lexicon ingestion — Engine v2.7-alpha

Codex now has a provenance-preserving import boundary for external lexicons.

Every imported corpus must declare source ID, title, language, version, licence, source URL, attribution, checksum, importer version and import timestamp.

Supported UTF-8 CSV/TSV columns: `text`, `translation`, `meaning`, `language`, `part_of_speech`, `tags`, `lemma`, `morphology`.

```bash
python3 scripts/import_lexicon.py data/latin.csv packages/engine/codex_engine/config/lexicon_sources/example_manifest.json --database state/studio/lexicon.sqlite --replace-source
```

Each entry retains `source_id` and `source_row`; each corpus retains its SHA-256.
