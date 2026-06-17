#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash /workspace/instruments/strategy/score.sh /path/to/opportunities.csv" >&2
  exit 1
fi

csv_path="$1"

if [[ ! -f "$csv_path" ]]; then
  echo "CSV file not found: $csv_path" >&2
  exit 1
fi

python3 - "$csv_path" <<'PY'
import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])

weights = {
    "legality": 2.0,
    "consent": 2.0,
    "data_rights": 1.5,
    "autonomy_fit": 1.25,
    "time_to_cash": 1.0,
    "margin": 1.0,
    "distribution": 0.75,
    "defensibility": 1.0,
    "complexity": -0.75,
}

required = ["name", *weights.keys()]
rows = []

with path.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    if reader.fieldnames is None:
        raise SystemExit("CSV is missing a header row.")

    missing = [field for field in required if field not in reader.fieldnames]
    if missing:
        raise SystemExit(f"CSV is missing required columns: {', '.join(missing)}")

    for index, row in enumerate(reader, start=2):
        parsed = {"name": row["name"].strip()}
        if not parsed["name"]:
            raise SystemExit(f"Row {index}: name is required.")

        for field in weights:
            raw_value = row[field].strip()
            try:
                value = float(raw_value)
            except ValueError as exc:
                raise SystemExit(f"Row {index}: {field} must be numeric, got {raw_value!r}") from exc

            if not 0 <= value <= 10:
                raise SystemExit(f"Row {index}: {field} must be between 0 and 10, got {value}")
            parsed[field] = value

        gating_failures = [
            field for field in ("legality", "consent", "data_rights")
            if parsed[field] < 7
        ]

        score = sum(parsed[field] * weight for field, weight in weights.items())
        parsed["score"] = round(score, 2)
        parsed["status"] = "REJECT" if gating_failures else "PASS"
        parsed["notes"] = (
            "Fails gate: " + ", ".join(gating_failures)
            if gating_failures
            else "Eligible for activation review"
        )
        rows.append(parsed)

if not rows:
    raise SystemExit("CSV contains no opportunity rows.")

rows.sort(key=lambda item: (item["status"] != "PASS", -item["score"], item["name"].lower()))

headers = ["rank", "name", "status", "score", "notes"]
display_rows = []
for rank, row in enumerate(rows, start=1):
    display_rows.append([
        str(rank),
        row["name"],
        row["status"],
        f'{row["score"]:.2f}',
        row["notes"],
    ])

widths = []
for column_index, header in enumerate(headers):
    content_width = max(len(r[column_index]) for r in display_rows)
    widths.append(max(len(header), content_width))

def fmt_line(values):
    return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))

print(fmt_line(headers))
print("-+-".join("-" * width for width in widths))
for row in display_rows:
    print(fmt_line(row))
PY
