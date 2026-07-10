from __future__ import annotations

import sqlite3
from pathlib import Path

from .provider import LexiconEntry


SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS lexicon_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    normalised_text TEXT NOT NULL,
    translation TEXT NOT NULL,
    meaning TEXT DEFAULT '',
    language TEXT NOT NULL,
    part_of_speech TEXT DEFAULT '',
    tags TEXT DEFAULT '',
    letter_inventory TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lexicon_language
ON lexicon_entries(language);

CREATE INDEX IF NOT EXISTS idx_lexicon_inventory
ON lexicon_entries(letter_inventory);
'''


class SQLiteLexiconProvider:
    """SQLite-backed lexicon provider.

    This is the first persistent lexicon layer. It remains small and explicit:
    external dictionary imports can later write into this schema without changing
    the engine/plugin contract.
    """

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialise()

    def initialise(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA_SQL)

    def seed(self, entries: list[LexiconEntry]) -> None:
        with self._connect() as conn:
            for entry in entries:
                conn.execute(
                    '''
                    INSERT INTO lexicon_entries (
                        text,
                        normalised_text,
                        translation,
                        meaning,
                        language,
                        part_of_speech,
                        tags,
                        letter_inventory
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        entry.text,
                        self._normalise(entry.text),
                        entry.translation,
                        entry.meaning,
                        entry.language,
                        entry.part_of_speech,
                        ",".join(entry.tags),
                        self._inventory_key(entry.text),
                    ),
                )

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM lexicon_entries")

    def entries(self, language: str) -> list[LexiconEntry]:
        with self._connect() as conn:
            rows = conn.execute(
                '''
                SELECT text, translation, meaning, language, part_of_speech, tags
                FROM lexicon_entries
                WHERE lower(language) = lower(?)
                ORDER BY length(text), text
                ''',
                (language,),
            ).fetchall()

        return [
            LexiconEntry(
                text=row[0],
                translation=row[1],
                meaning=row[2],
                language=row[3],
                part_of_speech=row[4],
                tags=tuple(filter(None, row[5].split(","))) if row[5] else (),
            )
            for row in rows
        ]

    def entries_fitting_inventory(self, language: str, source_text: str) -> list[LexiconEntry]:
        # Initial simple implementation; later this should be SQL-pruned.
        from codex_engine.search import LetterInventory

        source = LetterInventory.from_text(source_text)
        return [
            entry
            for entry in self.entries(language)
            if source.contains(LetterInventory.from_text(entry.text))
        ]

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _normalise(self, text: str) -> str:
        return "".join(ch for ch in text.upper() if ch.isalpha())

    def _inventory_key(self, text: str) -> str:
        from codex_engine.search import LetterInventory

        return ";".join(f"{letter}:{count}" for letter, count in LetterInventory.from_text(text).letters)
