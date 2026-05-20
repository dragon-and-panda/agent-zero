#!/usr/bin/env bash
set -euo pipefail

declare -A values=(
  [legality]="medium"
  [consent]="medium"
  [provenance]="medium"
  [platform_risk]="medium"
  [time]="medium"
  [margin]="medium"
  [repeatability]="medium"
  [automation]="medium"
  [defensibility]="medium"
)

valid_level() {
  case "$1" in
    low|medium|high) return 0 ;;
    *) return 1 ;;
  esac
}

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    echo "Invalid argument: $arg" >&2
    echo "Expected key=value pairs." >&2
    exit 2
  fi

  key="${arg%%=*}"
  value="${arg#*=}"

  if [[ -z "${values[$key]+x}" ]]; then
    echo "Unknown factor: $key" >&2
    exit 2
  fi

  if ! valid_level "$value"; then
    echo "Invalid level for $key: $value" >&2
    exit 2
  fi

  values["$key"]="$value"
done

reasons=()
soft_high_count=0
soft_low_count=0
hard_hold=0
verdict="HOLD"

if [[ "${values[legality]}" == "low" ]]; then
  reasons+=("low legal confidence")
fi

if [[ "${values[consent]}" == "low" ]]; then
  reasons+=("weak or missing consent")
fi

if [[ "${values[provenance]}" == "low" ]]; then
  reasons+=("unclear or unsafe data provenance")
fi

if [[ "${values[platform_risk]}" == "high" ]]; then
  reasons+=("high platform or terms-of-service risk")
fi

if (( ${#reasons[@]} > 0 )); then
  verdict="REJECT"
else
  for key in legality consent provenance; do
    if [[ "${values[$key]}" == "medium" ]]; then
      reasons+=("$key needs stronger evidence")
      hard_hold=1
    fi
  done

  if [[ "${values[platform_risk]}" == "medium" ]]; then
    reasons+=("platform risk needs mitigation")
    hard_hold=1
  fi

  for key in time margin repeatability automation defensibility; do
    case "${values[$key]}" in
      high)
        ((soft_high_count+=1))
        ;;
      low)
        ((soft_low_count+=1))
        reasons+=("$key is too weak")
        ;;
    esac
  done

  if (( hard_hold == 0 && soft_low_count == 0 && soft_high_count >= 3 )); then
    verdict="PASS"
  else
    verdict="HOLD"
  fi
fi

echo "VERDICT=$verdict"
echo "INPUTS:"
for key in legality consent provenance platform_risk time margin repeatability automation defensibility; do
  echo "  $key=${values[$key]}"
done

if (( ${#reasons[@]} > 0 )); then
  echo "REASONS:"
  for reason in "${reasons[@]}"; do
    echo "  - $reason"
  done
fi
