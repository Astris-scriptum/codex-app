from __future__ import annotations

from dataclasses import dataclass

from ..lexicon import LexiconEntry
from .inventory import LetterInventory


@dataclass(frozen=True)
class SolverConfig:
    max_words: int = 4
    max_results: int = 500
    require_full_inventory: bool = True


class RecursiveExactAnagramSolver:
    """Deterministic recursive solver for exact phrase anagrams.

    The solver works over indexed lexicon entries and prunes branches whose
    inventory cannot fit inside the remaining source inventory.
    """

    def __init__(self, config: SolverConfig | None = None) -> None:
        self.config = config or SolverConfig()

    def solve(self, source_text: str, entries: list[LexiconEntry]) -> list[tuple[LexiconEntry, ...]]:
        target = LetterInventory.from_text(source_text)
        indexed = []
        for entry in entries:
            inv = LetterInventory.from_text(entry.text)
            if target.contains(inv):
                indexed.append((entry, inv))

        indexed.sort(key=lambda item: (len(item[0].text), item[0].text))
        results: list[tuple[LexiconEntry, ...]] = []

        def walk(
            remaining: LetterInventory,
            start_index: int,
            phrase: list[LexiconEntry],
        ) -> None:
            if len(results) >= self.config.max_results:
                return

            if remaining.is_empty():
                results.append(tuple(phrase))
                return

            if len(phrase) >= self.config.max_words:
                return

            for i in range(start_index, len(indexed)):
                entry, inventory = indexed[i]
                if remaining.contains(inventory):
                    walk(remaining.subtract(inventory), 0, phrase + [entry])

        walk(target, 0, [])
        return self._dedupe(results)

    def _dedupe(self, phrases: list[tuple[LexiconEntry, ...]]) -> list[tuple[LexiconEntry, ...]]:
        seen: set[tuple[str, ...]] = set()
        deduped: list[tuple[LexiconEntry, ...]] = []
        for phrase in phrases:
            key = tuple(entry.text for entry in phrase)
            if key not in seen:
                seen.add(key)
                deduped.append(phrase)
        return deduped
