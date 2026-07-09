import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine.language_packs import LanguagePackManager


def test_latin_language_pack_loads_from_config():
    manager = LanguagePackManager()
    pack = manager.load("latin")
    assert pack.language == "Latin"
    assert pack.version == "latin_v1"
    assert "uppercase" in pack.normalisation_rules
