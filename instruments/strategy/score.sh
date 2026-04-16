#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: $0 <legality> <consent> <provenance> <tos> <time> <margin> <repeatability> <automation> <defensibility>" >&2
  exit 2
fi

validate() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid score '$1' (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

for score in "$@"; do
  validate "$score"
done

legality="$1"
consent="$2"
provenance="$3"
tos="$4"
time="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

hard_names=(legality consent provenance tos)
hard_values=("$legality" "$consent" "$provenance" "$tos")
soft_names=(time margin repeatability automation defensibility)
soft_values=("$time" "$margin" "$repeatability" "$automation" "$defensibility")

reject_reasons=()
for i in "${!hard_values[@]}"; do
  if [ "${hard_values[$i]}" != "high" ]; then
    reject_reasons+=("${hard_names[$i]}=${hard_values[$i]}")
  fi
done

if [ "${#reject_reasons[@]}" -gt 0 ]; then
  printf 'REJECT\n'
  printf 'Hard gate failure: %s\n' "$(IFS=', '; echo "${reject_reasons[*]}")"
  exit 0
fi

hold_reasons=()
for i in "${!soft_values[@]}"; do
  if [ "${soft_values[$i]}" != "high" ]; then
    hold_reasons+=("${soft_names[$i]}=${soft_values[$i]}")
  fi
done

if [ "${#hold_reasons[@]}" -gt 0 ]; then
  printf 'HOLD\n'
  printf 'Improve before launch: %s\n' "$(IFS=', '; echo "${hold_reasons[*]}")"
  exit 0
fi

printf 'PASS\n'
printf 'All hard gates are clear and all execution factors are strong.\n'
