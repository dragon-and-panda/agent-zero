#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: $0 <input.csv> [output.csv]"
  exit 1
fi

INPUT_CSV="$1"
OUTPUT_CSV="${2:-opportunity_scores.csv}"

python3 - "$INPUT_CSV" "$OUTPUT_CSV" <<'PY'
import csv
import sys

in_path = sys.argv[1]
out_path = sys.argv[2]

required = [
    "name",
    "market_demand",
    "margin_potential",
    "execution_speed",
    "compliance_risk",
    "automation_fit",
]

weights = {
    "market_demand": 0.30,
    "margin_potential": 0.25,
    "execution_speed": 0.20,
    "compliance_risk": -0.30,
    "automation_fit": 0.25,
}

rows = []
with open(in_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    missing = [c for c in required if c not in (reader.fieldnames or [])]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    for row in reader:
        score = 0.0
        for key, weight in weights.items():
            score += float(row[key]) * weight
        row["composite_score"] = round(score, 4)
        rows.append(row)

rows.sort(key=lambda r: r["composite_score"], reverse=True)

out_fields = list(rows[0].keys()) if rows else required + ["composite_score"]
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out_path}")
print("Top opportunities:")
for row in rows[:5]:
    print(f"- {row['name']}: {row['composite_score']}")
PY
