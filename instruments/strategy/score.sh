#!/bin/bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash score.sh \
    --idea "Idea name" \
    --legality 0-5 \
    --automation 0-5 \
    --time-to-cash 0-5 \
    --repeatability 0-5 \
    --capital-efficiency 0-5 \
    --redundancy 0-5 \
    --execution-risk 0-5 \
    --consent yes|no \
    --third-party-data yes|no \
    --regulated yes|no

Rules:
  - consent=no -> REJECT
  - third-party-data=yes -> REJECT
  - legality < 4 -> REJECT
  - regulated=yes -> HOLD unless score is too low, then REJECT
EOF
}

require_value() {
  local key="$1"
  local value="${2-}"
  if [[ -z "$value" ]]; then
    echo "Missing value for $key" >&2
    usage >&2
    exit 1
  fi
}

validate_score() {
  local key="$1"
  local value="$2"
  if ! [[ "$value" =~ ^[0-5]$ ]]; then
    echo "$key must be an integer from 0 to 5" >&2
    exit 1
  fi
}

idea=""
legality=""
automation=""
time_to_cash=""
repeatability=""
capital_efficiency=""
redundancy=""
execution_risk=""
consent=""
third_party_data=""
regulated=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --idea)
      idea="${2-}"
      shift 2
      ;;
    --legality)
      legality="${2-}"
      shift 2
      ;;
    --automation)
      automation="${2-}"
      shift 2
      ;;
    --time-to-cash)
      time_to_cash="${2-}"
      shift 2
      ;;
    --repeatability)
      repeatability="${2-}"
      shift 2
      ;;
    --capital-efficiency)
      capital_efficiency="${2-}"
      shift 2
      ;;
    --redundancy)
      redundancy="${2-}"
      shift 2
      ;;
    --execution-risk)
      execution_risk="${2-}"
      shift 2
      ;;
    --consent)
      consent="${2-}"
      shift 2
      ;;
    --third-party-data)
      third_party_data="${2-}"
      shift 2
      ;;
    --regulated)
      regulated="${2-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_value "--idea" "$idea"
require_value "--legality" "$legality"
require_value "--automation" "$automation"
require_value "--time-to-cash" "$time_to_cash"
require_value "--repeatability" "$repeatability"
require_value "--capital-efficiency" "$capital_efficiency"
require_value "--redundancy" "$redundancy"
require_value "--execution-risk" "$execution_risk"
require_value "--consent" "$consent"
require_value "--third-party-data" "$third_party_data"
require_value "--regulated" "$regulated"

validate_score "--legality" "$legality"
validate_score "--automation" "$automation"
validate_score "--time-to-cash" "$time_to_cash"
validate_score "--repeatability" "$repeatability"
validate_score "--capital-efficiency" "$capital_efficiency"
validate_score "--redundancy" "$redundancy"
validate_score "--execution-risk" "$execution_risk"

consent="$(printf '%s' "$consent" | tr '[:upper:]' '[:lower:]')"
third_party_data="$(printf '%s' "$third_party_data" | tr '[:upper:]' '[:lower:]')"
regulated="$(printf '%s' "$regulated" | tr '[:upper:]' '[:lower:]')"

if [[ "$consent" != "yes" && "$consent" != "no" ]]; then
  echo "--consent must be yes or no" >&2
  exit 1
fi

if [[ "$third_party_data" != "yes" && "$third_party_data" != "no" ]]; then
  echo "--third-party-data must be yes or no" >&2
  exit 1
fi

if [[ "$regulated" != "yes" && "$regulated" != "no" ]]; then
  echo "--regulated must be yes or no" >&2
  exit 1
fi

decision="GO"
reason="High-confidence compliant opportunity."

if [[ "$consent" == "no" ]]; then
  decision="REJECT"
  reason="No consent path."
elif [[ "$third_party_data" == "yes" ]]; then
  decision="REJECT"
  reason="Depends on third-party personal data."
elif (( legality < 4 )); then
  decision="REJECT"
  reason="Legal confidence is too low."
fi

total=$(( legality * 25 \
  + automation * 15 \
  + time_to_cash * 15 \
  + repeatability * 15 \
  + capital_efficiency * 10 \
  + redundancy * 10 \
  + (5 - execution_risk) * 10 ))

percentage=$(( total / 5 ))

if [[ "$decision" == "GO" ]]; then
  if (( percentage < 55 )); then
    decision="REJECT"
    reason="Composite score is too weak."
  elif [[ "$regulated" == "yes" ]]; then
    decision="HOLD"
    reason="Requires stronger regulatory controls before launch."
  elif (( percentage < 75 )); then
    decision="HOLD"
    reason="Promising, but needs tighter positioning or process controls."
  fi
fi

cat <<EOF
Idea: $idea
Decision: $decision
Reason: $reason
Score: ${percentage}/100

Inputs:
  legality: $legality
  automation: $automation
  time_to_cash: $time_to_cash
  repeatability: $repeatability
  capital_efficiency: $capital_efficiency
  redundancy: $redundancy
  execution_risk: $execution_risk
  consent: $consent
  third_party_data: $third_party_data
  regulated: $regulated
EOF
