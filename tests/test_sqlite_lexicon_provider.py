import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine.lexicon import LexiconEntry, SQLiteLexiconProvider


def test_sqlite_lexicon_provider_round_trip(tmp_path):
    db = tmp_path / "lexicon.sqlite"
    provider = SQLiteLexiconProvider(db)
    provider.seed([LexiconEntry("CLAVIS", "key", language="Latin")])

    entries = provider.entries("Latin")
    assert len(entries) == 1
    assert entries[0].text == "CLAVIS"
