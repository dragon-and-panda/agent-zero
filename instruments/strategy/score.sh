#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality consent provenance tos_risk time_to_cash margin repeatability automation defensibility [notes...]

Each input must be one of:
  low | medium | high

Interpretation:
  - legality, consent, provenance, time_to_cash, margin, repeatability, automation, defensibility:
      high is good
  - tos_risk:
      low is good

Outputs:
  PASS   -> compliant and operationally attractive
  HOLD   -> compliant enough to explore, but not attractive enough to activate
  REJECT -> fails legality, consent, provenance, or platform-risk gates
EOF
}

if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ "$#" -lt 9 ]]; then
  usage >&2
  exit 1
fi

expect_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "Invalid level: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

legality="$1"
consent="$2"
provenance="$3"
tos_risk="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"
notes="${10-}"

for value in "$legality" "$consent" "$provenance" "$tos_risk" "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"; do
  expect_level "$value"
done

high_soft_factors=0

# Hard reject gates first.
if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" ]]; then
  echo "REJECT"
  exit 0
fi

if [[ "$tos_risk" == "high" ]]; then
  echo "REJECT"
  exit 0
fi

# Soft commercial screen.
if [[ "$time_to_cash" == "low" || "$margin" == "low" || "$repeatability" == "low" || "$automation" == "low" || "$defensibility" == "low" ]]; then
  echo "HOLD"
  exit 0
fi

for value in "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$value" == "high" ]]; then
    high_soft_factors=$((high_soft_factors + 1))
  fi
done

if [[ "$legality" == "high" && "$consent" == "high" && "$provenance" == "high" && "$high_soft_factors" -ge 3 ]]; then
  echo "PASS"
else
  echo "HOLD"
fi
