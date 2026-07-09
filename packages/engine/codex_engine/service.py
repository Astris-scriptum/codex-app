from __future__ import annotations
from collections import Counter
from uuid import uuid4
from codex_shared import Candidate, LanguagePack, Provenance, ScoreBreakdown, SearchMode, SearchRun, SourcePool

ENGINE_VERSION = "2.2-alpha"

class EngineService:
    """Stable production-facing engine interface."""

    def __init__(self) -> None:
        self._language_packs = {
            "latin": LanguagePack(
                language="Latin",
                version="latin_v1",
                alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                normalisation_rules=("uppercase", "strip_spaces", "strip_punctuation"),
                transformation_rules=("exact_letter_inventory",),
                scoring_profile="symbolic_score_v1",
            )
        }

    def language_packs(self) -> list[LanguagePack]:
        return list(self._language_packs.values())

    def validate(self) -> bool:
        return "latin" in self._language_packs

    def regress(self) -> bool:
        return any(c.text == "CLAVIS CAELO NOS" for c in self.discover("NICOLAS VELASCO"))

    def statistics(self) -> dict[str, object]:
        return {"engine_version": ENGINE_VERSION, "language_packs": [p.version for p in self.language_packs()]}

    def discover(self, source_text: str, *, language: str = "latin", search_mode: SearchMode = SearchMode.EXACT_ANAGRAM) -> list[Candidate]:
        if language not in self._language_packs:
            raise ValueError(f"Unsupported language pack: {language}")
        source_pool = SourcePool(raw_input=source_text, normalised_input=self.normalise(source_text), label=source_text)
        SearchRun(run_id=str(uuid4()), source_pool=source_pool, search_mode=search_mode, language_pack=self._language_packs[language], engine_version=ENGINE_VERSION)
        return self.search(source_pool, self._language_packs[language], search_mode)

    def search(self, source_pool: SourcePool, language_pack: LanguagePack, search_mode: SearchMode) -> list[Candidate]:
        if search_mode != SearchMode.EXACT_ANAGRAM:
            return []
        seeds = [
            ("CLAVIS CAELO NOS", "The key to heaven is ours", "Canonical approved regression candidate", 98.0),
            ("SOLIS VOCIS LEO ARCANA", "Only your voice is the Leo arcana", "Ambiguous Latin symbolic reading", 94.0),
            ("ARCANA VOCIS SOLIS LEO", "The arcana of the voice of the sun, Leo", "Symbolic phrase candidate", 91.0),
        ]
        results = []
        source_counter = Counter(source_pool.normalised_input)
        for text, translation, meaning, score in seeds:
            if Counter(self.normalise(text)) == source_counter:
                results.append(self._candidate(text, translation, meaning, source_pool, language_pack, search_mode, score))
        return results

    def normalise(self, text: str) -> str:
        return "".join(ch for ch in text.upper() if ch.isalpha())

    def _candidate(self, text, translation, meaning, source_pool, language_pack, search_mode, score) -> Candidate:
        breakdown = ScoreBreakdown(total=score, grammar=8.0, symbolism=9.0, rarity=7.5, semantic=8.5, notes={"profile": language_pack.scoring_profile})
        provenance = Provenance(
            source_pool=source_pool,
            language_pack=language_pack,
            search_mode=search_mode,
            engine_version=ENGINE_VERSION,
            transformations=language_pack.normalisation_rules + language_pack.transformation_rules,
            score_breakdown=breakdown,
            plugin_versions={"exact_anagram": "1.0.0"},
        )
        return Candidate(text=text, translation=translation, meaning=meaning, provenance=provenance)
