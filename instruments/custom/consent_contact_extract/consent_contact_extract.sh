#!/bin/bash
set -euo pipefail

INPUT_CSV="${1:-}"
OUTPUT_DIR="${2:-}"
EMAIL_COL="${EMAIL_COL:-email}"
CONSENT_COL="${CONSENT_COL:-consent_status}"
CONSENT_VALUES="${CONSENT_VALUES:-yes,true,1,opted_in,consented}"

if [[ -z "$INPUT_CSV" || -z "$OUTPUT_DIR" ]]; then
  echo "Usage: bash consent_contact_extract.sh <input_csv> <output_dir>"
  echo "Optional env vars: EMAIL_COL, CONSENT_COL, CONSENT_VALUES"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

python3 - "$INPUT_CSV" "$OUTPUT_DIR" "$EMAIL_COL" "$CONSENT_COL" "$CONSENT_VALUES" <<'PY'
import csv
import os
import re
import sys
from collections import Counter

input_csv, output_dir, email_col, consent_col, consent_values = sys.argv[1:]
allowed = {v.strip().lower() for v in consent_values.split(",") if v.strip()}
email_re = re.compile(r"^[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

consented = set()
domains = Counter()
invalid = []

with open(input_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames or []
    missing = [c for c in (email_col, consent_col) if c not in fields]
    if missing:
        raise SystemExit(
            f"Missing required columns: {', '.join(missing)}. Found: {', '.join(fields)}"
        )

    for idx, row in enumerate(reader, start=2):
        consent_value = (row.get(consent_col) or "").strip().lower()
        if consent_value not in allowed:
            continue

        email = (row.get(email_col) or "").strip().lower()
        if not email_re.match(email):
            invalid.append((idx, row.get(email_col, ""), row.get(consent_col, "")))
            continue

        consented.add(email)
        domains[email.split("@", 1)[1]] += 1

emails_path = os.path.join(output_dir, "consented_emails.txt")
with open(emails_path, "w", encoding="utf-8") as f:
    for email in sorted(consented):
        f.write(email + "\n")

domain_path = os.path.join(output_dir, "domain_counts.csv")
with open(domain_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["domain", "count"])
    for domain, count in sorted(domains.items(), key=lambda kv: (-kv[1], kv[0])):
        w.writerow([domain, count])

invalid_path = os.path.join(output_dir, "invalid_rows.csv")
with open(invalid_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["row_number", "email_value", "consent_value"])
    w.writerows(invalid)

print(f"Wrote {len(consented)} consented emails to: {emails_path}")
print(f"Wrote {len(domains)} domain counts to: {domain_path}")
print(f"Wrote {len(invalid)} invalid consented rows to: {invalid_path}")
PY
