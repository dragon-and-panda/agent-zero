#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <lane-name> key=value ..." >&2
  exit 1
fi

lane_name="$1"
shift

score_value() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
    *)
      echo "Invalid level: $1 (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

weight_for() {
  case "$1" in
    legality|consent|provenance|tos) echo 4 ;;
    automation|time_to_cash|differentiation) echo 2 ;;
    ops_burden) echo 1 ;;
    *)
      echo "Unknown field: $1" >&2
      exit 2
      ;;
  esac
}

required_fields=(
  legality
  consent
  provenance
  tos
  automation
  time_to_cash
  differentiation
  ops_burden
)

declare -A values

for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  values["$key"]="$value"
done

for field in "${required_fields[@]}"; do
  if [[ -z "${values[$field]:-}" ]]; then
    echo "Missing required field: $field" >&2
    exit 2
  fi
done

for core in legality consent provenance tos; do
  if [[ "${values[$core]}" == "low" ]]; then
    echo "Decision: REJECT"
    echo "Lane: $lane_name"
    echo "Reason: $core is low"
    exit 0
  fi
done

total=0
max_total=0

for field in "${required_fields[@]}"; do
  raw="${values[$field]}"
  numeric="$(score_value "$raw")"
  weight="$(weight_for "$field")"

  if [[ "$field" == "ops_burden" ]]; then
    # Lower operational burden is better, so invert the score.
    numeric=$((2 - numeric))
  fi

  total=$((total + numeric * weight))
  max_total=$((max_total + 2 * weight))
done

percent=$((100 * total / max_total))

decision="HOLD"
reason="Core risk factors passed, but score needs review."

if [[ "${values[legality]}" == "high" && "${values[consent]}" == "high" && \
      "${values[provenance]}" == "high" && "${values[tos]}" == "high" && \
      $percent -ge 70 ]]; then
  decision="PASS"
  reason="Strong legality, consent, provenance, and TOS posture with sufficient upside."
elif [[ $percent -lt 50 ]]; then
  decision="HOLD"
  reason="Commercial and operational profile is too weak to activate."
fi

echo "Decision: $decision"
echo "Lane: $lane_name"
echo "Score: $total/$max_total ($percent%)"
echo "Reason: $reason"
