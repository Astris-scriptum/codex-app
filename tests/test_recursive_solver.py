import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine.lexicon import LexiconEntry
from codex_engine.search import RecursiveExactAnagramSolver


def test_recursive_solver_finds_phrase_from_inventory():
    entries = [
        LexiconEntry("CLAVIS", "key"),
        LexiconEntry("CAELO", "heaven"),
        LexiconEntry("NOS", "us"),
        LexiconEntry("RANDOM", "random"),
    ]
    solver = RecursiveExactAnagramSolver()
    phrases = solver.solve("NICOLAS VELASCO", entries)
    rendered = {" ".join(entry.text for entry in phrase) for phrase in phrases}
    assert "CLAVIS CAELO NOS" in rendered
