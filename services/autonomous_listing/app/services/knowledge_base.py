from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List


class KnowledgeBase:
    """
    Lightweight reader over the repo's knowledge packs.
    Provides trimmed snippets that can be injected into prompts or compliance checks.
    """

    def __init__(self, base_path: Path | None = None) -> None:
        repo_root = Path(__file__).resolve().parents[5]
        default_base = repo_root / "knowledge" / "custom" / "main"
        self._base_path = base_path or default_base

    def get_listing_references(self, limit: int = 3) -> List[str]:
        """
        Returns a small collection of high-signal snippets for prompts / RAG calls.
        """
        snippets: List[str] = []
        for label, rel_path in [
            ("Policy", "policies/marketplace_policy_pack.md"),
            ("Tone", "policies/listing_voice_tone.md"),
            ("SOP", "sops/listing_creation_sop.md"),
        ]:
            text = self._read(rel_path)
            if not text:
                continue
            excerpt = self._summarize(text)
            snippets.append(f"{label} guidance:\n{excerpt}")
            if len(snippets) >= limit:
                break
        return snippets

    def get_policy_text(self) -> str:
        return self._read("policies/marketplace_policy_pack.md")

    def get_voice_guide(self) -> str:
        return self._read("policies/listing_voice_tone.md")

    def _read(self, relative_path: str) -> str:
        path = self._base_path / relative_path
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8").strip()

    @staticmethod
    def _summarize(text: str, max_chars: int = 1200) -> str:
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3] + "..."


@lru_cache
def get_knowledge_base() -> KnowledgeBase:
    return KnowledgeBase()
