#!/usr/bin/env bash

set -euo pipefail

lane=""
legality=""
consent=""
provenance=""
tos=""
time_to_value=""
margin=""
repeatability=""
automation=""
defensibility=""

usage() {
  cat <<'EOF'
Usage:
  score.sh --lane NAME \
    --legality low|medium|high \
    --consent low|medium|high \
    --provenance low|medium|high \
    --tos low|medium|high \
    --time low|medium|high \
    --margin low|medium|high \
    --repeatability low|medium|high \
    --automation low|medium|high \
    --defensibility low|medium|high
EOF
}

value_of() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
    *)
      echo "Invalid value: $1" >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lane)
      lane="${2:-}"
      shift 2
      ;;
    --legality)
      legality="${2:-}"
      shift 2
      ;;
    --consent)
      consent="${2:-}"
      shift 2
      ;;
    --provenance)
      provenance="${2:-}"
      shift 2
      ;;
    --tos)
      tos="${2:-}"
      shift 2
      ;;
    --time)
      time_to_value="${2:-}"
      shift 2
      ;;
    --margin)
      margin="${2:-}"
      shift 2
      ;;
    --repeatability)
      repeatability="${2:-}"
      shift 2
      ;;
    --automation)
      automation="${2:-}"
      shift 2
      ;;
    --defensibility)
      defensibility="${2:-}"
      shift 2
      ;;
    --help|-h)
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

required=(
  "$lane"
  "$legality"
  "$consent"
  "$provenance"
  "$tos"
  "$time_to_value"
  "$margin"
  "$repeatability"
  "$automation"
  "$defensibility"
)

for item in "${required[@]}"; do
  if [[ -z "$item" ]]; then
    usage >&2
    exit 1
  fi
done

legality_score="$(value_of "$legality")"
consent_score="$(value_of "$consent")"
provenance_score="$(value_of "$provenance")"
tos_score="$(value_of "$tos")"
time_score="$(value_of "$time_to_value")"
margin_score="$(value_of "$margin")"
repeatability_score="$(value_of "$repeatability")"
automation_score="$(value_of "$automation")"
defensibility_score="$(value_of "$defensibility")"

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" || "$tos" == "low" ]]; then
  echo "Lane: $lane"
  echo "Decision: REJECT"
  echo "Reason: failed hard gate (legality, consent, provenance, or TOS alignment)."
  exit 0
fi

total=$(( \
  legality_score * 3 + \
  consent_score * 3 + \
  provenance_score * 2 + \
  tos_score * 2 + \
  time_score * 2 + \
  margin_score * 2 + \
  repeatability_score * 2 + \
  automation_score * 2 + \
  defensibility_score * 1 \
))

max_total=34

decision="HOLD"
reason="compliant lane, but it needs stronger economics or automation before activation."

if (( total >= 25 )); then
  decision="PASS"
  reason="cleared hard gates and scored strongly on repeatability, economics, and automation fit."
elif (( total < 18 )); then
  decision="REJECT"
  reason="compliant on paper, but too weak to justify activation right now."
fi

echo "Lane: $lane"
echo "Decision: $decision"
echo "Score: $total/$max_total"
echo "Reason: $reason"
