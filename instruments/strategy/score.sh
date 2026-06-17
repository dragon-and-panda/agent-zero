#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 7 ]]; then
  cat <<'EOF'
Usage:
  score.sh "<lane_name>" <legality> <consent> <time_to_cash> <automation_fit> <margin> <durability>

Scoring notes:
  - Inputs must be integers from 0 to 10.
  - legality and consent are hard gates.
  - Recommended starting point:
      legality=10 consent=10 time_to_cash=6 automation_fit=8 margin=7 durability=7

Example:
  score.sh "Inbox-to-CRM Hygiene Service" 10 10 7 8 7 8
EOF
  exit 1
fi

lane_name="$1"
shift

labels=("legality" "consent" "time_to_cash" "automation_fit" "margin" "durability")
values=("$@")

for idx in "${!labels[@]}"; do
  value="${values[$idx]}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "error: ${labels[$idx]} must be an integer from 0 to 10" >&2
    exit 2
  fi
  if (( value < 0 || value > 10 )); then
    echo "error: ${labels[$idx]} must be between 0 and 10" >&2
    exit 2
  fi
done

legality="${values[0]}"
consent="${values[1]}"
time_to_cash="${values[2]}"
automation_fit="${values[3]}"
margin="${values[4]}"
durability="${values[5]}"

if (( legality < 8 )); then
  decision="REJECT"
  rationale="Legality score below minimum threshold."
elif (( consent < 8 )); then
  decision="REJECT"
  rationale="Consent score below minimum threshold."
else
  weighted_score=$(( legality * 3 + consent * 3 + time_to_cash * 2 + automation_fit * 2 + margin * 2 + durability * 2 ))
  if (( weighted_score >= 110 )); then
    decision="GO"
    rationale="Lane is legally strong, consent-based, and commercially attractive."
  elif (( weighted_score >= 90 )); then
    decision="HOLD"
    rationale="Lane is promising but needs sharper positioning, proof, or automation."
  else
    decision="REJECT"
    rationale="Lane does not clear the return threshold after compliance gates."
  fi
fi

cat <<EOF
Lane: $lane_name
Decision: $decision
Rationale: $rationale
Inputs:
  legality: $legality
  consent: $consent
  time_to_cash: $time_to_cash
  automation_fit: $automation_fit
  margin: $margin
  durability: $durability
EOF
