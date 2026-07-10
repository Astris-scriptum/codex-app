from __future__ import annotations
from uuid import uuid4
from codex_shared import SearchMode,SearchRun,SourcePool
from .language_packs import LanguagePackManager
from .lexicon import InMemoryLexiconProvider
from .plugins import ExactAnagramPlugin,PluginRegistry
from .search import SearchOptions
from .source_pools import SourcePoolCatalogue
ENGINE_VERSION="2.6-alpha"
class EngineService:
    def __init__(self,lexicon_provider=None):
        self.language_pack_manager=LanguagePackManager(); self.lexicon_provider=lexicon_provider or InMemoryLexiconProvider(); self.plugins=PluginRegistry(); self.plugins.register(ExactAnagramPlugin(self.lexicon_provider,ENGINE_VERSION)); self.source_pool_catalogue=SourcePoolCatalogue()
    def language_packs(self): return [self.language_pack_manager.load(k) for k in self.language_pack_manager.list_available()]
    def source_pools(self): return self.source_pool_catalogue.list_catalogues()
    def statistics(self): return {'engine_version':ENGINE_VERSION,'language_packs':[p.version for p in self.language_packs()],'plugins':[f'{p.name}:{p.version}' for p in self.plugins.list_plugins()],'streaming':True,'source_pool_catalogues':len(self.source_pools())}
    def discover(self,source_text,*,language='latin',search_mode=SearchMode.EXACT_ANAGRAM,options=None):
        lp,sp=self._prepare(source_text,language,search_mode); return self.plugins.get(search_mode).discover(sp,lp,options or SearchOptions())
    def stream(
        self,
        source_text,
        *,
        language="latin",
        search_mode=SearchMode.EXACT_ANAGRAM,
        options=None,
    ) -> Iterator[SearchEvent]:
        language_pack, source_pool = self._prepare(
            source_text,
            language,
            search_mode,
        )
        plugin = self.plugins.get(search_mode)

        if hasattr(plugin, "stream"):
            yield from plugin.stream(
                source_pool,
                language_pack,
                options or SearchOptions(),
            )
            return

        for index, candidate in enumerate(
            plugin.discover(
                source_pool,
                language_pack,
                options or SearchOptions(),
            ),
            start=1,
        ):
            yield SearchEvent(
                event_type="candidate",
                candidate=candidate,
                sequence=index,
            )

    def _prepare(self,source_text,language,search_mode):
        lp=self.language_pack_manager.load(language); sp=SourcePool(raw_input=source_text,normalised_input=self.normalise(source_text),label=source_text); SearchRun(run_id=str(uuid4()),source_pool=sp,search_mode=search_mode,language_pack=lp,engine_version=ENGINE_VERSION); return lp,sp
    def normalise(self,text): return ''.join(c for c in text.upper() if c.isalpha())
