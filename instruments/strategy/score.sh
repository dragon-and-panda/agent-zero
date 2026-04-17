#!/bin/bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: $0 <legality> <consent> <provenance> <tos_fit> <margin> <automation> <repeatability> <defensibility> <time_to_cash>"
  exit 1
fi

normalize() {
  case "$1" in
    low|medium|high)
      printf '%s\n' "$1"
      ;;
    *)
      echo "invalid value: $1 (expected low, medium, or high)" >&2
      exit 2
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos_fit="$(normalize "$4")"
margin="$(normalize "$5")"
automation="$(normalize "$6")"
repeatability="$(normalize "$7")"
defensibility="$(normalize "$8")"
time_to_cash="$(normalize "$9")"

hard_names=("legality" "consent" "provenance" "tos_fit")
hard_values=("$legality" "$consent" "$provenance" "$tos_fit")

soft_names=("margin" "automation" "repeatability" "defensibility" "time_to_cash")
soft_values=("$margin" "$automation" "$repeatability" "$defensibility" "$time_to_cash")

for i in "${!hard_values[@]}"; do
  if [ "${hard_values[$i]}" = "low" ]; then
    echo "REJECT ${hard_names[$i]} is low"
    exit 0
  fi
done

for i in "${!soft_values[@]}"; do
  if [ "${soft_values[$i]}" = "low" ]; then
    echo "HOLD ${soft_names[$i]} is low"
    exit 0
  fi
done

for i in "${!hard_values[@]}"; do
  if [ "${hard_values[$i]}" = "medium" ]; then
    echo "HOLD ${hard_names[$i]} needs stronger evidence"
    exit 0
  fi
done

echo "PASS lane clears hard gates and soft factors"
