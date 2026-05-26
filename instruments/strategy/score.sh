#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 legality=<low|medium|high> consent=<low|medium|high> provenance=<low|medium|high> platform_fit=<low|medium|high> time=<low|medium|high> margin=<low|medium|high> repeatability=<low|medium|high> automation=<low|medium|high> defensibility=<low|medium|high>" >&2
}

normalize_level() {
  local value="${1:-}"
  case "${value}" in
    low|medium|high)
      printf "%s" "${value}"
      ;;
    *)
      echo "Invalid level: ${value}" >&2
      usage
      exit 1
      ;;
  esac
}

score_line() {
  local name="$1"
  local value="$2"
  printf "%-14s %s\n" "${name}:" "${value}"
}

declare -A values=(
  [legality]=""
  [consent]=""
  [provenance]=""
  [platform_fit]=""
  [time]=""
  [margin]=""
  [repeatability]=""
  [automation]=""
  [defensibility]=""
)

for pair in "$@"; do
  key="${pair%%=*}"
  value="${pair#*=}"
  if [[ -z "${values[$key]+x}" ]]; then
    echo "Unknown factor: ${key}" >&2
    usage
    exit 1
  fi
  values["$key"]="$(normalize_level "${value}")"
done

for key in "${!values[@]}"; do
  if [[ -z "${values[$key]}" ]]; then
    echo "Missing factor: ${key}" >&2
    usage
    exit 1
  fi
done

hard_factors=(legality consent provenance platform_fit)
soft_factors=(time margin repeatability automation defensibility)

decision="PASS"
reason="All hard gates are strong and the lane is attractive enough to activate."
soft_high_count=0

for factor in "${hard_factors[@]}"; do
  level="${values[$factor]}"
  if [[ "${level}" == "low" ]]; then
    decision="REJECT"
    reason="At least one hard gate failed."
    break
  fi
  if [[ "${level}" == "medium" && "${decision}" != "REJECT" ]]; then
    decision="HOLD"
    reason="At least one hard gate remains uncertain."
  fi
done

if [[ "${decision}" != "REJECT" ]]; then
  for factor in "${soft_factors[@]}"; do
    level="${values[$factor]}"
    if [[ "${level}" == "high" ]]; then
      ((soft_high_count+=1))
    fi
    if [[ "${level}" == "low" ]]; then
      decision="HOLD"
      reason="The lane is compliant but unattractive on at least one execution factor."
    fi
  done
fi

if [[ "${decision}" == "PASS" && "${soft_high_count}" -lt 3 ]]; then
  decision="HOLD"
  reason="The lane is compliant but not yet compelling enough to activate."
fi

printf "Decision: %s\n" "${decision}"
printf "Reason: %s\n" "${reason}"
printf "\nHard gates\n"
for factor in "${hard_factors[@]}"; do
  score_line "${factor}" "${values[$factor]}"
done
printf "\nSoft factors\n"
for factor in "${soft_factors[@]}"; do
  score_line "${factor}" "${values[$factor]}"
done
printf "\nSoft highs: %s\n" "${soft_high_count}"
