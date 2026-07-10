from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from codex_shared import Candidate


class CandidateRepository:
    """Simple JSONL candidate persistence.

    This gives Codex durable candidate history before introducing a richer
    workspace database.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, candidate: Candidate) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(candidate), ensure_ascii=False, default=str) + "\n")

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
