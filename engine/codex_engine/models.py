from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

@dataclass
class Candidate:
    candidate: str
    translation: str = ""
    score: float = 0.0
    language: str = "Latin"
    search_mode: str = "exact_anagram"
    source_pool: str = ""
    review_status: str = "Generated"
    canon_status: str = ""
    provenance: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
