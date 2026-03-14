#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$#" -eq 0 ]]; then
  echo "Usage:"
  echo "  bash \"$SCRIPT_DIR/email_contact_intel.sh\" --mbox /path/to/mailbox.mbox --owner you@example.com"
  exit 1
fi

python3 "$SCRIPT_DIR/email_contact_intel.py" "$@"
