#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 9 ]]; then
  echo "usage: $0 <legality> <consent> <provenance> <platform_risk> <time> <margin> <repeatability> <automation> <defensibility>" >&2
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
      echo "invalid score: $1 (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform_risk="$(normalize "$4")"
time="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

hard_scores=("$legality" "$consent" "$provenance" "$platform_risk")
soft_scores=("$time" "$margin" "$repeatability" "$automation" "$defensibility")

for score in "${hard_scores[@]}"; do
  if [[ "$score" == "low" ]]; then
    echo "REJECT"
    exit 0
  fi
done

soft_lows=0
soft_highs=0

for score in "${soft_scores[@]}"; do
  if [[ "$score" == "low" ]]; then
    ((soft_lows+=1))
  fi
  if [[ "$score" == "high" ]]; then
    ((soft_highs+=1))
  fi
done

if [[ "$soft_lows" -eq 0 && "$soft_highs" -ge 3 ]]; then
  echo "PASS"
else
  echo "HOLD"
fi
