#!/bin/bash

set -euo pipefail

usage() {
  echo "usage: $0 <legality> <consent> <provenance> <tos> <margin> <repeatability> <automation> <defensibility> <time_to_cash> <setup_complexity>"
  echo "all arguments must be one of: low medium high"
}

if [ "$#" -ne 10 ]; then
  usage
  exit 1
fi

to_score() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
    *)
      echo "invalid level: $1" >&2
      exit 2
      ;;
  esac
}

legality="$1"
consent="$2"
provenance="$3"
tos="$4"
margin="$5"
repeatability="$6"
automation="$7"
defensibility="$8"
time_to_cash="$9"
setup_complexity="${10}"

hard_names=("legality" "consent" "provenance" "tos")
hard_values=("$legality" "$consent" "$provenance" "$tos")

for i in "${!hard_names[@]}"; do
  name="${hard_names[$i]}"
  value="${hard_values[$i]}"
  if [ "$value" = "low" ]; then
    echo "VERDICT: REJECT"
    echo "REASON: hard gate '$name' is low"
    exit 0
  fi
done

hold_reasons=()

for i in "${!hard_names[@]}"; do
  name="${hard_names[$i]}"
  value="${hard_values[$i]}"
  if [ "$value" = "medium" ]; then
    hold_reasons+=("hard gate '$name' needs stronger evidence")
  fi
done

soft_names=("margin" "repeatability" "automation" "defensibility" "time_to_cash")
soft_values=("$margin" "$repeatability" "$automation" "$defensibility" "$time_to_cash")

soft_total=0
soft_high=0

for i in "${!soft_names[@]}"; do
  name="${soft_names[$i]}"
  value="${soft_values[$i]}"
  score="$(to_score "$value")"
  soft_total=$((soft_total + score))
  if [ "$value" = "high" ]; then
    soft_high=$((soft_high + 1))
  fi
  if [ "$value" = "low" ]; then
    hold_reasons+=("soft factor '$name' is low")
  fi
done

case "$setup_complexity" in
  low)
    execution_score=3
    ;;
  medium)
    execution_score=2
    hold_reasons+=("setup complexity is medium")
    ;;
  high)
    execution_score=1
    hold_reasons+=("setup complexity is high")
    ;;
  *)
    echo "invalid level: $setup_complexity" >&2
    exit 2
    ;;
esac

soft_total=$((soft_total + execution_score))

if [ "${#hold_reasons[@]}" -eq 0 ] && [ "$soft_high" -ge 4 ] && [ "$soft_total" -ge 15 ]; then
  echo "VERDICT: PASS"
  echo "REASON: hard gates are clear and execution factors are strong"
  exit 0
fi

echo "VERDICT: HOLD"
if [ "${#hold_reasons[@]}" -gt 0 ]; then
  printf 'REASON: %s\n' "${hold_reasons[0]}"
  for reason in "${hold_reasons[@]:1}"; do
    printf 'DETAIL: %s\n' "$reason"
  done
else
  echo "REASON: economics are not strong enough to prioritize yet"
fi
