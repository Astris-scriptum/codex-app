from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LexiconEntry:
    text: str
    translation: str
    meaning: str = ""
    language: str = "Latin"


class LexiconProvider(Protocol):
    def entries(self, language: str) -> list[LexiconEntry]:
        ...


class InMemoryLexiconProvider:
    """Initial lexicon provider. Replaceable by SQLite, Airtable, or dictionary providers."""

    def __init__(self, entries: list[LexiconEntry] | None = None) -> None:
        self._entries = entries or [
            LexiconEntry("CLAVIS", "key", "key; symbolic opening"),
            LexiconEntry("CAELO", "to/from heaven", "heaven/sky, dative or ablative reading"),
            LexiconEntry("NOS", "we/us/ours", "first person plural pronoun"),
            LexiconEntry("SOLIS", "of the sun / alone / only", "ambiguous genitive or adjective/adverbial reading"),
            LexiconEntry("VOCIS", "of the voice", "genitive of vox"),
            LexiconEntry("LEO", "lion / Leo", "zodiac and animal symbol"),
            LexiconEntry("ARCANA", "arcana / mysteries", "hidden or sacred mysteries"),
        ]

    def entries(self, language: str) -> list[LexiconEntry]:
        return [entry for entry in self._entries if entry.language.lower() == language.lower()]
