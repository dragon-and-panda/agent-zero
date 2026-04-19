#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 10 ]]; then
  echo "usage: $0 lane legality consent provenance tos time margin repeatability automation defensibility"
  echo "values: low|medium|high"
  exit 1
fi

normalize() {
  local value="${1,,}"
  case "$value" in
    low|medium|high)
      printf '%s' "$value"
      ;;
    *)
      echo "invalid value: $1" >&2
      exit 1
      ;;
  esac
}

lane="$1"
legality="$(normalize "$2")"
consent="$(normalize "$3")"
provenance="$(normalize "$4")"
tos="$(normalize "$5")"
time="$(normalize "$6")"
margin="$(normalize "$7")"
repeatability="$(normalize "$8")"
automation="$(normalize "$9")"
defensibility="$(normalize "${10}")"

reject_reasons=()
hold_reasons=()

if [[ "$legality" == "low" ]]; then
  reject_reasons+=("legality")
fi
if [[ "$consent" == "low" ]]; then
  reject_reasons+=("consent")
fi
if [[ "$provenance" == "low" ]]; then
  reject_reasons+=("provenance")
fi
if [[ "$tos" == "low" ]]; then
  reject_reasons+=("platform_tos")
fi

if [[ ${#reject_reasons[@]} -gt 0 ]]; then
  printf 'REJECT [%s]: failed hard gates -> %s\n' "$lane" "$(IFS=, ; echo "${reject_reasons[*]}")"
  exit 0
fi

for factor_name in legality consent provenance tos; do
  factor_value="${!factor_name}"
  if [[ "$factor_value" == "medium" ]]; then
    hold_reasons+=("${factor_name}")
  fi
done

soft_low_reasons=()
for factor_name in time margin repeatability automation defensibility; do
  factor_value="${!factor_name}"
  if [[ "$factor_value" == "low" ]]; then
    soft_low_reasons+=("${factor_name}")
  fi
done

if [[ ${#soft_low_reasons[@]} -gt 0 ]]; then
  hold_reasons+=("${soft_low_reasons[@]}")
fi

if [[ ${#hold_reasons[@]} -gt 0 ]]; then
  printf 'HOLD [%s]: improve or validate -> %s\n' "$lane" "$(IFS=, ; echo "${hold_reasons[*]}")"
  exit 0
fi

printf 'PASS [%s]: compliant and commercially attractive\n' "$lane"
