#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality consent provenance tos_conflict time margin repeatability automation defensibility

Inputs:
  legality, consent, provenance, tos_conflict, time, margin, repeatability, automation, defensibility
  must each be one of: low, medium, high

Semantics:
  legality, consent, provenance: low = unacceptable, medium = partial, high = strong
  tos_conflict: low = no known conflict, medium = unclear, high = likely conflict
  time, margin, repeatability, automation, defensibility: low/medium/high desirability

Outputs:
  PASS   = compliant and execution profile is strong
  HOLD   = compliant enough to explore, but weak or uncertain execution factors remain
  REJECT = fails legal, consent, provenance, or platform-rule gates
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

declare -A SCORE=(
  [low]=1
  [medium]=2
  [high]=3
)

for value in "$@"; do
  if [[ -z "${SCORE[$value]:-}" ]]; then
    echo "Invalid value: $value" >&2
    usage >&2
    exit 1
  fi
done

legality="$1"
consent="$2"
provenance="$3"
tos_conflict="$4"
time="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" ]]; then
  echo "REJECT"
  echo "Hard gate failed: legality, consent, and provenance must all clear medium or high."
  exit 0
fi

if [[ "$tos_conflict" == "high" ]]; then
  echo "REJECT"
  echo "Hard gate failed: platform terms conflict is too high."
  exit 0
fi

if [[ "$legality" == "medium" || "$consent" == "medium" || "$provenance" == "medium" || "$tos_conflict" == "medium" ]]; then
  echo "HOLD"
  echo "Compliant directionally, but unresolved legal, consent, provenance, or platform ambiguity remains."
  exit 0
fi

soft_labels=(time margin repeatability automation defensibility)
soft_values=("$time" "$margin" "$repeatability" "$automation" "$defensibility")
soft_total=0
has_low=0

for index in "${!soft_values[@]}"; do
  value="${soft_values[$index]}"
  soft_total=$((soft_total + SCORE[$value]))
  if [[ "$value" == "low" ]]; then
    has_low=1
  fi
done

if (( has_low == 1 )); then
  echo "HOLD"
  echo "Compliant but operational profile is weak: at least one execution factor is low."
  exit 0
fi

if (( soft_total >= 13 )); then
  echo "PASS"
  echo "Compliant and operationally attractive."
else
  echo "HOLD"
  echo "Compliant, but execution profile needs improvement before activation."
fi
