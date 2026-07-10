from __future__ import annotations
from dataclasses import dataclass
from ..lexicon import LexiconEntry
from .inventory import LetterInventory
from .options import SearchOptions
@dataclass(frozen=True)
class SolverConfig:
    max_words:int=4
    max_results:int=500
class RecursiveExactAnagramSolver:
    def __init__(self,config:SolverConfig|None=None): self.config=config or SolverConfig()
    def solve(self,source_text,entries,options:SearchOptions|None=None):
        options=options or SearchOptions(max_words=self.config.max_words,max_results=self.config.max_results)
        target=LetterInventory.from_text(source_text); required={w.upper() for w in options.required_words}; excluded={w.upper() for w in options.excluded_words}
        indexed=[]
        for entry in entries:
            text=entry.text.upper()
            if len(''.join(c for c in text if c.isalpha()))<options.min_word_length or text in excluded: continue
            inv=LetterInventory.from_text(entry.text)
            if target.contains(inv): indexed.append((entry,inv))
        indexed.sort(key=lambda x:(-len(x[0].text),x[0].text)); results=[]
        def walk(remaining,start,phrase):
            if len(results)>=options.max_results:return
            if remaining.is_empty():
                if required.issubset({e.text.upper() for e in phrase}): results.append(tuple(phrase))
                return
            if len(phrase)>=options.max_words:return
            for i in range(start,len(indexed)):
                entry,inv=indexed[i]
                if remaining.contains(inv): walk(remaining.subtract(inv),i,phrase+[entry])
        walk(target,0,[])
        seen=set(); out=[]
        for phrase in results:
            key=tuple(sorted(e.text.upper() for e in phrase)) if options.deduplicate_permutations else tuple(e.text.upper() for e in phrase)
            if key not in seen: seen.add(key); out.append(phrase)
        return out
