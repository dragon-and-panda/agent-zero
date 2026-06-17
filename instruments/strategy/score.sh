#!/usr/bin/env bash

set -euo pipefail

normalize() {
  local value="${1:-}"
  value="${value,,}"
  case "$value" in
    high|h|yes|y|strong|clear)
      printf "high"
      ;;
    medium|med|m|mixed|partial)
      printf "medium"
      ;;
    low|l|no|n|weak|unclear|unknown)
      printf "low"
      ;;
    *)
      printf ""
      ;;
  esac
}

declare -A scores=(
  [legality]=""
  [consent]=""
  [provenance]=""
  [tos]=""
  [time]=""
  [margin]=""
  [repeatability]=""
  [automation]=""
  [defensibility]=""
)

for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  if [[ -n "${scores[$key]+x}" ]]; then
    scores["$key"]="$(normalize "$value")"
  fi
done

for key in "${!scores[@]}"; do
  if [[ -z "${scores[$key]}" ]]; then
    echo "Missing or invalid score for '$key'. Use high, medium, or low." >&2
    exit 1
  fi
done

hard_gates=(legality consent provenance tos)
soft_factors=(time margin repeatability automation defensibility)

hard_failures=()
high_soft_count=0
soft_low_count=0

for key in "${hard_gates[@]}"; do
  if [[ "${scores[$key]}" != "high" ]]; then
    hard_failures+=("$key=${scores[$key]}")
  fi
done

for key in "${soft_factors[@]}"; do
  if [[ "${scores[$key]}" == "high" ]]; then
    ((high_soft_count+=1))
  fi
  if [[ "${scores[$key]}" == "low" ]]; then
    ((soft_low_count+=1))
  fi
done

decision="HOLD"
reason="Compliant lane, but execution quality is not strong enough yet."

if (( ${#hard_failures[@]} > 0 )); then
  decision="REJECT"
  reason="One or more hard compliance gates failed."
elif (( soft_low_count == 0 )) && (( high_soft_count >= 3 )); then
  decision="PASS"
  reason="Hard gates cleared and execution factors are strong enough to activate."
fi

printf "decision=%s\n" "$decision"
printf "reason=%s\n" "$reason"
printf "hard_gates=legality:%s consent:%s provenance:%s tos:%s\n" \
  "${scores[legality]}" "${scores[consent]}" "${scores[provenance]}" "${scores[tos]}"
printf "soft_factors=time:%s margin:%s repeatability:%s automation:%s defensibility:%s\n" \
  "${scores[time]}" "${scores[margin]}" "${scores[repeatability]}" "${scores[automation]}" "${scores[defensibility]}"

if (( ${#hard_failures[@]} > 0 )); then
  printf "hard_failures=%s\n" "${hard_failures[*]}"
fi
