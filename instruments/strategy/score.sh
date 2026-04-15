#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh LEGALITY CONSENT TIME_TO_CASH MARGIN AUTOMATION_FIT REPEATABILITY

Or:
  score.sh legality=10 consent=10 time_to_cash=8 margin=7 automation_fit=9 repeatability=8

Scores must be numbers from 0 to 10.
Hard gates:
  - legality < 8 => REJECT
  - consent < 8 => REJECT
EOF
}

validate_score() {
  local label="$1"
  local value="$2"

  if ! [[ "$value" =~ ^([0-9]|10)(\.[0-9]+)?$ ]]; then
    echo "Invalid ${label} score: ${value}. Expected a number between 0 and 10." >&2
    exit 1
  fi
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

legality=""
consent=""
time_to_cash=""
margin=""
automation_fit=""
repeatability=""

if [[ "$#" -eq 6 && "${1}" != *=* ]]; then
  legality="$1"
  consent="$2"
  time_to_cash="$3"
  margin="$4"
  automation_fit="$5"
  repeatability="$6"
else
  for arg in "$@"; do
    case "$arg" in
      legality=*) legality="${arg#*=}" ;;
      consent=*) consent="${arg#*=}" ;;
      time_to_cash=*) time_to_cash="${arg#*=}" ;;
      margin=*) margin="${arg#*=}" ;;
      automation_fit=*) automation_fit="${arg#*=}" ;;
      repeatability=*) repeatability="${arg#*=}" ;;
      *)
        echo "Unknown argument: $arg" >&2
        usage
        exit 1
        ;;
    esac
  done
fi

for pair in \
  "legality:$legality" \
  "consent:$consent" \
  "time_to_cash:$time_to_cash" \
  "margin:$margin" \
  "automation_fit:$automation_fit" \
  "repeatability:$repeatability"; do
  label="${pair%%:*}"
  value="${pair#*:}"
  if [[ -z "$value" ]]; then
    echo "Missing required score: $label" >&2
    usage
    exit 1
  fi
  validate_score "$label" "$value"
done

weighted_score="$(awk \
  -v legality="$legality" \
  -v consent="$consent" \
  -v time_to_cash="$time_to_cash" \
  -v margin="$margin" \
  -v automation_fit="$automation_fit" \
  -v repeatability="$repeatability" \
  'BEGIN {
    score = (legality * 0.20) + (consent * 0.20) + (time_to_cash * 0.15) + (margin * 0.15) + (automation_fit * 0.15) + (repeatability * 0.15);
    printf "%.2f", score;
  }')"

decision="HOLD"
reason="Opportunity is viable but needs refinement before activation."

if awk "BEGIN { exit !($legality < 8) }"; then
  decision="REJECT"
  reason="Legality score failed the hard gate."
elif awk "BEGIN { exit !($consent < 8) }"; then
  decision="REJECT"
  reason="Consent score failed the hard gate."
elif awk "BEGIN { exit !($weighted_score >= 7.50) }"; then
  decision="GO"
  reason="Passed hard gates and scored strongly enough for a pilot."
elif awk "BEGIN { exit !($weighted_score < 6.00) }"; then
  decision="REJECT"
  reason="Passed hard gates but unit economics or fit are too weak."
fi

printf 'Decision: %s\n' "$decision"
printf 'Weighted score: %s/10.00\n' "$weighted_score"
printf 'Legality gate: %s\n' "$legality"
printf 'Consent gate: %s\n' "$consent"
printf 'Time to cash: %s\n' "$time_to_cash"
printf 'Margin: %s\n' "$margin"
printf 'Automation fit: %s\n' "$automation_fit"
printf 'Repeatability: %s\n' "$repeatability"
printf 'Rationale: %s\n' "$reason"
