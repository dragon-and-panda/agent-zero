#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 9 ]]; then
  echo "Usage: $0 <legality> <consent> <provenance> <tos> <time> <margin> <repeatability> <automation> <defensibility>" >&2
  echo "Each value must be: high, medium, or low" >&2
  exit 2
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | xargs)"
  case "$value" in
    high|medium|low)
      printf '%s' "$value"
      ;;
    *)
      echo "invalid:$value"
      ;;
  esac
}

score_value() {
  case "$1" in
    high) echo 3 ;;
    medium) echo 2 ;;
    low) echo 1 ;;
    *) echo 0 ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
time_to_revenue="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

for value in \
  "$legality" "$consent" "$provenance" "$tos" \
  "$time_to_revenue" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$value" == invalid:* ]]; then
    echo "Invalid rating: ${value#invalid:}" >&2
    exit 2
  fi
done

hard_fail=0
hard_holds=0
soft_low=0

for value in "$legality" "$consent" "$provenance" "$tos"; do
  if [[ "$value" == "low" ]]; then
    hard_fail=1
  elif [[ "$value" == "medium" ]]; then
    hard_holds=$((hard_holds + 1))
  fi
done

for value in "$time_to_revenue" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$value" == "low" ]]; then
    soft_low=$((soft_low + 1))
  fi
done

hard_total=$(( \
  $(score_value "$legality") + \
  $(score_value "$consent") + \
  $(score_value "$provenance") + \
  $(score_value "$tos") \
))

soft_total=$(( \
  $(score_value "$time_to_revenue") + \
  $(score_value "$margin") + \
  $(score_value "$repeatability") + \
  $(score_value "$automation") + \
  $(score_value "$defensibility") \
))

total=$((hard_total + soft_total))

decision="HOLD"
reason="Hard gates are acceptable but execution quality needs work."

if [[ $hard_fail -eq 1 ]]; then
  decision="REJECT"
  reason="At least one hard gate failed."
elif [[ $hard_holds -gt 0 ]]; then
  decision="HOLD"
  reason="Hard gates are not yet strong enough for activation."
elif [[ $soft_low -gt 0 ]]; then
  decision="HOLD"
  reason="Hard gates passed, but at least one soft factor is low."
else
  decision="PASS"
  reason="All hard gates are high and soft factors are at least medium."
fi

printf 'decision=%s\n' "$decision"
printf 'reason=%s\n' "$reason"
printf 'hard_score=%s/12\n' "$hard_total"
printf 'soft_score=%s/15\n' "$soft_total"
printf 'total_score=%s/27\n' "$total"
