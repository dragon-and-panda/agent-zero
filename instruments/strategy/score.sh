#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "usage: $0 <legality> <consent> <provenance> <platform_risk> <time_to_cash> <margin> <repeatability> <automation> <defensibility>" >&2
}

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid value: $1 (expected low, medium, or high)" >&2
      exit 64
      ;;
  esac
}

if [ "$#" -ne 9 ]; then
  usage
  exit 64
fi

legality="$1"
consent="$2"
provenance="$3"
platform_risk="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

for value in \
  "$legality" \
  "$consent" \
  "$provenance" \
  "$platform_risk" \
  "$time_to_cash" \
  "$margin" \
  "$repeatability" \
  "$automation" \
  "$defensibility"
do
  validate_level "$value"
done

hard_failures=()
hold_reasons=()

if [ "$legality" = "low" ]; then
  hard_failures+=("legality is low")
fi

if [ "$consent" = "low" ]; then
  hard_failures+=("consent is low")
fi

if [ "$provenance" = "low" ]; then
  hard_failures+=("provenance is low")
fi

if [ "$platform_risk" = "high" ]; then
  hard_failures+=("platform risk is high")
fi

if [ "${#hard_failures[@]}" -eq 0 ]; then
  if [ "$legality" != "high" ]; then
    hold_reasons+=("legality is not fully cleared")
  fi
  if [ "$consent" != "high" ]; then
    hold_reasons+=("consent is not fully cleared")
  fi
  if [ "$provenance" != "high" ]; then
    hold_reasons+=("provenance is not fully cleared")
  fi
  if [ "$platform_risk" != "low" ]; then
    hold_reasons+=("platform risk is not low")
  fi
fi

soft_names=(time_to_cash margin repeatability automation defensibility)
soft_values=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility")
soft_high_count=0

for i in "${!soft_names[@]}"; do
  name="${soft_names[$i]}"
  value="${soft_values[$i]}"

  if [ "$value" = "low" ]; then
    hold_reasons+=("$name is low")
  fi

  if [ "$value" = "high" ]; then
    soft_high_count=$((soft_high_count + 1))
  fi
done

if [ "${#hard_failures[@]}" -gt 0 ]; then
  verdict="REJECT"
elif [ "${#hold_reasons[@]}" -gt 0 ]; then
  verdict="HOLD"
elif [ "$soft_high_count" -lt 3 ]; then
  verdict="HOLD"
  hold_reasons+=("fewer than three soft factors are high")
else
  verdict="PASS"
fi

echo "VERDICT: $verdict"
echo "HARD_FACTORS: legality=$legality consent=$consent provenance=$provenance platform_risk=$platform_risk"
echo "SOFT_FACTORS: time_to_cash=$time_to_cash margin=$margin repeatability=$repeatability automation=$automation defensibility=$defensibility"

if [ "${#hard_failures[@]}" -gt 0 ]; then
  printf 'REASONS:\n'
  for reason in "${hard_failures[@]}"; do
    printf -- '- %s\n' "$reason"
  done
elif [ "$verdict" = "HOLD" ]; then
  printf 'REASONS:\n'
  for reason in "${hold_reasons[@]}"; do
    printf -- '- %s\n' "$reason"
  done
else
  echo "REASONS:"
  echo "- hard gates are clear"
  echo "- no soft factor is low"
  echo "- at least three soft factors are high"
fi
