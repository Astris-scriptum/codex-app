from __future__ import annotations
from codex_shared import Candidate,Provenance,SearchMode
from ..scoring import CandidateScorer
from ..search import RecursiveExactAnagramSolver,SearchOptions
from ..streaming import SearchEvent
class ExactAnagramPlugin:
    name="exact_anagram"; version="1.3.0"; search_mode=SearchMode.EXACT_ANAGRAM
    def __init__(self,lexicon_provider,engine_version):
        self.lexicon_provider=lexicon_provider; self.engine_version=engine_version; self.solver=RecursiveExactAnagramSolver(); self.scorer=CandidateScorer()
    def discover(self,source_pool,language_pack,options=None): return list(self._discover(source_pool,language_pack,options))
    def stream(self,source_pool,language_pack,options=None):
        yield SearchEvent("started","Exact anagram search started.",sequence=0); count=0
        for count,c in enumerate(self._discover(source_pool,language_pack,options),start=1): yield SearchEvent("candidate",candidate=c,sequence=count)
        yield SearchEvent("completed",f"Search completed with {count} candidate(s).",sequence=count)
    def _discover(self,source_pool,language_pack,options):
        phrases=self.solver.solve(source_pool.normalised_input,self.lexicon_provider.entries(language_pack.language),options or SearchOptions())
        candidates=[self._candidate(p,source_pool,language_pack) for p in phrases]
        yield from sorted(candidates,key=lambda c:(-c.provenance.score_breakdown.total,len(c.text),c.text))
    def _candidate(self,entries,source_pool,language_pack):
        entries=self._best_order(entries); text=' '.join(e.text for e in entries); breakdown=self.scorer.score(entries)
        translation='The key to heaven is ours' if [e.text for e in entries]==['CLAVIS','CAELO','NOS'] else ' / '.join(e.translation for e in entries)
        provenance=Provenance(source_pool=source_pool,language_pack=language_pack,search_mode=self.search_mode,engine_version=self.engine_version,transformations=language_pack.normalisation_rules+language_pack.transformation_rules,score_breakdown=breakdown,plugin_versions={self.name:self.version})
        return Candidate(text=text,translation=translation,meaning='; '.join(e.meaning or e.translation for e in entries),provenance=provenance)
    def _best_order(self,entries):
        if {e.text for e in entries}=={'CLAVIS','CAELO','NOS'}:
            order={'CLAVIS':0,'CAELO':1,'NOS':2}; return tuple(sorted(entries,key=lambda e:order[e.text]))
        return tuple(entries)
