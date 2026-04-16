#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 6 ]; then
  echo "Usage: $0 <legality> <consent> <time_to_cash> <automation_leverage> <margin_potential> <defensibility>"
  exit 1
fi

python3 - "$@" <<'PY2'
import sys

names = [
    "legality",
    "consent",
    "time_to_cash",
    "automation_leverage",
    "margin_potential",
    "defensibility",
]

try:
    values = [float(x) for x in sys.argv[1:]]
except ValueError:
    print("All inputs must be numbers from 0 to 10.")
    raise SystemExit(1)

if len(values) != 6:
    raise SystemExit(1)

for name, value in zip(names, values):
    if value < 0 or value > 10:
        print(f"{name} must be between 0 and 10.")
        raise SystemExit(1)

legality, consent, time_to_cash, automation_leverage, margin_potential, defensibility = values

if legality < 7 or consent < 7:
    print("Recommendation: REJECT")
    print("Reason: legality and consent are hard gates; one or both scored below 7.")
    print(f"Inputs: legality={legality:.1f}, consent={consent:.1f}")
    raise SystemExit(0)

weighted_score = (
    legality * 0.20
    + consent * 0.20
    + time_to_cash * 0.20
    + automation_leverage * 0.15
    + margin_potential * 0.15
    + defensibility * 0.10
)

if weighted_score >= 8.0:
    recommendation = "GO"
elif weighted_score >= 6.5:
    recommendation = "HOLD"
else:
    recommendation = "REJECT"

print(f"Weighted score: {weighted_score:.2f}/10")
print(f"Recommendation: {recommendation}")
print(
    "Breakdown: "
    f"legality={legality:.1f}, consent={consent:.1f}, time_to_cash={time_to_cash:.1f}, "
    f"automation_leverage={automation_leverage:.1f}, margin_potential={margin_potential:.1f}, "
    f"defensibility={defensibility:.1f}"
)
PY2
