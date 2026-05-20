#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: score.sh LEGALITY CONSENT PROVENANCE PLATFORM_RISK TIME MARGIN REPEATABILITY AUTOMATION DEFENSIBILITY" >&2
  exit 1
fi

normalize_level() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s' "$value"
      ;;
    *)
      echo "invalid level: $1" >&2
      exit 1
      ;;
  esac
}

LEGALITY="$(normalize_level "$1")"
CONSENT="$(normalize_level "$2")"
PROVENANCE="$(normalize_level "$3")"
PLATFORM_RISK="$(normalize_level "$4")"
TIME_TO_REVENUE="$(normalize_level "$5")"
MARGIN="$(normalize_level "$6")"
REPEATABILITY="$(normalize_level "$7")"
AUTOMATION="$(normalize_level "$8")"
DEFENSIBILITY="$(normalize_level "$9")"

decision="PASS"
declare -a reasons=()
soft_high_count=0

if [ "$LEGALITY" = "low" ]; then
  decision="REJECT"
  reasons+=("legality is weak")
fi

if [ "$CONSENT" = "low" ]; then
  decision="REJECT"
  reasons+=("consent is weak")
fi

if [ "$PROVENANCE" = "low" ]; then
  decision="REJECT"
  reasons+=("data provenance is weak")
fi

if [ "$PLATFORM_RISK" = "high" ]; then
  decision="REJECT"
  reasons+=("platform risk is high")
fi

if [ "$decision" != "REJECT" ]; then
  if [ "$LEGALITY" = "medium" ]; then
    decision="HOLD"
    reasons+=("legality needs stronger validation")
  fi

  if [ "$CONSENT" = "medium" ]; then
    decision="HOLD"
    reasons+=("consent needs stronger validation")
  fi

  if [ "$PROVENANCE" = "medium" ]; then
    decision="HOLD"
    reasons+=("data provenance needs stronger validation")
  fi

  if [ "$PLATFORM_RISK" = "medium" ]; then
    decision="HOLD"
    reasons+=("platform risk is not yet low")
  fi
fi

for factor_name in TIME_TO_REVENUE MARGIN REPEATABILITY AUTOMATION DEFENSIBILITY; do
  factor_value="${!factor_name}"
  if [ "$factor_value" = "low" ] && [ "$decision" != "REJECT" ]; then
    decision="HOLD"
    reasons+=("${factor_name,,} is weak")
  fi

  if [ "$factor_value" = "high" ]; then
    soft_high_count=$((soft_high_count + 1))
  fi
done

if [ "$decision" = "PASS" ] && [ "$soft_high_count" -lt 3 ]; then
  decision="HOLD"
  reasons+=("fewer than three soft factors are high")
fi

printf 'decision=%s\n' "$decision"
printf 'soft_high_count=%s\n' "$soft_high_count"

if [ "${#reasons[@]}" -eq 0 ]; then
  echo "reasons=cleared all hard gates and enough soft factors are strong"
else
  printf 'reasons=%s\n' "$(IFS='; '; echo "${reasons[*]}")"
fi
