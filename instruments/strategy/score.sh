#!/bin/bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 opportunities.csv" >&2
  exit 1
fi

INPUT="$1"
if [[ ! -f "$INPUT" ]]; then
  echo "Input file not found: $INPUT" >&2
  exit 1
fi

python3 - "$INPUT" <<'PY'
import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])
required = [
    "opportunity",
    "legality",
    "time_to_cash",
    "automation_fit",
    "margin",
    "repeatability",
    "downside_safety",
]
weights = {
    "legality": 0.30,
    "time_to_cash": 0.20,
    "automation_fit": 0.15,
    "margin": 0.15,
    "repeatability": 0.10,
    "downside_safety": 0.10,
}

with path.open(newline="", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    missing = [name for name in required if name not in (reader.fieldnames or [])]
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(missing)}")

    rows = []
    for idx, row in enumerate(reader, start=2):
        try:
            metrics = {name: float(row[name]) for name in required[1:]}
        except ValueError as exc:
            raise SystemExit(f"Row {idx}: invalid numeric value ({exc})") from exc

        score = 10 * sum(metrics[name] * weight for name, weight in weights.items())
        if metrics["legality"] < 7 or metrics["downside_safety"] < 5:
            decision = "REJECT"
        elif score >= 75:
            decision = "GO"
        elif score >= 60:
            decision = "HOLD"
        else:
            decision = "REJECT"

        rows.append((row["opportunity"], score, decision))

rows.sort(key=lambda item: item[1], reverse=True)
print(f"Scored {len(rows)} opportunities from {path}")
print("=" * 72)
print(f"{'Opportunity':40} {'Score':>8} {'Decision':>10}")
print("-" * 72)
for opportunity, score, decision in rows:
    label = (opportunity[:37] + "...") if len(opportunity) > 40 else opportunity
    print(f"{label:40} {score:8.1f} {decision:>10}")
PY
