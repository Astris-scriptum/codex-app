from __future__ import annotations
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4
from codex_shared import SearchMode, SearchRun, SourcePool
from .language_packs import LanguagePackManager
from .lexicon import InMemoryLexiconProvider, SQLiteLexiconProvider, bootstrap_sqlite_lexicon
from .plugins import ExactAnagramPlugin, PluginRegistry
from .search import SearchOptions
from .source_pools import SourcePoolCatalogue
from .streaming import SearchEvent
ENGINE_VERSION='2.7-alpha'
class EngineService:
    def __init__(self, lexicon_provider=None, *, workspace_root=None):
        self.language_pack_manager=LanguagePackManager()
        if lexicon_provider is not None: self.lexicon_provider=lexicon_provider
        elif workspace_root is not None:
            db_path=Path(workspace_root)/'lexicon.sqlite'; provider=SQLiteLexiconProvider(db_path)
            if not provider.entries('Latin'): provider=bootstrap_sqlite_lexicon(str(db_path))
            self.lexicon_provider=provider
        else: self.lexicon_provider=InMemoryLexiconProvider()
        self.plugins=PluginRegistry(); self.plugins.register(ExactAnagramPlugin(self.lexicon_provider,ENGINE_VERSION)); self.source_pool_catalogue=SourcePoolCatalogue()
    def language_packs(self): return [self.language_pack_manager.load(k) for k in self.language_pack_manager.list_available()]
    def source_pools(self): return self.source_pool_catalogue.list_catalogues()
    def statistics(self):
        result={'engine_version':ENGINE_VERSION,'language_packs':[p.version for p in self.language_packs()],'plugins':[f'{p.name}:{p.version}' for p in self.plugins.list_plugins()],'streaming':True,'source_pool_catalogues':len(self.source_pools()),'lexicon_provider':type(self.lexicon_provider).__name__}
        if hasattr(self.lexicon_provider,'source_statistics'): result['lexicon_sources']=self.lexicon_provider.source_statistics()
        return result
    def discover(self,source_text,*,language='latin',search_mode=SearchMode.EXACT_ANAGRAM,options=None):
        lp,sp=self._prepare(source_text,language,search_mode); return self.plugins.get(search_mode).discover(sp,lp,options or SearchOptions())
    def stream(self,source_text,*,language='latin',search_mode=SearchMode.EXACT_ANAGRAM,options=None)->Iterator[SearchEvent]:
        lp,sp=self._prepare(source_text,language,search_mode); yield from self.plugins.get(search_mode).stream(sp,lp,options or SearchOptions())
    def _prepare(self,source_text,language,search_mode):
        lp=self.language_pack_manager.load(language); sp=SourcePool(raw_input=source_text,normalised_input=self.normalise(source_text),label=source_text); SearchRun(run_id=str(uuid4()),source_pool=sp,search_mode=search_mode,language_pack=lp,engine_version=ENGINE_VERSION); return lp,sp
    def normalise(self,text): return ''.join(c for c in text.upper() if c.isalpha())
