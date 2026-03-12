#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input.csv> <output.csv>"
  exit 1
fi

INPUT_CSV="$1"
OUTPUT_CSV="$2"

if [ ! -f "$INPUT_CSV" ]; then
  echo "Input file not found: $INPUT_CSV"
  exit 1
fi

python3 - "$INPUT_CSV" "$OUTPUT_CSV" <<'PY'
import csv
import re
import sys
from pathlib import Path

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])

allowed_states = {"opt_in", "transactional_only"}
email_pattern = re.compile(r"^[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}$", re.IGNORECASE)

rows_in = 0
rows_bad_email = 0
rows_filtered_consent = 0
rows_kept = 0

unique = {}

with input_path.open("r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    expected = {"email", "source", "consent_status"}
    if not reader.fieldnames or not expected.issubset(set(reader.fieldnames)):
        raise SystemExit(
            "Input CSV must include columns: email, source, consent_status"
        )

    for row in reader:
        rows_in += 1
        email = (row.get("email") or "").strip().lower()
        source = (row.get("source") or "").strip()
        consent_status = (row.get("consent_status") or "").strip().lower()

        if not email_pattern.match(email):
            rows_bad_email += 1
            continue

        if consent_status not in allowed_states:
            rows_filtered_consent += 1
            continue

        if email not in unique:
            unique[email] = {
                "email": email,
                "source": source or "unknown",
                "consent_status": consent_status,
            }

rows_kept = len(unique)
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["email", "source", "consent_status"])
    writer.writeheader()
    for row in unique.values():
        writer.writerow(row)

print(f"Input rows: {rows_in}")
print(f"Invalid email rows skipped: {rows_bad_email}")
print(f"Rows filtered by consent: {rows_filtered_consent}")
print(f"Output rows: {rows_kept}")
print(f"Saved: {output_path}")
PY

