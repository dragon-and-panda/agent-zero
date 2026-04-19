#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: $0 legality consent provenance tos margin repeatability automation defensibility time_to_cash" >&2
  echo "values: low|medium|high" >&2
  exit 2
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s\n' "$value"
      ;;
    *)
      echo "invalid value: $1" >&2
      exit 2
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
margin="$(normalize "$5")"
repeatability="$(normalize "$6")"
automation="$(normalize "$7")"
defensibility="$(normalize "$8")"
time_to_cash="$(normalize "$9")"

hard_fail_reason=""

if [ "$legality" = "low" ]; then
  hard_fail_reason="legality"
elif [ "$consent" = "low" ]; then
  hard_fail_reason="consent"
elif [ "$provenance" = "low" ]; then
  hard_fail_reason="provenance"
elif [ "$tos" = "low" ]; then
  hard_fail_reason="tos"
fi

if [ -n "$hard_fail_reason" ]; then
  printf 'REJECT hard_gate=%s\n' "$hard_fail_reason"
  exit 0
fi

soft_factors=("$margin" "$repeatability" "$automation" "$defensibility" "$time_to_cash")
soft_names=("margin" "repeatability" "automation" "defensibility" "time_to_cash")

low_names=()
medium_count=0

for i in "${!soft_factors[@]}"; do
  if [ "${soft_factors[$i]}" = "low" ]; then
    low_names+=("${soft_names[$i]}")
  elif [ "${soft_factors[$i]}" = "medium" ]; then
    medium_count=$((medium_count + 1))
  fi
done

if [ "${#low_names[@]}" -gt 0 ]; then
  printf 'HOLD reason=soft_low factors=%s\n' "$(IFS=,; echo "${low_names[*]}")"
  exit 0
fi

if [ "$medium_count" -gt 2 ]; then
  printf 'HOLD reason=too_many_medium medium_count=%s\n' "$medium_count"
  exit 0
fi

echo "PASS"
