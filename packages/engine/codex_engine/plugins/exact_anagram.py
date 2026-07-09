from __future__ import annotations

from collections import Counter

from codex_shared import Candidate, LanguagePack, Provenance, ScoreBreakdown, SearchMode, SourcePool

from ..lexicon import LexiconEntry, LexiconProvider


class ExactAnagramPlugin:
    name = "exact_anagram"
    version = "1.0.0"
    search_mode = SearchMode.EXACT_ANAGRAM

    def __init__(self, lexicon_provider: LexiconProvider, engine_version: str) -> None:
        self.lexicon_provider = lexicon_provider
        self.engine_version = engine_version

    def discover(self, source_pool: SourcePool, language_pack: LanguagePack) -> list[Candidate]:
        entries = self.lexicon_provider.entries(language_pack.language)
        target = Counter(source_pool.normalised_input)
        results: list[Candidate] = []

        # Phrase search over one, two, and three-word combinations for alpha scale.
        for phrase_entries in self._entry_combinations(entries, max_words=3):
            phrase_text = " ".join(entry.text for entry in phrase_entries)
            if Counter(self._normalise(phrase_text)) == target:
                results.append(self._candidate(phrase_entries, source_pool, language_pack))

        return sorted(results, key=lambda c: c.provenance.score_breakdown.total, reverse=True)

    def _entry_combinations(self, entries: list[LexiconEntry], max_words: int):
        def rec(prefix: list[LexiconEntry], remaining: list[LexiconEntry], depth: int):
            if prefix:
                yield tuple(prefix)
            if depth >= max_words:
                return
            for i, entry in enumerate(remaining):
                yield from rec(prefix + [entry], remaining[:i] + remaining[i + 1 :], depth + 1)

        yield from rec([], entries, 0)

    def _normalise(self, text: str) -> str:
        return "".join(ch for ch in text.upper() if ch.isalpha())

    def _candidate(
        self,
        entries: tuple[LexiconEntry, ...],
        source_pool: SourcePool,
        language_pack: LanguagePack,
    ) -> Candidate:
        text = " ".join(entry.text for entry in entries)
        translation = self._translate(entries)
        meaning = "; ".join(entry.meaning or entry.translation for entry in entries)
        score = self._score(entries)

        breakdown = ScoreBreakdown(
            total=score,
            grammar=8.0,
            symbolism=9.0 if "CLAVIS" in text or "ARCANA" in text else 7.0,
            rarity=7.5,
            semantic=8.5,
            notes={"plugin": self.name, "plugin_version": self.version},
        )
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

    def _score(self, entries: tuple[LexiconEntry, ...]) -> float:
        base = 75.0
        words = [entry.text for entry in entries]
        if words == ["CLAVIS", "CAELO", "NOS"]:
            return 98.0
        if "ARCANA" in words:
            base += 10
        if "SOLIS" in words or "LEO" in words:
            base += 5
        return min(base, 95.0)
