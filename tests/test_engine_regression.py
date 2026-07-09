import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))
from codex_engine import EngineService

def test_nicolas_velasco_regression():
    engine = EngineService()
    assert any(c.text == "CLAVIS CAELO NOS" for c in engine.discover("NICOLAS VELASCO"))

def test_candidate_has_complete_provenance():
    candidate = EngineService().discover("NICOLAS VELASCO")[0]
    p = candidate.provenance
    assert p.source_pool.raw_input == "NICOLAS VELASCO"
    assert p.source_pool.normalised_input == "NICOLASVELASCO"
    assert p.language_pack.version == "latin_v1"
    assert p.search_mode.value == "exact_anagram"
    assert p.engine_version == "2.2-alpha"
    assert p.score_breakdown.total > 0
