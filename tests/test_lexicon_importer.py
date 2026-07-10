import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'packages'/'engine'))
from codex_engine.lexicon import DelimitedLexiconImporter,LexiconSourceManifest,SQLiteLexiconProvider

def test_delimited_import_preserves_source_provenance(tmp_path):
    source=tmp_path/'latin.csv'; source.write_text('text,translation,language,part_of_speech,lemma,morphology\nCLAVIS,key,Latin,noun,clavis,nom.sg\n',encoding='utf-8')
    provider=SQLiteLexiconProvider(tmp_path/'lexicon.sqlite'); manifest=LexiconSourceManifest(source_id='test_source',title='Test Source',language='Latin',version='1',licence='test-only')
    report=DelimitedLexiconImporter().import_file(source,provider,manifest)
    assert report.rows_imported==1; assert provider.entries('Latin')[0].text=='CLAVIS'; stats=provider.source_statistics(); row=next(x for x in stats if x['source_id']=='test_source'); assert row['entry_count']==1; assert row['source_sha256']==report.source_sha256
