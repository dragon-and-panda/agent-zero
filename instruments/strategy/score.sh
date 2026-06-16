#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 legality consent provenance platform time_to_cash margin repeatability automation defensibility"
  echo "Each value must be one of: low medium high"
}

if [[ $# -ne 9 ]]; then
  usage
  exit 1
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high) printf '%s' "$value" ;;
    *)
      echo "Invalid level: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform="$(normalize "$4")"
time_to_cash="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

hard_names=("legality" "consent" "provenance" "platform")
hard_values=("$legality" "$consent" "$provenance" "$platform")
soft_names=("time_to_cash" "margin" "repeatability" "automation" "defensibility")
soft_values=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility")

verdict="HOLD"
reason="Compliant lane needs stronger evidence or economics."

for i in "${!hard_values[@]}"; do
  if [[ "${hard_values[$i]}" == "low" ]]; then
    verdict="REJECT"
    reason="Hard gate '${hard_names[$i]}' failed."
    break
  fi
done

if [[ "$verdict" != "REJECT" ]]; then
  for i in "${!hard_values[@]}"; do
    if [[ "${hard_values[$i]}" == "medium" ]]; then
      verdict="HOLD"
      reason="Hard gate '${hard_names[$i]}' is not fully cleared."
      break
    fi
  done
fi

high_soft_count=0
low_soft_name=""
for i in "${!soft_values[@]}"; do
  if [[ "${soft_values[$i]}" == "high" ]]; then
    high_soft_count=$((high_soft_count + 1))
  elif [[ "${soft_values[$i]}" == "low" && -z "$low_soft_name" ]]; then
    low_soft_name="${soft_names[$i]}"
  fi
done

all_hard_high="true"
for value in "${hard_values[@]}"; do
  if [[ "$value" != "high" ]]; then
    all_hard_high="false"
    break
  fi
done

if [[ "$verdict" != "REJECT" && "$all_hard_high" == "true" ]]; then
  if [[ -n "$low_soft_name" ]]; then
    verdict="HOLD"
    reason="Soft factor '${low_soft_name}' is too weak."
  elif [[ "$high_soft_count" -ge 3 ]]; then
    verdict="PASS"
    reason="All hard gates clear and commercial quality is strong enough to activate."
  fi
fi

printf 'VERDICT=%s\n' "$verdict"
printf 'REASON=%s\n' "$reason"
printf 'HARD_GATES=legality:%s consent:%s provenance:%s platform:%s\n' "$legality" "$consent" "$provenance" "$platform"
printf 'SOFT_FACTORS=time_to_cash:%s margin:%s repeatability:%s automation:%s defensibility:%s\n' "$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility"
