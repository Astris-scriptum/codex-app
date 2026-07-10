#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'packages'/'engine'))
from codex_engine.lexicon import DelimitedLexiconImporter,LexiconSourceManifest,SQLiteLexiconProvider

def main():
    p=argparse.ArgumentParser(); p.add_argument('source_file'); p.add_argument('manifest_file'); p.add_argument('--database',default='state/studio/lexicon.sqlite'); p.add_argument('--delimiter',default=','); p.add_argument('--replace-source',action='store_true'); a=p.parse_args()
    provider=SQLiteLexiconProvider(ROOT/a.database); manifest=LexiconSourceManifest.from_json(a.manifest_file)
    report=DelimitedLexiconImporter().import_file(a.source_file,provider,manifest,delimiter=a.delimiter.encode().decode('unicode_escape'),replace_source=a.replace_source); print(report)
if __name__=='__main__': main()
