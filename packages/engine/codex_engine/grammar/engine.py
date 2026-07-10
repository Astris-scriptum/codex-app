from __future__ import annotations

from dataclasses import dataclass

from ..lexicon import LexiconEntry


@dataclass(frozen=True)
class GrammarAssessment:
    valid: bool
    score: float
    notes: tuple[str, ...] = ()


class GrammarEngine:
    """Alpha grammar validator.

    This is intentionally conservative and configurable later. It creates a
    stable grammar boundary before deeper Latin morphology is introduced.
    """

    def assess(self, entries: tuple[LexiconEntry, ...]) -> GrammarAssessment:
        if not entries:
            return GrammarAssessment(False, 0.0, ("empty phrase",))

        notes: list[str] = []
        parts = [entry.part_of_speech for entry in entries]
        has_noun = "noun" in parts
        has_pronoun = "pronoun" in parts

        score = 6.0
        if has_noun:
            score += 1.5
            notes.append("contains noun")
        if has_pronoun:
            score += 1.0
            notes.append("contains pronoun")
        if len(entries) <= 4:
            score += 0.5
            notes.append("phrase length acceptable")

        return GrammarAssessment(True, min(score, 10.0), tuple(notes))
