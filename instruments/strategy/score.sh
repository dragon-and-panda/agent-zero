#!/usr/bin/env bash
set -euo pipefail

lane="unnamed-lane"
legal=""
consent=""
provenance=""
tos=""
privacy_safe=""
resale_personal_data="no"
time_score="medium"
margin="medium"
repeatability="medium"
automation="medium"
defensibility="medium"

usage() {
  echo "Usage: $0 --lane NAME --legal yes|no --consent yes|no --provenance yes|no --tos yes|no --privacy_safe yes|no --resale_personal_data yes|no --time low|medium|high --margin low|medium|high --repeatability low|medium|high --automation low|medium|high --defensibility low|medium|high" >&2
}

require_yes_no() {
  local name="$1"
  local value="$2"
  if [[ "$value" != "yes" && "$value" != "no" ]]; then
    echo "Invalid value for $name: $value" >&2
    exit 2
  fi
}

require_rating() {
  local name="$1"
  local value="$2"
  if [[ "$value" != "low" && "$value" != "medium" && "$value" != "high" ]]; then
    echo "Invalid value for $name: $value" >&2
    exit 2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lane) lane="$2"; shift 2 ;;
    --legal) legal="$2"; shift 2 ;;
    --consent) consent="$2"; shift 2 ;;
    --provenance) provenance="$2"; shift 2 ;;
    --tos) tos="$2"; shift 2 ;;
    --privacy_safe) privacy_safe="$2"; shift 2 ;;
    --resale_personal_data) resale_personal_data="$2"; shift 2 ;;
    --time) time_score="$2"; shift 2 ;;
    --margin) margin="$2"; shift 2 ;;
    --repeatability) repeatability="$2"; shift 2 ;;
    --automation) automation="$2"; shift 2 ;;
    --defensibility) defensibility="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

require_yes_no "legal" "$legal"
require_yes_no "consent" "$consent"
require_yes_no "provenance" "$provenance"
require_yes_no "tos" "$tos"
require_yes_no "privacy_safe" "$privacy_safe"
require_yes_no "resale_personal_data" "$resale_personal_data"

require_rating "time" "$time_score"
require_rating "margin" "$margin"
require_rating "repeatability" "$repeatability"
require_rating "automation" "$automation"
require_rating "defensibility" "$defensibility"

hard_failures=()
soft_values=("$time_score" "$margin" "$repeatability" "$automation" "$defensibility")
soft_names=("time" "margin" "repeatability" "automation" "defensibility")

[[ "$legal" == "yes" ]] || hard_failures+=("legal")
[[ "$consent" == "yes" ]] || hard_failures+=("consent")
[[ "$provenance" == "yes" ]] || hard_failures+=("provenance")
[[ "$tos" == "yes" ]] || hard_failures+=("tos")
[[ "$privacy_safe" == "yes" ]] || hard_failures+=("privacy_safe")
[[ "$resale_personal_data" == "no" ]] || hard_failures+=("resale_personal_data")

high_count=0
low_factors=()

for i in "${!soft_values[@]}"; do
  value="${soft_values[$i]}"
  name="${soft_names[$i]}"
  if [[ "$value" == "high" ]]; then
    high_count=$((high_count + 1))
  elif [[ "$value" == "low" ]]; then
    low_factors+=("$name")
  fi
done

decision="HOLD"
reason="Compliant but not yet strong enough for activation."

if [[ ${#hard_failures[@]} -gt 0 ]]; then
  decision="REJECT"
  reason="One or more hard gates failed."
elif [[ ${#low_factors[@]} -eq 0 && $high_count -ge 3 ]]; then
  decision="PASS"
  reason="All hard gates passed, no soft factor is low, and at least three soft factors are high."
fi

echo "LANE=$lane"
echo "DECISION=$decision"
echo "REASON=$reason"
echo "HARD_FAILURES=${hard_failures[*]:-none}"
echo "LOW_FACTORS=${low_factors[*]:-none}"
echo "HIGH_COUNT=$high_count"
echo "SOFT_FACTORS=time:$time_score margin:$margin repeatability:$repeatability automation:$automation defensibility:$defensibility"
