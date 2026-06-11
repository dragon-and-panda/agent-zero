#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 6 ]; then
  echo "Usage: $0 legality consent speed_to_cash margin repeatability automation_fit" >&2
  exit 1
fi

legality="$1"
consent="$2"
speed_to_cash="$3"
margin="$4"
repeatability="$5"
automation_fit="$6"

for value in "$legality" "$consent" "$speed_to_cash" "$margin" "$repeatability" "$automation_fit"; do
  if ! [[ "$value" =~ ^([0-9]|10)(\.[0-9]+)?$ ]]; then
    echo "All inputs must be numbers from 0 to 10." >&2
    exit 1
  fi
done

if awk "BEGIN { exit !($legality < 8 || $consent < 8) }"; then
  decision="REJECT"
else
  total="$(awk "BEGIN {
    printf \"%.2f\", \
      ($legality * 0.25) + \
      ($consent * 0.25) + \
      ($speed_to_cash * 0.15) + \
      ($margin * 0.10) + \
      ($repeatability * 0.15) + \
      ($automation_fit * 0.10)
  }")"

  if awk "BEGIN { exit !($total >= 8.0) }"; then
    decision="GO"
  elif awk "BEGIN { exit !($total >= 6.5) }"; then
    decision="HOLD"
  else
    decision="REJECT"
  fi

  echo "decision=$decision"
  echo "total=$total"
  exit 0
fi

echo "decision=$decision"
echo "reason=failed_hard_gate_legality_or_consent"
