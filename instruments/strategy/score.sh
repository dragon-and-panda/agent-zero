#!/usr/bin/env bash

set -euo pipefail

declare -A values=()
required=(
  legality consent provenance tos
  time margin repeatability automation defensibility
)

for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  values["$key"]="$value"
done

for key in "${required[@]}"; do
  if [[ -z "${values[$key]:-}" ]]; then
    echo "ERROR: missing required input '$key'" >&2
    exit 1
  fi

  case "${values[$key]}" in
    low|medium|high) ;;
    *)
      echo "ERROR: invalid value for '$key': ${values[$key]}" >&2
      exit 1
      ;;
  esac
done

hard_keys=(legality consent provenance tos)
soft_keys=(time margin repeatability automation defensibility)

hard_low=0
hard_medium=0
soft_low=0
soft_high=0

for key in "${hard_keys[@]}"; do
  case "${values[$key]}" in
    low) ((hard_low += 1)) ;;
    medium) ((hard_medium += 1)) ;;
  esac
done

for key in "${soft_keys[@]}"; do
  case "${values[$key]}" in
    low) ((soft_low += 1)) ;;
    high) ((soft_high += 1)) ;;
  esac
done

verdict="HOLD"
reason="Compliant enough to continue researching, but not ready to prioritize yet."

if (( hard_low > 0 )); then
  verdict="REJECT"
  reason="One or more hard gates failed."
elif (( hard_medium == 0 && soft_low == 0 && soft_high >= 3 )); then
  verdict="PASS"
  reason="Hard gates cleared and enough execution factors are attractive."
fi

printf 'VERDICT=%s\n' "$verdict"
printf 'REASON=%s\n' "$reason"
printf 'HARD_GATES=%s,%s,%s,%s\n' \
  "${values[legality]}" \
  "${values[consent]}" \
  "${values[provenance]}" \
  "${values[tos]}"
printf 'SOFT_FACTORS=%s,%s,%s,%s,%s\n' \
  "${values[time]}" \
  "${values[margin]}" \
  "${values[repeatability]}" \
  "${values[automation]}" \
  "${values[defensibility]}"
