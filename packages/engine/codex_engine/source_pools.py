from __future__ import annotations
import json
from pathlib import Path
class SourcePoolCatalogue:
    def __init__(self, config_root: Path|None=None):
        self.config_root=config_root or (Path(__file__).resolve().parent/"config"/"source_pools")
    def list_catalogues(self):
        if not self.config_root.exists(): return []
        return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(self.config_root.glob("*.json"))]
