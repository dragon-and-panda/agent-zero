#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 legality=<low|medium|high> consent=<low|medium|high> provenance=<low|medium|high> platform_risk=<low|medium|high> time=<low|medium|high> margin=<low|medium|high> repeatability=<low|medium|high> automation=<low|medium|high> defensibility=<low|medium|high>"
}

declare -A values=(
  [legality]=""
  [consent]=""
  [provenance]=""
  [platform_risk]=""
  [time]=""
  [margin]=""
  [repeatability]=""
  [automation]=""
  [defensibility]=""
)

valid_rating() {
  case "$1" in
    low|medium|high) return 0 ;;
    *) return 1 ;;
  esac
}

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    usage
    exit 1
  fi

  key="${arg%%=*}"
  value="${arg#*=}"

  if [[ -z "${values[$key]+x}" ]]; then
    echo "Unknown factor: $key" >&2
    usage
    exit 1
  fi

  if ! valid_rating "$value"; then
    echo "Invalid rating for $key: $value" >&2
    usage
    exit 1
  fi

  values["$key"]="$value"
done

for key in "${!values[@]}"; do
  if [[ -z "${values[$key]}" ]]; then
    echo "Missing factor: $key" >&2
    usage
    exit 1
  fi
done

hard_failures=()
hold_reasons=()

if [[ "${values[legality]}" != "high" ]]; then
  hard_failures+=("legality must be high")
fi

if [[ "${values[consent]}" != "high" ]]; then
  hard_failures+=("consent must be high")
fi

if [[ "${values[provenance]}" == "low" ]]; then
  hard_failures+=("provenance cannot be low")
elif [[ "${values[provenance]}" == "medium" ]]; then
  hold_reasons+=("provenance needs stronger documentation")
fi

if [[ "${values[platform_risk]}" == "high" ]]; then
  hard_failures+=("platform risk cannot be high")
elif [[ "${values[platform_risk]}" == "medium" ]]; then
  hold_reasons+=("platform risk needs mitigation")
fi

soft_keys=(time margin repeatability automation defensibility)
soft_high_count=0
soft_low_count=0

for key in "${soft_keys[@]}"; do
  case "${values[$key]}" in
    high)
      ((soft_high_count += 1))
      ;;
    low)
      ((soft_low_count += 1))
      hold_reasons+=("$key is too weak")
      ;;
  esac
done

decision="HOLD"

if (( ${#hard_failures[@]} > 0 )); then
  decision="REJECT"
elif (( soft_low_count == 0 && soft_high_count >= 3 && ${#hold_reasons[@]} == 0 )); then
  decision="PASS"
fi

echo "decision=${decision}"
echo "hard_failures=${#hard_failures[@]}"
for reason in "${hard_failures[@]}"; do
  echo "hard_reason=${reason}"
done

echo "hold_reasons=${#hold_reasons[@]}"
for reason in "${hold_reasons[@]}"; do
  echo "hold_reason=${reason}"
done

echo "soft_high_count=${soft_high_count}"
echo "soft_low_count=${soft_low_count}"
