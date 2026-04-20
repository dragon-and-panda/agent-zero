#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality=high consent=high provenance=high platform_risk=low            time=medium margin=high repeatability=high automation=high defensibility=medium
EOF
}

declare -A values
required=(
  legality
  consent
  provenance
  platform_risk
  time
  margin
  repeatability
  automation
  defensibility
)

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    usage >&2
    exit 2
  fi
  key=${arg%%=*}
  value=${arg#*=}
  values["$key"]="$value"
done

validate_level() {
  local value=$1
  case "$value" in
    low|medium|high) ;;
    *)
      echo "Invalid value: $value (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

for key in "${required[@]}"; do
  if [[ -z "${values[$key]:-}" ]]; then
    echo "Missing required input: $key" >&2
    usage >&2
    exit 2
  fi
  validate_level "${values[$key]}"
done

hard_fail=0
if [[ "${values[legality]}" != "high" ]]; then
  hard_fail=1
fi
if [[ "${values[consent]}" != "high" ]]; then
  hard_fail=1
fi
if [[ "${values[provenance]}" != "high" ]]; then
  hard_fail=1
fi
if [[ "${values[platform_risk]}" != "low" ]]; then
  hard_fail=1
fi

if [[ "$hard_fail" -eq 1 ]]; then
  result=REJECT
else
  soft_keys=(time margin repeatability automation defensibility)
  high_count=0
  low_count=0

  for key in "${soft_keys[@]}"; do
    case "${values[$key]}" in
      high)
        high_count=$((high_count + 1))
        ;;
      low)
        low_count=$((low_count + 1))
        ;;
    esac
  done

  if [[ "$low_count" -gt 0 ]]; then
    result=HOLD
  elif [[ "$high_count" -ge 3 ]]; then
    result=PASS
  else
    result=HOLD
  fi
fi

printf 'RESULT=%s\n' "$result"
printf 'hard_gates=legality:%s consent:%s provenance:%s platform_risk:%s\n' \
  "${values[legality]}" "${values[consent]}" "${values[provenance]}" "${values[platform_risk]}"
printf 'soft_factors=time:%s margin:%s repeatability:%s automation:%s defensibility:%s\n' \
  "${values[time]}" "${values[margin]}" "${values[repeatability]}" "${values[automation]}" "${values[defensibility]}"
