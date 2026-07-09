from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class LetterInventory:
    letters: tuple[tuple[str, int], ...]

    @classmethod
    def from_text(cls, text: str) -> "LetterInventory":
        normalised = "".join(ch for ch in text.upper() if ch.isalpha())
        return cls(tuple(sorted(Counter(normalised).items())))

    @classmethod
    def from_counter(cls, counter: Counter[str]) -> "LetterInventory":
        return cls(tuple(sorted((k, v) for k, v in counter.items() if v > 0)))

    def to_counter(self) -> Counter[str]:
        return Counter(dict(self.letters))

    def contains(self, other: "LetterInventory") -> bool:
        left = self.to_counter()
        right = other.to_counter()
        return all(left[ch] >= count for ch, count in right.items())

    def subtract(self, other: "LetterInventory") -> "LetterInventory":
        if not self.contains(other):
            raise ValueError("Cannot subtract inventory that is not contained.")
        result = self.to_counter()
        result.subtract(other.to_counter())
        return LetterInventory.from_counter(result)

    def is_empty(self) -> bool:
        return not self.letters
