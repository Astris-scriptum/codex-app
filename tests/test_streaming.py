import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "shared"))
sys.path.insert(0, str(ROOT / "packages" / "engine"))

from codex_engine import EngineService


def test_streaming_emits_candidate_event():
    events = list(EngineService().stream("NICOLAS VELASCO"))
    assert events[0].event_type == "started"
    assert any(event.event_type == "candidate" and event.candidate and event.candidate.text == "CLAVIS CAELO NOS" for event in events)
    assert events[-1].event_type == "completed"
