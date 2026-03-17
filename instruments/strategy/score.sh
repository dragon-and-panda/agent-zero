#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh --name NAME --legality N --consent N --automation-fit N \
           --time-to-cash N --margin N --repeatability N --redundancy N \
           --downside-protection N --setup-ease N

All scores use a 0-10 scale where higher is better.
EOF
}

NAME=""
LEGALITY=""
CONSENT=""
AUTOMATION_FIT=""
TIME_TO_CASH=""
MARGIN=""
REPEATABILITY=""
REDUNDANCY=""
DOWNSIDE_PROTECTION=""
SETUP_EASE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --legality)
      LEGALITY="${2:-}"
      shift 2
      ;;
    --consent)
      CONSENT="${2:-}"
      shift 2
      ;;
    --automation-fit)
      AUTOMATION_FIT="${2:-}"
      shift 2
      ;;
    --time-to-cash)
      TIME_TO_CASH="${2:-}"
      shift 2
      ;;
    --margin)
      MARGIN="${2:-}"
      shift 2
      ;;
    --repeatability)
      REPEATABILITY="${2:-}"
      shift 2
      ;;
    --redundancy)
      REDUNDANCY="${2:-}"
      shift 2
      ;;
    --downside-protection)
      DOWNSIDE_PROTECTION="${2:-}"
      shift 2
      ;;
    --setup-ease)
      SETUP_EASE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

for required in \
  NAME LEGALITY CONSENT AUTOMATION_FIT TIME_TO_CASH MARGIN \
  REPEATABILITY REDUNDANCY DOWNSIDE_PROTECTION SETUP_EASE
do
  if [[ -z "${!required}" ]]; then
    echo "Missing required argument: ${required}" >&2
    usage >&2
    exit 1
  fi
done

python3 - "$NAME" "$LEGALITY" "$CONSENT" "$AUTOMATION_FIT" "$TIME_TO_CASH" \
  "$MARGIN" "$REPEATABILITY" "$REDUNDANCY" "$DOWNSIDE_PROTECTION" "$SETUP_EASE" <<'PY'
import json
import sys

name = sys.argv[1]
raw_scores = {
    "legality": sys.argv[2],
    "consent": sys.argv[3],
    "automation_fit": sys.argv[4],
    "time_to_cash": sys.argv[5],
    "margin": sys.argv[6],
    "repeatability": sys.argv[7],
    "redundancy": sys.argv[8],
    "downside_protection": sys.argv[9],
    "setup_ease": sys.argv[10],
}

weights = {
    "legality": 0.18,
    "consent": 0.15,
    "automation_fit": 0.13,
    "time_to_cash": 0.12,
    "margin": 0.11,
    "repeatability": 0.11,
    "redundancy": 0.08,
    "downside_protection": 0.08,
    "setup_ease": 0.04,
}

scores = {}
for key, value in raw_scores.items():
    try:
        parsed = float(value)
    except ValueError as exc:
        raise SystemExit(f"{key} must be numeric: {value}") from exc
    if parsed < 0 or parsed > 10:
        raise SystemExit(f"{key} must be between 0 and 10: {parsed}")
    scores[key] = parsed

weighted_score = sum(scores[key] * weights[key] for key in scores) * 10

if weighted_score >= 85:
    recommendation = "strong_candidate"
elif weighted_score >= 70:
    recommendation = "viable_with_tuning"
elif weighted_score >= 50:
    recommendation = "experiment_only"
else:
    recommendation = "avoid_or_redesign"

sorted_factors = sorted(scores.items(), key=lambda item: item[1], reverse=True)
strongest = [name for name, _ in sorted_factors[:3]]
weakest = [name for name, _ in sorted(scores.items(), key=lambda item: item[1])[:3]]

report = {
    "name": name,
    "weighted_score": round(weighted_score, 1),
    "recommendation": recommendation,
    "scores": scores,
    "weights": weights,
    "strongest_factors": strongest,
    "weakest_factors": weakest,
}

print(json.dumps(report, indent=2, sort_keys=True))
PY
