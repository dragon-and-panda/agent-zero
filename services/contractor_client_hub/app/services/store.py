from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from .. import schemas
from ..config import get_settings


class HubStore:
    """JSON-backed persistence for contract threads.

    This keeps the MVP simple while preserving a durable audit trail.
    """

    def __init__(self, storage_path: str | None = None) -> None:
        self._path = Path(storage_path or get_settings().threads_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._state: dict[str, dict[str, Any]] = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self._path.exists():
            return {}
        try:
            with self._path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            if isinstance(raw, dict):
                return raw
        except Exception:
            return {}
        return {}

    def _persist(self) -> None:
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(self._state, f, ensure_ascii=True, indent=2, sort_keys=True)

    def upsert_thread(self, thread: schemas.ContractThread) -> None:
        with self._lock:
            self._state[thread.thread_id] = thread.model_dump(mode="json")
            self._persist()

    def get_thread(self, thread_id: str) -> schemas.ContractThread | None:
        with self._lock:
            payload = self._state.get(thread_id)
            if not payload:
                return None
            return schemas.ContractThread.model_validate(payload)

    def list_threads(self, limit: int = 100) -> list[schemas.ContractThread]:
        with self._lock:
            values = list(self._state.values())[: max(1, min(limit, 500))]
            return [schemas.ContractThread.model_validate(v) for v in values]
