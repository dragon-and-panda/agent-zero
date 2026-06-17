#!/bin/bash

set -euo pipefail

if [ "$#" -ne 7 ]; then
  echo "Usage: $0 \"lane name\" legality consent time_to_cash automation_fit complexity defensibility"
  exit 1
fi

lane_name="$1"
legality="$2"
consent="$3"
time_to_cash="$4"
automation_fit="$5"
complexity="$6"
defensibility="$7"

python3 - "$lane_name" "$legality" "$consent" "$time_to_cash" "$automation_fit" "$complexity" "$defensibility" <<'PY'
import sys

lane_name = sys.argv[1]
scores = list(map(int, sys.argv[2:]))
legality, consent, time_to_cash, automation_fit, complexity, defensibility = scores

for value in scores:
    if value < 1 or value > 10:
        raise SystemExit("All scores must be integers between 1 and 10.")

if legality < 8 or consent < 8:
    print(f"Lane: {lane_name}")
    print("Decision: REJECT")
    print("Reason: Failed legality/consent gate.")
    sys.exit(0)

complexity_bonus = 11 - complexity
weighted_score = (
    legality * 0.30
    + consent * 0.25
    + time_to_cash * 0.15
    + automation_fit * 0.15
    + complexity_bonus * 0.05
    + defensibility * 0.10
)

decision = "ADVANCE" if weighted_score >= 7.5 else "HOLD"

print(f"Lane: {lane_name}")
print(f"Decision: {decision}")
print(f"Weighted score: {weighted_score:.2f}/10")
print("Breakdown:")
print(f"  legality: {legality}")
print(f"  consent: {consent}")
print(f"  time_to_cash: {time_to_cash}")
print(f"  automation_fit: {automation_fit}")
print(f"  complexity_bonus: {complexity_bonus}")
print(f"  defensibility: {defensibility}")
PY
