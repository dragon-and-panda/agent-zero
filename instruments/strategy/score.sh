#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 10 ]; then
  echo "usage: $0 legality consent provenance platform_risk time_to_cash margin repeatability automation_fit defensibility notes" >&2
  echo "values: low|medium|high for the first 9 args; notes can be any string" >&2
  exit 2
fi

legality="$1"
consent="$2"
provenance="$3"
platform_risk="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation_fit="$8"
defensibility="$9"
notes="${10}"

normalize() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

for value in \
  "$legality" "$consent" "$provenance" "$platform_risk" \
  "$time_to_cash" "$margin" "$repeatability" "$automation_fit" "$defensibility"
do
  case "$(normalize "$value")" in
    low|medium|high) ;;
    *)
      echo "invalid value: $value (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
done

legality="$(normalize "$legality")"
consent="$(normalize "$consent")"
provenance="$(normalize "$provenance")"
platform_risk="$(normalize "$platform_risk")"
time_to_cash="$(normalize "$time_to_cash")"
margin="$(normalize "$margin")"
repeatability="$(normalize "$repeatability")"
automation_fit="$(normalize "$automation_fit")"
defensibility="$(normalize "$defensibility")"

hard_fail_reasons=()
hold_reasons=()

if [ "$legality" != "high" ]; then
  hard_fail_reasons+=("legality")
fi

if [ "$consent" != "high" ]; then
  hard_fail_reasons+=("consent")
fi

if [ "$provenance" != "high" ]; then
  hard_fail_reasons+=("provenance")
fi

if [ "$platform_risk" = "low" ]; then
  hard_fail_reasons+=("platform_risk")
elif [ "$platform_risk" = "medium" ]; then
  hold_reasons+=("platform_risk")
fi

soft_lows=0
soft_highs=0

for value_name in time_to_cash margin repeatability automation_fit defensibility; do
  value="${!value_name}"
  if [ "$value" = "low" ]; then
    soft_lows=$((soft_lows + 1))
    hold_reasons+=("$value_name")
  elif [ "$value" = "high" ]; then
    soft_highs=$((soft_highs + 1))
  fi
done

if [ "${#hard_fail_reasons[@]}" -gt 0 ]; then
  printf 'REJECT | hard_gates_failed=%s | notes=%s\n' "$(IFS=,; echo "${hard_fail_reasons[*]}")" "$notes"
  exit 0
fi

if [ "$soft_lows" -gt 0 ] || [ "$soft_highs" -lt 3 ]; then
  if [ "$soft_highs" -lt 3 ]; then
    hold_reasons+=("insufficient_high_conviction")
  fi
  printf 'HOLD | issues=%s | notes=%s\n' "$(IFS=,; echo "${hold_reasons[*]}")" "$notes"
  exit 0
fi

printf 'PASS | issues=none | notes=%s\n' "$notes"
