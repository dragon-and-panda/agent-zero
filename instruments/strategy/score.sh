#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 6 ]]; then
  echo "Usage: $0 legality consent repeatability speed_to_cash leverage defensibility" >&2
  echo "Each input must be an integer from 0 to 10." >&2
  exit 1
fi

names=(
  "legality"
  "consent"
  "repeatability"
  "speed_to_cash"
  "leverage"
  "defensibility"
)

values=("$@")

for i in "${!values[@]}"; do
  value="${values[$i]}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "Invalid ${names[$i]} score: $value" >&2
    exit 1
  fi

  if (( value < 0 || value > 10 )); then
    echo "${names[$i]} must be between 0 and 10." >&2
    exit 1
  fi
done

legality="${values[0]}"
consent="${values[1]}"
repeatability="${values[2]}"
speed_to_cash="${values[3]}"
leverage="${values[4]}"
defensibility="${values[5]}"

if (( legality < 7 )); then
  echo "REJECT"
  echo "Reason: legality score below threshold."
  exit 0
fi

if (( consent < 7 )); then
  echo "REJECT"
  echo "Reason: consent score below threshold."
  exit 0
fi

weighted_score=$(
  python3 - <<'PY' "$legality" "$consent" "$repeatability" "$speed_to_cash" "$leverage" "$defensibility"
import sys

legality, consent, repeatability, speed_to_cash, leverage, defensibility = map(int, sys.argv[1:])
weights = {
    "legality": 0.25,
    "consent": 0.20,
    "repeatability": 0.15,
    "speed_to_cash": 0.15,
    "leverage": 0.15,
    "defensibility": 0.10,
}

score = (
    legality * weights["legality"]
    + consent * weights["consent"]
    + repeatability * weights["repeatability"]
    + speed_to_cash * weights["speed_to_cash"]
    + leverage * weights["leverage"]
    + defensibility * weights["defensibility"]
)

print(f"{score:.2f}")
PY
)

echo "Weighted score: $weighted_score / 10.00"

python3 - <<'PY' "$weighted_score"
import sys

score = float(sys.argv[1])
if score >= 8.0:
    print("GO")
    print("Action: prioritize this lane now.")
elif score >= 6.5:
    print("HOLD")
    print("Action: improve the lane before activation.")
else:
    print("REJECT")
    print("Reason: weighted score below activation threshold.")
PY
