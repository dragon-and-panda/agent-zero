#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "Usage: $0 legality consent provenance tos time margin repeatability automation defensibility" >&2
  echo "Each value must be: low | medium | high" >&2
  exit 2
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s\n' "$value"
      ;;
    *)
      echo "Invalid score: $1" >&2
      exit 2
      ;;
  esac
}

score_value() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
time_to_cash="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

# Reject immediately when the lane fails any hard compliance gate.
if [ "$legality" = "low" ] || [ "$consent" = "low" ] || [ "$provenance" = "low" ] || [ "$tos" = "low" ]; then
  echo "REJECT"
  exit 0
fi

soft_total=0
for value in "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"; do
  soft_total=$((soft_total + $(score_value "$value")))
done

# Preserve a meaningful HOLD state: any weak execution factor prevents PASS.
for value in "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [ "$value" = "low" ]; then
    echo "HOLD"
    exit 0
  fi
done

if [ "$soft_total" -ge 12 ]; then
  echo "PASS"
else
  echo "HOLD"
fi
