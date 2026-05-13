#!/usr/bin/env bash

set -euo pipefail

readonly VALID_LOW="low"
readonly VALID_MEDIUM="medium"
readonly VALID_HIGH="high"

usage() {
  echo "Usage: $0 legality=<low|medium|high> consent=<low|medium|high> provenance=<low|medium|high> platform_fit=<low|medium|high> time=<low|medium|high> margin=<low|medium|high> repeatability=<low|medium|high> automation=<low|medium|high> defensibility=<low|medium|high>" >&2
}

normalize_rating() {
  local value="${1,,}"
  case "$value" in
    "$VALID_LOW"|"$VALID_MEDIUM"|"$VALID_HIGH")
      printf "%s" "$value"
      ;;
    *)
      return 1
      ;;
  esac
}

declare -A ratings=(
  [legality]=""
  [consent]=""
  [provenance]=""
  [platform_fit]=""
  [time]=""
  [margin]=""
  [repeatability]=""
  [automation]=""
  [defensibility]=""
)

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    usage
    exit 1
  fi

  key="${arg%%=*}"
  value="${arg#*=}"

  if [[ -z "${ratings[$key]+x}" ]]; then
    echo "Unknown factor: $key" >&2
    usage
    exit 1
  fi

  if ! normalized="$(normalize_rating "$value")"; then
    echo "Invalid rating for $key: $value" >&2
    usage
    exit 1
  fi

  ratings["$key"]="$normalized"
done

for key in "${!ratings[@]}"; do
  if [[ -z "${ratings[$key]}" ]]; then
    echo "Missing factor: $key" >&2
    usage
    exit 1
  fi
done

hard_failures=()
hard_cautions=()

for key in legality consent provenance platform_fit; do
  case "${ratings[$key]}" in
    "$VALID_LOW")
      hard_failures+=("$key")
      ;;
    "$VALID_MEDIUM")
      hard_cautions+=("$key")
      ;;
  esac
done

soft_lows=()
soft_high_count=0

for key in time margin repeatability automation defensibility; do
  case "${ratings[$key]}" in
    "$VALID_LOW")
      soft_lows+=("$key")
      ;;
    "$VALID_HIGH")
      ((soft_high_count+=1))
      ;;
  esac
done

status="HOLD"
reason="Compliant enough to consider, but not strong enough to activate yet."

if ((${#hard_failures[@]} > 0)); then
  status="REJECT"
  reason="One or more hard gates failed."
elif ((${#hard_cautions[@]} > 0)); then
  status="HOLD"
  reason="At least one hard gate is still only medium."
elif ((${#soft_lows[@]} > 0)); then
  status="HOLD"
  reason="The lane is compliant but too weak on one or more execution factors."
elif ((soft_high_count >= 3)); then
  status="PASS"
  reason="All hard gates cleared and enough soft factors are strong."
else
  status="HOLD"
  reason="The lane is compliant, but not yet compelling."
fi

echo "STATUS: $status"
echo "REASON: $reason"
echo "HARD_GATES: legality=${ratings[legality]} consent=${ratings[consent]} provenance=${ratings[provenance]} platform_fit=${ratings[platform_fit]}"
echo "SOFT_FACTORS: time=${ratings[time]} margin=${ratings[margin]} repeatability=${ratings[repeatability]} automation=${ratings[automation]} defensibility=${ratings[defensibility]}"

if ((${#hard_failures[@]} > 0)); then
  printf "HARD_FAILURES: %s\n" "${hard_failures[*]}"
fi

if ((${#hard_cautions[@]} > 0)); then
  printf "HARD_CAUTIONS: %s\n" "${hard_cautions[*]}"
fi

if ((${#soft_lows[@]} > 0)); then
  printf "SOFT_LIMITERS: %s\n" "${soft_lows[*]}"
fi
