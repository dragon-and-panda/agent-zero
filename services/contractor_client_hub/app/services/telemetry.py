from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class TelemetryClient:
    def __init__(self, sink_path: str) -> None:
        self._sink = Path(sink_path)
        self._sink.parent.mkdir(parents=True, exist_ok=True)

    def record_event(
        self, event_type: str, thread_id: str, payload: dict[str, Any] | None = None
    ) -> None:
        event = {
            "ts": time.time(),
            "event": event_type,
            "thread_id": thread_id,
            "data": payload or {},
        }
        with self._sink.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=True))
            f.write("\n")
