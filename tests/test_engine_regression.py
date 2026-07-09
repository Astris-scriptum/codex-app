import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine import EngineService


def test_nicolas_velasco_regression():
    engine = EngineService()
    results = engine.discover("NICOLAS VELASCO")
    assert any(candidate.text == "CLAVIS CAELO NOS" for candidate in results)


def test_candidate_has_complete_provenance():
    engine = EngineService()
    candidate = engine.discover("NICOLAS VELASCO")[0]
    provenance = candidate.provenance

    assert provenance.source_pool.raw_input == "NICOLAS VELASCO"
    assert provenance.source_pool.normalised_input == "NICOLASVELASCO"
    assert provenance.language_pack.version == "latin_v1"
    assert provenance.search_mode.value == "exact_anagram"
    assert provenance.engine_version == "2.4-alpha"
    assert provenance.score_breakdown.total > 0


def test_engine_reports_plugins_and_language_packs():
    stats = EngineService().statistics()
    assert "latin_v1" in stats["language_packs"]
    assert "exact_anagram:1.1.0" in stats["plugins"]
