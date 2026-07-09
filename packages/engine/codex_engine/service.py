from __future__ import annotations

from uuid import uuid4

from codex_shared import Candidate, SearchMode, SearchRun, SourcePool

from .language_packs import LanguagePackManager
from .lexicon import InMemoryLexiconProvider, LexiconProvider
from .plugins import ExactAnagramPlugin, PluginRegistry

ENGINE_VERSION = "2.4-alpha"


class EngineService:
    """Stable production-facing engine interface."""

    def __init__(self, lexicon_provider: LexiconProvider | None = None) -> None:
        self.language_pack_manager = LanguagePackManager()
        self.lexicon_provider = lexicon_provider or InMemoryLexiconProvider()
        self.plugins = PluginRegistry()
        self.plugins.register(ExactAnagramPlugin(self.lexicon_provider, ENGINE_VERSION))

    def language_packs(self):
        return [self.language_pack_manager.load(key) for key in self.language_pack_manager.list_available()]

    def validate(self) -> bool:
        return "latin" in self.language_pack_manager.list_available()

    def regress(self) -> bool:
        return any(c.text == "CLAVIS CAELO NOS" for c in self.discover("NICOLAS VELASCO"))

    def statistics(self) -> dict[str, object]:
        return {
            "engine_version": ENGINE_VERSION,
            "language_packs": [pack.version for pack in self.language_packs()],
            "plugins": [f"{plugin.name}:{plugin.version}" for plugin in self.plugins.list_plugins()],
        }

    def discover(
        self,
        source_text: str,
        *,
        language: str = "latin",
        search_mode: SearchMode = SearchMode.EXACT_ANAGRAM,
    ) -> list[Candidate]:
        language_pack = self.language_pack_manager.load(language)
        source_pool = SourcePool(
            raw_input=source_text,
            normalised_input=self.normalise(source_text),
            label=source_text,
        )
        SearchRun(
            run_id=str(uuid4()),
            source_pool=source_pool,
            search_mode=search_mode,
            language_pack=language_pack,
            engine_version=ENGINE_VERSION,
        )
        plugin = self.plugins.get(search_mode)
        return plugin.discover(source_pool, language_pack)

    def normalise(self, text: str) -> str:
        return "".join(ch for ch in text.upper() if ch.isalpha())
