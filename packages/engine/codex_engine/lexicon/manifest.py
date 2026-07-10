from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json

@dataclass(frozen=True)
class LexiconSourceManifest:
    source_id: str
    title: str
    language: str
    version: str
    licence: str
    source_url: str = ''
    attribution: str = ''
    imported_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_sha256: str = ''
    importer_version: str = '1.0.0'

    @classmethod
    def from_json(cls, path: str | Path) -> 'LexiconSourceManifest':
        return cls(**json.loads(Path(path).read_text(encoding='utf-8')))

    @staticmethod
    def sha256(path: str | Path) -> str:
        digest = hashlib.sha256()
        with Path(path).open('rb') as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                digest.update(chunk)
        return digest.hexdigest()
