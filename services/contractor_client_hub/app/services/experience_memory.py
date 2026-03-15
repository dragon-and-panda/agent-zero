from __future__ import annotations

import json
import threading
from pathlib import Path


class ExperienceMemory:
    """Very small persistence layer that stores lessons learned across threads."""

    def __init__(self, path: str = "/workspace/logs/contract_hub/experience_memory.json") -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._entries = self._load()

    def _load(self) -> list[str]:
        if not self._path.exists():
            return []
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                return [str(x) for x in payload if isinstance(x, str)]
        except Exception:
            return []
        return []

    def _persist(self) -> None:
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(self._entries[-500:], f, ensure_ascii=True, indent=2)

    def add_lesson(self, lesson: str) -> None:
        lesson = lesson.strip()
        if not lesson:
            return
        with self._lock:
            self._entries.append(lesson)
            self._persist()

    def top_hints(self, query: str, limit: int = 5) -> list[str]:
        tokens = {t for t in query.lower().split() if len(t) >= 4}
        with self._lock:
            if not tokens:
                return self._entries[-limit:]
            scored: list[tuple[int, str]] = []
            for entry in self._entries:
                score = sum(1 for t in tokens if t in entry.lower())
                if score > 0:
                    scored.append((score, entry))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [text for _, text in scored[:limit]]
