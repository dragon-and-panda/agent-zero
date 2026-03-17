#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 8 ]]; then
  echo "Usage: bash /workspace/instruments/strategy/score.sh \"<name>\" <legality> <consent> <automation> <margin> <speed> <dependence> <risk>"
  echo "All scores must be integers from 1 to 5."
  exit 1
fi

name="$1"
legality="$2"
consent="$3"
automation="$4"
margin="$5"
speed="$6"
dependence="$7"
risk="$8"

for value in "$legality" "$consent" "$automation" "$margin" "$speed" "$dependence" "$risk"; do
  if ! [[ "$value" =~ ^[1-5]$ ]]; then
    echo "Scores must be integers from 1 to 5."
    exit 1
  fi
done

if (( legality <= 2 || consent <= 2 )); then
  verdict="REJECT"
  reason="fails core legality or consent gate"
else
  total=$((legality + consent + automation + margin + speed))
  penalties=$(((dependence - 1) + (risk - 1)))
  score=$((total - penalties))

  if (( legality < 4 || consent < 4 )); then
    verdict="HOLD"
    reason="needs stronger compliance confidence"
  elif (( score >= 17 )); then
    verdict="GO"
    reason="high value with acceptable risk and dependency profile"
  elif (( score >= 12 )); then
    verdict="HOLD"
    reason="promising but needs derisking or tighter scoping"
  else
    verdict="REJECT"
    reason="insufficient upside relative to execution risk"
  fi
fi

cat <<EOF
Opportunity: $name
Legality: $legality/5
Consent: $consent/5
Automation fit: $automation/5
Margin potential: $margin/5
Speed to first value: $speed/5
Platform dependence: $dependence/5
Operational risk: $risk/5
Verdict: $verdict
Reason: $reason
EOF
