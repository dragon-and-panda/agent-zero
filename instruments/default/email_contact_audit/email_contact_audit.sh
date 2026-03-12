#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <path-to-mbox> <output-dir> [owned-email-1] [owned-email-2] ..."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MBOX_PATH="$1"
OUTPUT_DIR="$2"
shift 2

OWNED_ARGS=()
for owned_email in "$@"; do
  OWNED_ARGS+=(--owned-email "$owned_email")
done

python3 "$SCRIPT_DIR/extract_contacts.py" \
  --mbox "$MBOX_PATH" \
  --output-dir "$OUTPUT_DIR" \
  "${OWNED_ARGS[@]}"
