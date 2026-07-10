import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'packages'/'shared'));sys.path.insert(0,str(ROOT/'packages'/'engine'))
from codex_engine import EngineService
from codex_engine.search import SearchOptions
def test_required(): assert [c.text for c in EngineService().discover('NICOLAS VELASCO',options=SearchOptions(required_words=('CLAVIS',)))]==['CLAVIS CAELO NOS']
def test_excluded(): assert EngineService().discover('NICOLAS VELASCO',options=SearchOptions(excluded_words=('CLAVIS',)))==[]
