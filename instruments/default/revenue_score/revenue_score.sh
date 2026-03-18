#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 --name <offer> --impact <1-5> --time-to-cash <1-5> --automation-fit <1-5> --confidence <1-5> --redundancy <1-5> --setup-cost <1-5> --compliance-risk <1-5>"
}

require_value() {
  local key="$1"
  local value="$2"

  if [[ -z "$value" ]]; then
    echo "Missing value for $key" >&2
    usage
    exit 1
  fi
}

validate_score() {
  local key="$1"
  local value="$2"

  if ! [[ "$value" =~ ^[1-5]$ ]]; then
    echo "Invalid value for $key: $value (expected 1-5)" >&2
    exit 1
  fi
}

name=""
impact=""
time_to_cash=""
automation_fit=""
confidence=""
redundancy=""
setup_cost=""
compliance_risk=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      shift
      name="${1:-}"
      ;;
    --impact)
      shift
      impact="${1:-}"
      ;;
    --time-to-cash)
      shift
      time_to_cash="${1:-}"
      ;;
    --automation-fit)
      shift
      automation_fit="${1:-}"
      ;;
    --confidence)
      shift
      confidence="${1:-}"
      ;;
    --redundancy)
      shift
      redundancy="${1:-}"
      ;;
    --setup-cost)
      shift
      setup_cost="${1:-}"
      ;;
    --compliance-risk)
      shift
      compliance_risk="${1:-}"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

require_value "--name" "$name"
require_value "--impact" "$impact"
require_value "--time-to-cash" "$time_to_cash"
require_value "--automation-fit" "$automation_fit"
require_value "--confidence" "$confidence"
require_value "--redundancy" "$redundancy"
require_value "--setup-cost" "$setup_cost"
require_value "--compliance-risk" "$compliance_risk"

validate_score "--impact" "$impact"
validate_score "--time-to-cash" "$time_to_cash"
validate_score "--automation-fit" "$automation_fit"
validate_score "--confidence" "$confidence"
validate_score "--redundancy" "$redundancy"
validate_score "--setup-cost" "$setup_cost"
validate_score "--compliance-risk" "$compliance_risk"

score=$(
  awk \
    -v impact="$impact" \
    -v time_to_cash="$time_to_cash" \
    -v automation_fit="$automation_fit" \
    -v confidence="$confidence" \
    -v redundancy="$redundancy" \
    -v setup_cost="$setup_cost" \
    -v compliance_risk="$compliance_risk" \
    'BEGIN {
      total = 0
      total += ((impact - 1) / 4) * 25
      total += ((time_to_cash - 1) / 4) * 20
      total += ((automation_fit - 1) / 4) * 20
      total += ((confidence - 1) / 4) * 15
      total += ((redundancy - 1) / 4) * 10
      total += ((5 - setup_cost) / 4) * 5
      total += ((5 - compliance_risk) / 4) * 5
      printf "%.1f", total
    }'
)

band="hold or reject"
if awk "BEGIN { exit !($score >= 80) }"; then
  band="launch now"
elif awk "BEGIN { exit !($score >= 60) }"; then
  band="incubate with constraints"
fi

cat <<EOF
Opportunity: $name
Weighted score: $score / 100
Decision band: $band

Breakdown
- impact: $impact
- time-to-cash: $time_to_cash
- automation-fit: $automation_fit
- confidence: $confidence
- redundancy: $redundancy
- setup-cost: $setup_cost
- compliance-risk: $compliance_risk
EOF
