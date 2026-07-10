import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "studio" / "python_backend"))
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))
from codex_studio_backend.server import StudioApplication

def test_health_reports_engine(tmp_path):
    assert StudioApplication(tmp_path).health()["engine"]["engine_version"] == "2.5-alpha"

def test_discover_returns_canonical_candidate(tmp_path):
    result = StudioApplication(tmp_path).discover({"source_text":"NICOLAS VELASCO","language":"latin"})
    assert any(c["text"] == "CLAVIS CAELO NOS" for c in result["candidates"])

def test_save_candidate_persists_history(tmp_path):
    app = StudioApplication(tmp_path)
    assert app.save_candidate({"source_text":"NICOLAS VELASCO","candidate_text":"CLAVIS CAELO NOS"})["saved"]
    assert app.history()["count"] == 1
