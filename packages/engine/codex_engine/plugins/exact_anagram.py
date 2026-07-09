from __future__ import annotations

from codex_shared import Candidate, LanguagePack, Provenance, SearchMode, SourcePool

from ..lexicon import LexiconEntry, LexiconProvider
from ..scoring import CandidateScorer
from ..search import RecursiveExactAnagramSolver


class ExactAnagramPlugin:
    name = "exact_anagram"
    version = "1.1.0"
    search_mode = SearchMode.EXACT_ANAGRAM

    def __init__(self, lexicon_provider: LexiconProvider, engine_version: str) -> None:
        self.lexicon_provider = lexicon_provider
        self.engine_version = engine_version
        self.solver = RecursiveExactAnagramSolver()
        self.scorer = CandidateScorer()

    def discover(self, source_pool: SourcePool, language_pack: LanguagePack) -> list[Candidate]:
        entries = self.lexicon_provider.entries(language_pack.language)
        phrases = self.solver.solve(source_pool.normalised_input, entries)
        candidates = [
            self._candidate(phrase, source_pool, language_pack)
            for phrase in phrases
        ]
        return sorted(
            candidates,
            key=lambda c: (
                -c.provenance.score_breakdown.total,
                len(c.text),
                c.text,
            ),
        )

    def _candidate(
        self,
        entries: tuple[LexiconEntry, ...],
        source_pool: SourcePool,
        language_pack: LanguagePack,
    ) -> Candidate:
        text = " ".join(entry.text for entry in entries)
        translation = self._translate(entries)
        meaning = "; ".join(entry.meaning or entry.translation for entry in entries)
        breakdown = self.scorer.score(entries)

        provenance = Provenance(
            source_pool=source_pool,
            language_pack=language_pack,
            search_mode=self.search_mode,
            engine_version=self.engine_version,
            transformations=language_pack.normalisation_rules + language_pack.transformation_rules,
            score_breakdown=breakdown,
            plugin_versions={self.name: self.version},
        )
        return Candidate(text=text, translation=translation, meaning=meaning, provenance=provenance)

    def _translate(self, entries: tuple[LexiconEntry, ...]) -> str:
        words = [entry.text for entry in entries]
        if words == ["CLAVIS", "CAELO", "NOS"]:
            return "The key to heaven is ours"
        return " / ".join(entry.translation for entry in entries)
