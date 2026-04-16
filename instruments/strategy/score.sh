#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 legality consent provenance tos time margin repeatability automation defensibility"
  echo "Each value must be one of: low, medium, high"
}

if [ "$#" -ne 9 ]; then
  usage
  exit 1
fi

normalize() {
  case "$1" in
    low|medium|high)
      printf '%s\n' "$1"
      ;;
    *)
      echo "Invalid score: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
time_score="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

reject_reasons=()
for gate in legality consent provenance tos; do
  value="${!gate}"
  if [ "$value" != "high" ]; then
    reject_reasons+=("$gate=$value")
  fi
done

if [ "${#reject_reasons[@]}" -gt 0 ]; then
  printf 'REJECT hard_gate_failed %s\n' "$(IFS=,; echo "${reject_reasons[*]}")"
  exit 0
fi

hold_reasons=()
for factor in time_score margin repeatability automation defensibility; do
  value="${!factor}"
  if [ "$value" = "low" ]; then
    hold_reasons+=("$factor=$value")
  fi
done

if [ "${#hold_reasons[@]}" -gt 0 ]; then
  printf 'HOLD soft_factor_low %s\n' "$(IFS=,; echo "${hold_reasons[*]}")"
  exit 0
fi

printf 'PASS compliant_and_executable legality=%s consent=%s provenance=%s tos=%s time=%s margin=%s repeatability=%s automation=%s defensibility=%s\n' \
  "$legality" "$consent" "$provenance" "$tos" "$time_score" "$margin" "$repeatability" "$automation" "$defensibility"
