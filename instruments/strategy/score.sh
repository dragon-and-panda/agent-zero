#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: $0 legality consent provenance platform time margin repeatability automation defensibility" >&2
  echo "values: low medium high" >&2
  exit 1
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s\n' "$value"
      ;;
    *)
      echo "invalid value: $1" >&2
      exit 1
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform="$(normalize "$4")"
time_to_cash="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

hard_factors=("$legality" "$consent" "$provenance" "$platform")
for factor in "${hard_factors[@]}"; do
  if [ "$factor" = "low" ]; then
    echo "REJECT"
    exit 0
  fi
done

soft_factors=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility")
high_count=0

for factor in "${soft_factors[@]}"; do
  if [ "$factor" = "low" ]; then
    echo "HOLD"
    exit 0
  fi
  if [ "$factor" = "high" ]; then
    high_count=$((high_count + 1))
  fi
done

if [ "$high_count" -ge 3 ]; then
  echo "PASS"
else
  echo "HOLD"
fi
