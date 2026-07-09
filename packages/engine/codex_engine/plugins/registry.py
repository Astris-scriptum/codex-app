from __future__ import annotations

from codex_shared import SearchMode, SearchPlugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[SearchMode, SearchPlugin] = {}

    def register(self, plugin: SearchPlugin) -> None:
        self._plugins[plugin.search_mode] = plugin

    def get(self, search_mode: SearchMode) -> SearchPlugin:
        if search_mode not in self._plugins:
            raise ValueError(f"No plugin registered for search mode: {search_mode.value}")
        return self._plugins[search_mode]

    def list_plugins(self) -> list[SearchPlugin]:
        return list(self._plugins.values())
