import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'packages'/'shared')); sys.path.insert(0,str(ROOT/'packages'/'engine'))
from codex_engine import EngineService

def test_workspace_engine_uses_sqlite_and_preserves_regression(tmp_path):
    engine=EngineService(workspace_root=tmp_path); assert engine.statistics()['engine_version']=='2.7-alpha'; assert engine.statistics()['lexicon_provider']=='SQLiteLexiconProvider'; assert any(c.text=='CLAVIS CAELO NOS' for c in engine.discover('NICOLAS VELASCO'))
def test_streaming_api_is_available(tmp_path):
    events=list(EngineService(workspace_root=tmp_path).stream('NICOLAS VELASCO')); assert events[0].event_type=='started'; assert events[-1].event_type=='completed'
