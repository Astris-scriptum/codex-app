from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from ..manifest import LexiconSourceManifest
from ..provider import LexiconEntry
from ..sqlite_provider import SQLiteLexiconProvider

@dataclass(frozen=True)
class ImportReport:
    source_id: str
    rows_seen: int
    rows_imported: int
    rows_rejected: int
    source_sha256: str

class DelimitedLexiconImporter:
    version = '1.0.0'
    def import_file(self, source_path, provider, manifest, *, delimiter=',', column_map=None, replace_source=False):
        source_path = Path(source_path)
        mapping = {'text':'text','translation':'translation','meaning':'meaning','language':'language','part_of_speech':'part_of_speech','tags':'tags','lemma':'lemma','morphology':'morphology', **(column_map or {})}
        checksum = LexiconSourceManifest.sha256(source_path)
        rows_seen = rows_imported = rows_rejected = 0
        if replace_source: provider.delete_source(manifest.source_id)
        with source_path.open('r', encoding='utf-8-sig', newline='') as handle:
            for row_number, row in enumerate(csv.DictReader(handle, delimiter=delimiter), start=2):
                rows_seen += 1
                text = (row.get(mapping['text']) or '').strip()
                translation = (row.get(mapping['translation']) or '').strip()
                if not text or not translation:
                    rows_rejected += 1; continue
                tags_raw = (row.get(mapping['tags']) or '').strip()
                entry = LexiconEntry(text=text, translation=translation, meaning=(row.get(mapping['meaning']) or '').strip(), language=(row.get(mapping['language']) or manifest.language).strip(), part_of_speech=(row.get(mapping['part_of_speech']) or '').strip(), tags=tuple(tag.strip() for tag in tags_raw.split('|') if tag.strip()))
                provider.insert_entry(entry, source_id=manifest.source_id, source_row=row_number, lemma=(row.get(mapping['lemma']) or '').strip(), morphology=(row.get(mapping['morphology']) or '').strip())
                rows_imported += 1
        provider.record_source(manifest, source_sha256=checksum, rows_imported=rows_imported)
        return ImportReport(manifest.source_id, rows_seen, rows_imported, rows_rejected, checksum)
