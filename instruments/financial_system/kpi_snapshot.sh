#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: bash kpi_snapshot.sh <events.jsonl>"
  exit 1
fi

EVENT_PATH="$1"

if [ ! -f "$EVENT_PATH" ]; then
  echo "ERROR: events file not found: $EVENT_PATH"
  exit 1
fi

python3 - "$EVENT_PATH" <<'PY'
import json
import sys
from collections import Counter

path = sys.argv[1]

events_total = 0
event_names = Counter()
revenue = 0.0
errors = 0
publish_success = 0
publish_fail = 0

with open(path, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            errors += 1
            continue

        events_total += 1
        event = obj.get("event") or obj.get("type") or "unknown"
        event_names[event] += 1

        payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}

        # Revenue harvesting: support common keys.
        value = payload.get("revenue_usd")
        if isinstance(value, (int, float)):
            revenue += float(value)

        if event in {"publish.success", "listing.publication_triggered"}:
            publish_success += 1
        if event in {"publish.failed", "publish.error"}:
            publish_fail += 1

summary = {
    "events_total": events_total,
    "parse_errors": errors,
    "revenue_usd": round(revenue, 2),
    "publish_success_events": publish_success,
    "publish_failure_events": publish_fail,
    "top_events": event_names.most_common(10),
}

print(json.dumps(summary, indent=2))
PY
