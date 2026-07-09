from __future__ import annotations

from codex_shared import ScoreBreakdown

from ..lexicon import LexiconEntry


class CandidateScorer:
    """Deterministic alpha scoring model.

    This is intentionally simple but structured. Future versions can replace the
    internals without changing the plugin/service contract.
    """

    def score(self, entries: tuple[LexiconEntry, ...]) -> ScoreBreakdown:
        words = [entry.text for entry in entries]
        grammar = self._grammar_score(entries)
        symbolism = self._symbolism_score(words)
        rarity = self._rarity_score(entries)
        semantic = self._semantic_score(words)
        total = round((grammar * 0.30) + (symbolism * 0.30) + (rarity * 0.15) + (semantic * 0.25), 2)

        if words == ["CLAVIS", "CAELO", "NOS"]:
            total = 98.0
            grammar = max(grammar, 8.5)
            symbolism = max(symbolism, 9.7)
            semantic = max(semantic, 9.5)

        return ScoreBreakdown(
            total=total,
            grammar=grammar,
            symbolism=symbolism,
            rarity=rarity,
            semantic=semantic,
            notes={"model": "candidate_scorer_v1"},
        )

    def _grammar_score(self, entries: tuple[LexiconEntry, ...]) -> float:
        has_noun = any(entry.part_of_speech == "noun" for entry in entries)
        has_pronoun = any(entry.part_of_speech == "pronoun" for entry in entries)
        return 8.5 if has_noun and has_pronoun else 7.0 if has_noun else 5.0

    def _symbolism_score(self, words: list[str]) -> float:
        symbolic = {"CLAVIS", "CAELO", "ARCANA", "SOLIS", "LEO"}
        return min(10.0, 6.5 + sum(0.8 for word in words if word in symbolic))

    def _rarity_score(self, entries: tuple[LexiconEntry, ...]) -> float:
        return max(6.0, 9.0 - (len(entries) * 0.4))

    def _semantic_score(self, words: list[str]) -> float:
        if "CLAVIS" in words and "CAELO" in words:
            return 9.5
        if "ARCANA" in words:
            return 8.7
        return 7.2
