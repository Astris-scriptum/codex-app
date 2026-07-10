import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'studio'/'python_backend'));sys.path.insert(0,str(ROOT/'packages'/'shared'));sys.path.insert(0,str(ROOT/'packages'/'engine'))
from codex_studio_backend.server import StudioApplication
def test_versions(tmp_path):
 h=StudioApplication(tmp_path).health();assert h['studio_version']=='0.2-alpha';assert h['engine']['engine_version']=='2.7-alpha'
def test_config_has_pools(tmp_path): assert 'NICOLAS VELASCO' in StudioApplication(tmp_path).config()['source_pool_catalogues'][0]['pools']
def test_dedupes(tmp_path):
 r=StudioApplication(tmp_path).discover({'source_text':'NICOLAS VELASCO'});assert [c['text'] for c in r['candidates']]==['CLAVIS CAELO NOS']
def test_zero_result(tmp_path): assert StudioApplication(tmp_path).discover({'source_text':'SIMON GARAIDH'})['candidate_count']==0
