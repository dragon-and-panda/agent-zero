#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: score.sh legality consent provenance platform_fit margin repeatability automation defensibility time_to_cash" >&2
  exit 64
fi

for value in "$@"; do
  case "$value" in
    low|medium|high) ;;
    *)
      echo "invalid value: $value (expected low|medium|high)" >&2
      exit 65
      ;;
  esac
done

legality="$1"
consent="$2"
provenance="$3"
platform_fit="$4"
margin="$5"
repeatability="$6"
automation="$7"
defensibility="$8"
time_to_cash="$9"

hard_values=("$legality" "$consent" "$provenance" "$platform_fit")
soft_values=("$margin" "$repeatability" "$automation" "$defensibility" "$time_to_cash")

for value in "${hard_values[@]}"; do
  if [ "$value" = "low" ]; then
    echo "REJECT"
    exit 0
  fi
done

for value in "${hard_values[@]}"; do
  if [ "$value" = "medium" ]; then
    echo "HOLD"
    exit 0
  fi
done

soft_high_count=0
for value in "${soft_values[@]}"; do
  if [ "$value" = "low" ]; then
    echo "HOLD"
    exit 0
  fi
  if [ "$value" = "high" ]; then
    soft_high_count=$((soft_high_count + 1))
  fi
done

if [ "$soft_high_count" -ge 3 ]; then
  echo "PASS"
else
  echo "HOLD"
fi
