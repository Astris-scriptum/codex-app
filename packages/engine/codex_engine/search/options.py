from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SearchOptions:
    max_words: int = 4
    max_results: int = 100
    min_word_length: int = 1
    required_words: tuple[str, ...] = ()
    excluded_words: tuple[str, ...] = ()
    deduplicate_permutations: bool = True
