from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

class CandidateStatus(str, Enum):
    GENERATED = "generated"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANONICAL = "canonical"

class SearchMode(str, Enum):
    EXACT_ANAGRAM = "exact_anagram"
    PARTIAL_ANAGRAM = "partial_anagram"
    PHRASE_CONSTRUCTION = "phrase_construction"
    HIDDEN_WORDS = "hidden_words"
    ACROSTIC = "acrostic"
    FUZZY = "fuzzy"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class SourcePool:
    raw_input: str
    normalised_input: str
    pool_id: str = field(default_factory=lambda: str(uuid4()))
    label: str | None = None

@dataclass(frozen=True)
class ScoreBreakdown:
    total: float
    grammar: float = 0.0
    symbolism: float = 0.0
    rarity: float = 0.0
    semantic: float = 0.0
    notes: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class LanguagePack:
    language: str
    version: str
    alphabet: str
    normalisation_rules: tuple[str, ...] = ()
    transformation_rules: tuple[str, ...] = ()
    scoring_profile: str = "default"

@dataclass(frozen=True)
class Provenance:
    source_pool: SourcePool
    language_pack: LanguagePack
    search_mode: SearchMode
    engine_version: str
    transformations: tuple[str, ...]
    score_breakdown: ScoreBreakdown
    timestamp: str = field(default_factory=utc_now_iso)
    plugin_versions: dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class Candidate:
    text: str
    translation: str
    meaning: str
    provenance: Provenance
    candidate_id: str = field(default_factory=lambda: str(uuid4()))
    status: CandidateStatus = CandidateStatus.GENERATED
    comments: str = ""

@dataclass(frozen=True)
class SearchRun:
    run_id: str
    source_pool: SourcePool
    search_mode: SearchMode
    language_pack: LanguagePack
    engine_version: str
    started_at: str = field(default_factory=utc_now_iso)
    finished_at: str | None = None
    candidate_count: int = 0
