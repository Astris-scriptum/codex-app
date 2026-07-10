from __future__ import annotations
import sqlite3
from pathlib import Path
from .manifest import LexiconSourceManifest
from .provider import LexiconEntry

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS lexicon_sources (source_id TEXT PRIMARY KEY,title TEXT NOT NULL,language TEXT NOT NULL,version TEXT NOT NULL,licence TEXT NOT NULL,source_url TEXT DEFAULT '',attribution TEXT DEFAULT '',imported_at TEXT NOT NULL,source_sha256 TEXT NOT NULL,importer_version TEXT NOT NULL,rows_imported INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS lexicon_entries (id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT NOT NULL,normalised_text TEXT NOT NULL,translation TEXT NOT NULL,meaning TEXT DEFAULT '',language TEXT NOT NULL,part_of_speech TEXT DEFAULT '',tags TEXT DEFAULT '',letter_inventory TEXT NOT NULL,source_id TEXT NOT NULL DEFAULT 'builtin',source_row INTEGER,lemma TEXT DEFAULT '',morphology TEXT DEFAULT '',FOREIGN KEY(source_id) REFERENCES lexicon_sources(source_id));
CREATE INDEX IF NOT EXISTS idx_lexicon_language ON lexicon_entries(language);
CREATE INDEX IF NOT EXISTS idx_lexicon_inventory ON lexicon_entries(letter_inventory);
CREATE INDEX IF NOT EXISTS idx_lexicon_normalised ON lexicon_entries(normalised_text);
CREATE INDEX IF NOT EXISTS idx_lexicon_source ON lexicon_entries(source_id);
"""

class SQLiteLexiconProvider:
    def __init__(self, db_path):
        self.db_path = Path(db_path); self.db_path.parent.mkdir(parents=True, exist_ok=True); self.initialise()
    def initialise(self):
        with self._connect() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.execute("INSERT OR IGNORE INTO lexicon_sources (source_id,title,language,version,licence,imported_at,source_sha256,importer_version) VALUES ('builtin','Codex built-in seed','Latin','1','internal',datetime('now'),'builtin','builtin')")
    def record_source(self, manifest, *, source_sha256, rows_imported):
        with self._connect() as conn:
            conn.execute("INSERT OR REPLACE INTO lexicon_sources (source_id,title,language,version,licence,source_url,attribution,imported_at,source_sha256,importer_version,rows_imported) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (manifest.source_id,manifest.title,manifest.language,manifest.version,manifest.licence,manifest.source_url,manifest.attribution,manifest.imported_at,source_sha256,manifest.importer_version,rows_imported))
    def insert_entry(self, entry, *, source_id='builtin', source_row=None, lemma='', morphology=''):
        with self._connect() as conn:
            conn.execute("INSERT INTO lexicon_entries (text,normalised_text,translation,meaning,language,part_of_speech,tags,letter_inventory,source_id,source_row,lemma,morphology) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (entry.text,self._normalise(entry.text),entry.translation,entry.meaning,entry.language,entry.part_of_speech,'|'.join(entry.tags),self._inventory_key(entry.text),source_id,source_row,lemma,morphology))
    def seed(self, entries):
        for entry in entries: self.insert_entry(entry)
    def clear(self):
        with self._connect() as conn: conn.execute('DELETE FROM lexicon_entries')
    def delete_source(self, source_id):
        with self._connect() as conn:
            conn.execute('DELETE FROM lexicon_entries WHERE source_id=?',(source_id,)); conn.execute('DELETE FROM lexicon_sources WHERE source_id=?',(source_id,))
    def entries(self, language):
        with self._connect() as conn:
            rows=conn.execute("SELECT text,translation,meaning,language,part_of_speech,tags FROM lexicon_entries WHERE lower(language)=lower(?) ORDER BY length(text),text",(language,)).fetchall()
        return [LexiconEntry(text=r[0],translation=r[1],meaning=r[2],language=r[3],part_of_speech=r[4],tags=tuple(filter(None,r[5].split('|'))) if r[5] else ()) for r in rows]
    def source_statistics(self):
        with self._connect() as conn:
            conn.row_factory=sqlite3.Row
            rows=conn.execute("SELECT s.*,COUNT(e.id) AS entry_count FROM lexicon_sources s LEFT JOIN lexicon_entries e ON e.source_id=s.source_id GROUP BY s.source_id ORDER BY s.source_id").fetchall()
        return [dict(r) for r in rows]
    def _connect(self): return sqlite3.connect(self.db_path)
    def _normalise(self,text): return ''.join(ch for ch in text.upper() if ch.isalpha())
    def _inventory_key(self,text):
        from codex_engine.search import LetterInventory
        return ';'.join(f'{l}:{c}' for l,c in LetterInventory.from_text(text).letters)
