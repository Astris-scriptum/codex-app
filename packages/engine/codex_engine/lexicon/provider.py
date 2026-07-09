from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LexiconEntry:
    text: str
    translation: str
    meaning: str = ""
    language: str = "Latin"
    part_of_speech: str = ""
    tags: tuple[str, ...] = ()


class LexiconProvider(Protocol):
    def entries(self, language: str) -> list[LexiconEntry]:
        ...


class InMemoryLexiconProvider:
    """Initial lexicon provider. Replaceable by SQLite, Airtable, or dictionary providers."""

    def __init__(self, entries: list[LexiconEntry] | None = None) -> None:
        self._entries = entries or [
            LexiconEntry("CLAVIS", "key", "key; symbolic opening", part_of_speech="noun"),
            LexiconEntry("CAELO", "to/from heaven", "heaven/sky, dative or ablative reading", part_of_speech="noun"),
            LexiconEntry("NOS", "we/us/ours", "first person plural pronoun", part_of_speech="pronoun"),
            LexiconEntry("SOLIS", "of the sun / alone / only", "ambiguous genitive or adjective/adverbial reading", part_of_speech="noun"),
            LexiconEntry("VOCIS", "of the voice", "genitive of vox", part_of_speech="noun"),
            LexiconEntry("LEO", "lion / Leo", "zodiac and animal symbol", part_of_speech="noun"),
            LexiconEntry("ARCANA", "arcana / mysteries", "hidden or sacred mysteries", part_of_speech="noun"),
        ]

    def entries(self, language: str) -> list[LexiconEntry]:
        return [entry for entry in self._entries if entry.language.lower() == language.lower()]
