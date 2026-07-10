# SQLite Lexicon

Codex Engine v2.5-alpha introduces `SQLiteLexiconProvider`.

The first schema stores:

- text
- normalised text
- translation
- meaning
- language
- part of speech
- tags
- letter inventory

This creates the first durable lexicon layer while preserving the provider interface used by plugins.
