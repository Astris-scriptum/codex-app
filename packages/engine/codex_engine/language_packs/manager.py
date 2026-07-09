from __future__ import annotations

import json
from pathlib import Path

from codex_shared import LanguagePack


class LanguagePackManager:
    """Loads language packs from configuration instead of hard-coded Python."""

    def __init__(self, config_root: Path | None = None) -> None:
        if config_root is None:
            config_root = Path(__file__).resolve().parents[1] / "config" / "language_packs"
        self.config_root = Path(config_root)

    def load(self, language_key: str) -> LanguagePack:
        config_path = self.config_root / language_key / "language.json"
        if not config_path.exists():
            raise ValueError(f"Language pack not found: {language_key}")

        data = json.loads(config_path.read_text(encoding="utf-8"))
        return LanguagePack(
            language=data["language"],
            version=data["version"],
            alphabet=data["alphabet"],
            normalisation_rules=tuple(data.get("normalisation_rules", [])),
            transformation_rules=tuple(data.get("transformation_rules", [])),
            scoring_profile=data.get("scoring_profile", "default"),
        )

    def list_available(self) -> list[str]:
        if not self.config_root.exists():
            return []
        return sorted(p.name for p in self.config_root.iterdir() if (p / "language.json").exists())
