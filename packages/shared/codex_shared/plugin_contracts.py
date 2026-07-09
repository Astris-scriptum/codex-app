from __future__ import annotations

from typing import Protocol

from .models import Candidate, LanguagePack, SearchMode, SourcePool


class SearchPlugin(Protocol):
    """Contract implemented by all search plugins."""

    name: str
    version: str
    search_mode: SearchMode

    def discover(
        self,
        source_pool: SourcePool,
        language_pack: LanguagePack,
    ) -> list[Candidate]:
        ...
