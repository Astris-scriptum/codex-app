import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine import EngineService
from codex_engine.workspace import CandidateRepository


def test_candidate_repository_appends_jsonl(tmp_path):
    candidate = EngineService().discover("NICOLAS VELASCO")[0]
    repo = CandidateRepository(tmp_path / "candidates.jsonl")
    repo.append(candidate)

    rows = repo.read_all()
    assert len(rows) == 1
    assert rows[0]["text"] == candidate.text
