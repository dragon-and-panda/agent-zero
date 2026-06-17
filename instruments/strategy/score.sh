#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "Usage: $0 <legality> <consent> <provenance> <tos> <time> <margin> <repeatability> <automation> <defensibility>"
  echo "Each value must be one of: low medium high"
  exit 2
fi

levels=("low" "medium" "high")

is_level() {
  local value="$1"
  local level
  for level in "${levels[@]}"; do
    if [ "$value" = "$level" ]; then
      return 0
    fi
  done
  return 1
}

count_value() {
  local needle="$1"
  shift
  local total=0
  local value
  for value in "$@"; do
    if [ "$value" = "$needle" ]; then
      total=$((total + 1))
    fi
  done
  echo "$total"
}

legality="$1"
consent="$2"
provenance="$3"
tos="$4"
time="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

for value in "$@"; do
  if ! is_level "$value"; then
    echo "ERROR: invalid value '$value'. Use only: low medium high"
    exit 2
  fi
done

hard_values=("$legality" "$consent" "$provenance" "$tos")
soft_values=("$time" "$margin" "$repeatability" "$automation" "$defensibility")

for gate in "${hard_values[@]}"; do
  if [ "$gate" != "high" ]; then
    echo "RESULT: REJECT"
    echo "Reason: one or more hard gates failed."
    echo "Hard gates must all be 'high' for legality, consent, provenance, and tos."
    exit 0
  fi
done

soft_lows="$(count_value low "${soft_values[@]}")"
soft_highs="$(count_value high "${soft_values[@]}")"

if [ "$soft_lows" -gt 0 ]; then
  echo "RESULT: HOLD"
  echo "Reason: hard gates passed, but at least one soft factor is low."
  echo "Soft highs: $soft_highs/5"
  exit 0
fi

if [ "$soft_highs" -ge 3 ]; then
  echo "RESULT: PASS"
  echo "Reason: hard gates passed, no soft factors are low, and the lane is operationally attractive."
  echo "Soft highs: $soft_highs/5"
  exit 0
fi

echo "RESULT: HOLD"
echo "Reason: hard gates passed, but the lane is still too average to prioritize."
echo "Soft highs: $soft_highs/5"
