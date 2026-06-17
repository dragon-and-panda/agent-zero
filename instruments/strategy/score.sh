#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality consent provenance platform_risk time margin repeatability automation defensibility

Inputs:
  legality, consent, provenance, platform_risk, time, margin, repeatability, automation, defensibility

Accepted values:
  low | medium | high

Notes:
  - platform_risk is inverted from the execution factors. high risk is bad.
  - PASS requires all hard gates to clear, no soft factor at low, and at least 3 soft factors at high.
  - HOLD is for compliant-but-not-yet-attractive lanes.
  - REJECT is for illegal, non-consensual, unclear-provenance, or high-risk lanes.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -ne 9 ]]; then
  usage >&2
  exit 1
fi

normalize() {
  local raw="$1"
  case "${raw,,}" in
    low|medium|high)
      printf '%s\n' "${raw,,}"
      ;;
    *)
      printf 'Invalid score value: %s\n' "$raw" >&2
      exit 2
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform_risk="$(normalize "$4")"
time_score="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

soft_factors=("$time_score" "$margin" "$repeatability" "$automation" "$defensibility")
high_count=0
low_count=0

for factor in "${soft_factors[@]}"; do
  if [[ "$factor" == "high" ]]; then
    high_count=$((high_count + 1))
  fi
  if [[ "$factor" == "low" ]]; then
    low_count=$((low_count + 1))
  fi
done

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" || "$platform_risk" == "high" ]]; then
  printf 'REJECT\n'
  exit 0
fi

if [[ "$legality" == "medium" || "$consent" == "medium" || "$provenance" == "medium" ]]; then
  printf 'HOLD\n'
  exit 0
fi

if [[ "$platform_risk" == "medium" ]]; then
  printf 'HOLD\n'
  exit 0
fi

if (( low_count > 0 )); then
  printf 'HOLD\n'
  exit 0
fi

if (( high_count >= 3 )); then
  printf 'PASS\n'
  exit 0
fi

printf 'HOLD\n'
