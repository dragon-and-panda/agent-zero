#!/bin/bash

set -euo pipefail

if [ "$#" -ne 7 ]; then
  echo "Usage: bash /workspace/instruments/strategy/score.sh \"<name>\" <legality> <privacy> <time_to_cash> <automation_fit> <demand> <durability>"
  exit 1
fi

name="$1"
legality="$2"
privacy="$3"
time_to_cash="$4"
automation_fit="$5"
demand="$6"
durability="$7"

for value in "$legality" "$privacy" "$time_to_cash" "$automation_fit" "$demand" "$durability"; do
  case "$value" in
    1|2|3|4|5) ;;
    *)
      echo "All scores must be integers from 1 to 5."
      exit 1
      ;;
  esac
done

if [ "$legality" -lt 4 ] || [ "$privacy" -lt 4 ]; then
  verdict="REJECT"
else
  weighted_total=$((legality * 30 + privacy * 25 + time_to_cash * 15 + automation_fit * 10 + demand * 10 + durability * 10))
  score_pct=$((weighted_total * 100 / 500))

  if [ "$score_pct" -ge 80 ]; then
    verdict="GO"
  elif [ "$score_pct" -ge 65 ]; then
    verdict="HOLD"
  else
    verdict="REJECT"
  fi
fi

weighted_total=${weighted_total:-0}
score_pct=${score_pct:-0}

printf 'Opportunity: %s\n' "$name"
printf 'Legality: %s/5\n' "$legality"
printf 'Privacy: %s/5\n' "$privacy"
printf 'Time to cash: %s/5\n' "$time_to_cash"
printf 'Automation fit: %s/5\n' "$automation_fit"
printf 'Demand: %s/5\n' "$demand"
printf 'Durability: %s/5\n' "$durability"
printf 'Weighted score: %s/100\n' "$score_pct"
printf 'Decision: %s\n' "$verdict"

case "$verdict" in
  GO)
    echo "Action: move to service packaging, outreach prep, and fulfillment design."
    ;;
  HOLD)
    echo "Action: identify blockers, add controls, and rescore before execution."
    ;;
  REJECT)
    echo "Action: do not execute; document why and search for adjacent compliant alternatives."
    ;;
esac
