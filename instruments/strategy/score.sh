#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 7 ]; then
  echo "Usage: $0 \"lane_name\" legality consent time_to_cash defensibility autonomy_fit effort_efficiency" >&2
  exit 1
fi

lane_name="$1"
legality="$2"
consent="$3"
time_to_cash="$4"
defensibility="$5"
autonomy_fit="$6"
effort_efficiency="$7"

for value in "$legality" "$consent" "$time_to_cash" "$defensibility" "$autonomy_fit" "$effort_efficiency"; do
  if ! [[ "$value" =~ ^[0-9]+$ ]] || [ "$value" -lt 0 ] || [ "$value" -gt 10 ]; then
    echo "All scores must be integers between 0 and 10." >&2
    exit 1
  fi
done

if [ "$legality" -lt 7 ]; then
  decision="REJECT"
  reason="Legality gate failed"
elif [ "$consent" -lt 7 ]; then
  decision="REJECT"
  reason="Consent gate failed"
else
  weighted_score="$(awk -v l="$legality" -v c="$consent" -v t="$time_to_cash" -v d="$defensibility" -v a="$autonomy_fit" -v e="$effort_efficiency" 'BEGIN { printf "%.2f", (0.25*l) + (0.25*c) + (0.15*t) + (0.15*d) + (0.15*a) + (0.05*e) }')"

  decision="$(awk -v score="$weighted_score" 'BEGIN {
    if (score >= 7.5) print "GO";
    else if (score >= 6.0) print "HOLD";
    else print "REJECT";
  }')"

  reason="Weighted score evaluation"
fi

if [ -z "${weighted_score:-}" ]; then
  weighted_score="n/a"
fi

printf "Lane: %s\n" "$lane_name"
printf "Legality: %s\n" "$legality"
printf "Consent: %s\n" "$consent"
printf "Time to cash: %s\n" "$time_to_cash"
printf "Defensibility: %s\n" "$defensibility"
printf "Autonomy fit: %s\n" "$autonomy_fit"
printf "Effort efficiency: %s\n" "$effort_efficiency"
printf "Weighted score: %s\n" "$weighted_score"
printf "Decision: %s\n" "$decision"
printf "Reason: %s\n" "$reason"
