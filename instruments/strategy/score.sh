#!/usr/bin/env bash
set -euo pipefail

declare -A FACTORS=(
  [legality]=medium
  [consent]=medium
  [provenance]=medium
  [tos]=medium
  [time]=medium
  [margin]=medium
  [repeatability]=medium
  [automation]=medium
  [defensibility]=medium
)

normalize() {
  local value="${1,,}"
  case "$value" in
    high|medium|low) printf '%s' "$value" ;;
    *)
      printf 'invalid'
      ;;
  esac
}

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    echo "ERROR: expected key=value args, got '$arg'" >&2
    exit 2
  fi

  key="${arg%%=*}"
  value="${arg#*=}"

  if [[ -z "${FACTORS[$key]+x}" ]]; then
    echo "ERROR: unknown factor '$key'" >&2
    exit 2
  fi

  normalized="$(normalize "$value")"
  if [[ "$normalized" == "invalid" ]]; then
    echo "ERROR: invalid value '$value' for factor '$key'" >&2
    exit 2
  fi

  FACTORS[$key]="$normalized"
done

hard=(legality consent provenance tos)
soft=(time margin repeatability automation defensibility)

hard_failures=()
soft_high=0
soft_low=0
hard_medium=0

for key in "${hard[@]}"; do
  case "${FACTORS[$key]}" in
    low) hard_failures+=("$key") ;;
    medium) ((hard_medium+=1)) ;;
  esac
done

for key in "${soft[@]}"; do
  case "${FACTORS[$key]}" in
    high) ((soft_high+=1)) ;;
    low) ((soft_low+=1)) ;;
  esac
done

decision="HOLD"
reason="compliant enough to explore, but not strong enough to activate"

if (( ${#hard_failures[@]} > 0 )); then
  decision="REJECT"
  reason="hard gate failure in: ${hard_failures[*]}"
elif (( hard_medium == 0 && soft_low == 0 && soft_high >= 3 )); then
  decision="PASS"
  reason="all hard gates are high and execution profile is strong"
fi

printf 'DECISION=%s\n' "$decision"
printf 'REASON=%s\n' "$reason"
for key in legality consent provenance tos time margin repeatability automation defensibility; do
  printf '%s=%s\n' "$key" "${FACTORS[$key]}"
done
