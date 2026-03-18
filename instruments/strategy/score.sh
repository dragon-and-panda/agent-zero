#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <legality> <consent> <unit_economics> <repeatability> <time_to_cash> <operator_fit> <capital_intensity> <downside_risk>"
  echo "All values must be integers from 0 to 5."
}

if [ "$#" -ne 8 ]; then
  usage
  exit 1
fi

names=(
  "legality"
  "consent"
  "unit_economics"
  "repeatability"
  "time_to_cash"
  "operator_fit"
  "capital_intensity"
  "downside_risk"
)

values=("$@")

for i in "${!values[@]}"; do
  value="${values[$i]}"
  if ! [[ "$value" =~ ^[0-5]$ ]]; then
    echo "Invalid ${names[$i]} value: $value"
    usage
    exit 1
  fi
done

legality="${values[0]}"
consent="${values[1]}"
unit_economics="${values[2]}"
repeatability="${values[3]}"
time_to_cash="${values[4]}"
operator_fit="${values[5]}"
capital_intensity="${values[6]}"
downside_risk="${values[7]}"

if [ "$legality" -lt 4 ] || [ "$consent" -lt 4 ]; then
  echo "decision=REJECT"
  echo "reason=legality_or_consent_below_threshold"
  exit 0
fi

positive_score=$((legality + consent + unit_economics + repeatability + time_to_cash + operator_fit))
negative_score=$((capital_intensity + downside_risk))
net_score=$((positive_score - negative_score))

decision="REJECT"
reason="score_below_threshold"

if [ "$net_score" -ge 22 ] && [ "$capital_intensity" -le 3 ] && [ "$downside_risk" -le 3 ]; then
  decision="GO"
  reason="strong_compliant_lane"
elif [ "$net_score" -ge 16 ]; then
  decision="HOLD"
  reason="needs_more_validation_or_risk_reduction"
fi

echo "decision=$decision"
echo "reason=$reason"
echo "positive_score=$positive_score"
echo "negative_score=$negative_score"
echo "net_score=$net_score"
