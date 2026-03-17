#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash instruments/strategy/score.sh <opportunities.tsv>" >&2
  exit 1
fi

input_file="$1"

if [[ ! -f "$input_file" ]]; then
  echo "Input file not found: $input_file" >&2
  exit 1
fi

{
  awk -F '\t' 'NR == 1 { print "weighted_score\t" $0 }' "$input_file"
  awk -F '\t' '
  BEGIN {
    OFS = "\t"
  }
  NR > 1 {
    legality = $2 + 0
    speed_to_cash = $3 + 0
    automation_fit = $4 + 0
    demand_confidence = $5 + 0
    resilience = $6 + 0
    low_capital_intensity = $7 + 0

    weighted_score = (legality * 3) + (speed_to_cash * 2) + (automation_fit * 2) + (demand_confidence * 2) + (resilience * 2) + low_capital_intensity

    print weighted_score, $0
  }
  ' "$input_file" | sort -t $'\t' -k1,1nr
}
