#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: bash instruments/strategy/score.sh legality consent provenance platform_risk time_to_cash margin repeatability automation defensibility" >&2
  echo "Each value must be one of: low, medium, high" >&2
  exit 2
}

normalize() {
  local value
  value="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s\n' "$value"
      ;;
    *)
      usage
      ;;
  esac
}

if [ "$#" -ne 9 ]; then
  usage
fi

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform_risk="$(normalize "$4")"
time_to_cash="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

reject_reasons=()
hold_reasons=()

if [ "$legality" = "low" ]; then
  reject_reasons+=("legality")
fi
if [ "$consent" = "low" ]; then
  reject_reasons+=("consent")
fi
if [ "$provenance" = "low" ]; then
  reject_reasons+=("provenance")
fi
if [ "$platform_risk" = "high" ]; then
  reject_reasons+=("platform_risk")
fi

if [ "${#reject_reasons[@]}" -gt 0 ]; then
  printf 'REJECT: failed hard gates -> %s\n' "$(IFS=', '; echo "${reject_reasons[*]}")"
  exit 0
fi

if [ "$legality" = "medium" ]; then
  hold_reasons+=("legality needs validation")
fi
if [ "$consent" = "medium" ]; then
  hold_reasons+=("consent needs validation")
fi
if [ "$provenance" = "medium" ]; then
  hold_reasons+=("provenance needs validation")
fi
if [ "$platform_risk" = "medium" ]; then
  hold_reasons+=("platform risk needs mitigation")
fi

soft_high=0
soft_low=0
for factor in "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [ "$factor" = "high" ]; then
    soft_high=$((soft_high + 1))
  elif [ "$factor" = "low" ]; then
    soft_low=$((soft_low + 1))
  fi
done

if [ "$soft_low" -gt 0 ]; then
  hold_reasons+=("at least one execution factor is low")
fi
if [ "$soft_high" -lt 3 ]; then
  hold_reasons+=("fewer than three execution factors are high")
fi

if [ "${#hold_reasons[@]}" -gt 0 ]; then
  printf 'HOLD: %s\n' "$(IFS='; '; echo "${hold_reasons[*]}")"
  exit 0
fi

printf 'PASS: hard gates clear and execution profile is strong\n'
