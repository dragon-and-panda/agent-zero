#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh --name NAME --demand N --speed N --fit N --compliance N --repeatability N --resilience N

Each score must be an integer from 0 to 10.
EOF
}

name=""
demand=""
speed=""
fit=""
compliance=""
repeatability=""
resilience=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) name="${2:-}"; shift 2 ;;
    --demand) demand="${2:-}"; shift 2 ;;
    --speed) speed="${2:-}"; shift 2 ;;
    --fit) fit="${2:-}"; shift 2 ;;
    --compliance) compliance="${2:-}"; shift 2 ;;
    --repeatability) repeatability="${2:-}"; shift 2 ;;
    --resilience) resilience="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

for field in name demand speed fit compliance repeatability resilience; do
  if [[ -z "${!field}" ]]; then
    echo "Missing required argument: $field" >&2
    usage >&2
    exit 1
  fi
done

validate_score() {
  local label="$1"
  local value="$2"

  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    echo "$label must be an integer from 0 to 10" >&2
    exit 1
  fi

  if (( value < 0 || value > 10 )); then
    echo "$label must be between 0 and 10" >&2
    exit 1
  fi
}

validate_score "demand" "$demand"
validate_score "speed" "$speed"
validate_score "fit" "$fit"
validate_score "compliance" "$compliance"
validate_score "repeatability" "$repeatability"
validate_score "resilience" "$resilience"

total=$(( demand + speed + fit + compliance + repeatability + resilience ))

decision="HOLD"
if (( compliance < 7 )); then
  decision="REJECT"
elif (( total >= 44 )); then
  decision="GO"
elif (( total < 32 )); then
  decision="REJECT"
fi

cat <<EOF
Opportunity: $name
Demand: $demand
Speed: $speed
Fit: $fit
Compliance: $compliance
Repeatability: $repeatability
Resilience: $resilience
Total: $total/60
Decision: $decision
EOF
