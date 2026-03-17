#!/bin/bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "Usage: $0 <name> <compliance> <time_to_cash> <automation_leverage> <margin> <repeatability> <resilience> <strategic_fit> <capital_efficiency>" >&2
  exit 1
fi

NAME="$1"
shift

FIELDS=(
  "compliance"
  "time_to_cash"
  "automation_leverage"
  "margin"
  "repeatability"
  "resilience"
  "strategic_fit"
  "capital_efficiency"
)

VALUES=("$@")

for i in "${!VALUES[@]}"; do
  value="${VALUES[$i]}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "Invalid ${FIELDS[$i]} score '$value': must be an integer from 0 to 10." >&2
    exit 1
  fi
  if [ "$value" -lt 0 ] || [ "$value" -gt 10 ]; then
    echo "Invalid ${FIELDS[$i]} score '$value': must be between 0 and 10." >&2
    exit 1
  fi
done

COMPLIANCE="${VALUES[0]}"
TIME_TO_CASH="${VALUES[1]}"
AUTOMATION="${VALUES[2]}"
MARGIN="${VALUES[3]}"
REPEATABILITY="${VALUES[4]}"
RESILIENCE="${VALUES[5]}"
STRATEGIC_FIT="${VALUES[6]}"
CAPITAL_EFFICIENCY="${VALUES[7]}"

if [ "$COMPLIANCE" -lt 8 ]; then
  printf 'Opportunity: %s\nStatus: REJECTED\nReason: compliance score below minimum threshold (8/10).\n' "$NAME"
  exit 2
fi

python3 - "$NAME" "$COMPLIANCE" "$TIME_TO_CASH" "$AUTOMATION" "$MARGIN" "$REPEATABILITY" "$RESILIENCE" "$STRATEGIC_FIT" "$CAPITAL_EFFICIENCY" <<'PY'
import json
import sys

name = sys.argv[1]
scores = {
    "compliance": int(sys.argv[2]),
    "time_to_cash": int(sys.argv[3]),
    "automation_leverage": int(sys.argv[4]),
    "margin": int(sys.argv[5]),
    "repeatability": int(sys.argv[6]),
    "resilience": int(sys.argv[7]),
    "strategic_fit": int(sys.argv[8]),
    "capital_efficiency": int(sys.argv[9]),
}

weights = {
    "compliance": 2.2,
    "time_to_cash": 1.4,
    "automation_leverage": 1.2,
    "margin": 1.1,
    "repeatability": 1.1,
    "resilience": 1.3,
    "strategic_fit": 1.2,
    "capital_efficiency": 1.0,
}

weighted_sum = sum(scores[key] * weights[key] for key in scores)
max_sum = sum(10 * weights[key] for key in weights)
overall = round((weighted_sum / max_sum) * 100, 1)

if overall >= 85:
    recommendation = "launch_now"
elif overall >= 75:
    recommendation = "pilot_next"
elif overall >= 65:
    recommendation = "improve_then_revisit"
else:
    recommendation = "deprioritize"

result = {
    "opportunity": name,
    "status": "approved_for_comparison",
    "overall_score": overall,
    "recommendation": recommendation,
    "scores": scores,
    "weights": weights,
}

print(json.dumps(result, indent=2, sort_keys=True))
PY
