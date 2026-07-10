from __future__ import annotations

from .provider import InMemoryLexiconProvider
from .sqlite_provider import SQLiteLexiconProvider


def bootstrap_sqlite_lexicon(db_path: str) -> SQLiteLexiconProvider:
    provider = SQLiteLexiconProvider(db_path)
    provider.clear()
    provider.seed(InMemoryLexiconProvider().entries("Latin"))
    return provider
