# Codex Engine API

`EngineService` is the stable production-facing API.

Methods:

- `discover(source_text, language, search_mode)`
- `validate()`
- `regress()`
- `statistics()`
- `language_packs()`

Search execution is now plugin-dispatched. The initial implemented plugin is `exact_anagram`.
