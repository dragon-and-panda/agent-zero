#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 9 ]]; then
  echo "Usage: $0 legality consent provenance platform_compliance time_to_cash margin repeatability automation_leverage defensibility" >&2
  exit 64
fi

allowed_values=("low" "medium" "high")

validate_value() {
  local name="$1"
  local value="$2"
  local valid="false"
  for allowed in "${allowed_values[@]}"; do
    if [[ "$value" == "$allowed" ]]; then
      valid="true"
      break
    fi
  done
  if [[ "$valid" != "true" ]]; then
    echo "Invalid value for $name: $value" >&2
    exit 64
  fi
}

names=(
  "legality"
  "consent"
  "provenance"
  "platform_compliance"
  "time_to_cash"
  "margin"
  "repeatability"
  "automation_leverage"
  "defensibility"
)

values=("$@")

for i in "${!names[@]}"; do
  validate_value "${names[$i]}" "${values[$i]}"
done

hard_names=("${names[@]:0:4}")
hard_values=("${values[@]:0:4}")
soft_names=("${names[@]:4}")
soft_values=("${values[@]:4}")

for i in "${!hard_names[@]}"; do
  if [[ "${hard_values[$i]}" == "low" ]]; then
    printf 'VERDICT: REJECT\n'
    printf 'REASON: hard gate failed (%s=%s)\n' "${hard_names[$i]}" "${hard_values[$i]}"
    exit 0
  fi
done

for value in "${hard_values[@]}"; do
  if [[ "$value" != "high" ]]; then
    printf 'VERDICT: HOLD\n'
    printf 'REASON: hard gates are not yet fully cleared\n'
    exit 0
  fi
done

soft_high_count=0

for i in "${!soft_names[@]}"; do
  if [[ "${soft_values[$i]}" == "low" ]]; then
    printf 'VERDICT: HOLD\n'
    printf 'REASON: weak business factor (%s=%s)\n' "${soft_names[$i]}" "${soft_values[$i]}"
    exit 0
  fi
  if [[ "${soft_values[$i]}" == "high" ]]; then
    soft_high_count=$((soft_high_count + 1))
  fi
done

if (( soft_high_count >= 3 )); then
  printf 'VERDICT: PASS\n'
  printf 'REASON: compliance gates cleared and business factors are attractive\n'
else
  printf 'VERDICT: HOLD\n'
  printf 'REASON: compliant, but not yet strong enough on business attractiveness\n'
fi
