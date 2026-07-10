from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from codex_shared import Candidate


@dataclass(frozen=True)
class SearchEvent:
    event_type: Literal["started", "candidate", "completed", "error"]
    message: str = ""
    candidate: Candidate | None = None
    sequence: int = 0
