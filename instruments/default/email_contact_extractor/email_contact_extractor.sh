#!/bin/bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <input_path> <output_csv> <owner_email> [extra_flags...]"
  exit 1
fi

INPUT_PATH="$1"
OUTPUT_CSV="$2"
OWNER_EMAIL="$3"
shift 3

python -m python.helpers.email_contact_extractor \
  --input "$INPUT_PATH" \
  --out-csv "$OUTPUT_CSV" \
  --owner-email "$OWNER_EMAIL" \
  "$@"
