#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: bash consent_audit.sh <contacts.csv> [mode]"
  echo "mode: outreach (default) or transactional"
  exit 1
fi

CSV_PATH="$1"
MODE="${2:-outreach}"

if [ ! -f "$CSV_PATH" ]; then
  echo "ERROR: CSV file not found: $CSV_PATH"
  exit 1
fi

python3 - "$CSV_PATH" "$MODE" <<'PY'
import csv
import json
import sys
from collections import Counter

csv_path = sys.argv[1]
mode = sys.argv[2]

required = {"email", "contact_status"}
valid_statuses = {"opt_in", "transactional_only", "no_consent", "do_not_contact"}

if mode not in {"outreach", "transactional"}:
    print("ERROR: mode must be 'outreach' or 'transactional'")
    sys.exit(1)

rows = 0
bad_rows = 0
missing_required = []
status_counter = Counter()
eligible = 0
invalid_status_examples = []

with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    if reader.fieldnames is None:
        print("ERROR: CSV has no header row")
        sys.exit(1)

    headers = {h.strip() for h in reader.fieldnames if h is not None}
    missing_required = sorted(required - headers)
    if missing_required:
        print("ERROR: Missing required columns:", ", ".join(missing_required))
        sys.exit(1)

    for idx, row in enumerate(reader, start=2):
        rows += 1
        email = (row.get("email") or "").strip()
        status = (row.get("contact_status") or "").strip()

        if not email:
            bad_rows += 1
            continue

        status_counter[status] += 1
        if status not in valid_statuses:
            bad_rows += 1
            if len(invalid_status_examples) < 5:
                invalid_status_examples.append({"line": idx, "email": email, "status": status})
            continue

        if mode == "outreach":
            if status == "opt_in":
                eligible += 1
        else:
            if status in {"opt_in", "transactional_only"}:
                eligible += 1

summary = {
    "mode": mode,
    "rows_total": rows,
    "rows_invalid": bad_rows,
    "status_counts": dict(status_counter),
    "eligible_rows": eligible,
    "eligible_ratio": (eligible / rows) if rows else 0.0,
    "invalid_status_examples": invalid_status_examples,
}

print(json.dumps(summary, indent=2))

# Fail closed if there are invalid rows; caller must fix data quality first.
if bad_rows > 0:
    sys.exit(2)
PY
