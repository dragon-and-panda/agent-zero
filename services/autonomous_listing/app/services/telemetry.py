from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_SINK = Path(
    os.getenv("LISTING_TELEMETRY_PATH", "/workspace/logs/listings/events.log")
)


class TelemetryClient:
    """
    Minimal JSONL telemetry sink.
    Replace with real observability stack (OpenTelemetry, Honeycomb, etc.) as needed.
    """

    def __init__(self, sink_path: Optional[Path] = None) -> None:
        self._sink = sink_path or DEFAULT_SINK
        self._sink.parent.mkdir(parents=True, exist_ok=True)

    def record_event(
        self,
        event_type: str,
        listing_id: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        event = {
            "ts": time.time(),
            "event": event_type,
            "listing_id": listing_id,
            "data": payload or {},
        }
        with self._sink.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event))
            handle.write("\n")
