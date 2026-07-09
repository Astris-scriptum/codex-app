# Plugin Architecture

Codex search modes are implemented as plugins.

Each plugin exposes:

- `name`
- `version`
- `search_mode`
- `discover(source_pool, language_pack)`

`EngineService` dispatches to plugins through `PluginRegistry`.
