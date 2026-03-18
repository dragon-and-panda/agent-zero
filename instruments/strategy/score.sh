#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh --name NAME --acquisition N --delivery N --compliance N --speed N --margin N --durability N --capital N [--notes TEXT]

All scores must be integers from 1 to 5.
EOF
}

require_value() {
  local value="$1"
  local label="$2"
  if [[ -z "$value" ]]; then
    echo "Missing required value: $label" >&2
    usage >&2
    exit 1
  fi
  if ! [[ "$value" =~ ^[1-5]$ ]]; then
    echo "Invalid score for $label: $value (expected 1-5)" >&2
    exit 1
  fi
}

name=""
notes=""
acquisition=""
delivery=""
compliance=""
speed=""
margin=""
durability=""
capital=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      name="${2:-}"
      shift 2
      ;;
    --notes)
      notes="${2:-}"
      shift 2
      ;;
    --acquisition)
      acquisition="${2:-}"
      shift 2
      ;;
    --delivery)
      delivery="${2:-}"
      shift 2
      ;;
    --compliance)
      compliance="${2:-}"
      shift 2
      ;;
    --speed)
      speed="${2:-}"
      shift 2
      ;;
    --margin)
      margin="${2:-}"
      shift 2
      ;;
    --durability)
      durability="${2:-}"
      shift 2
      ;;
    --capital)
      capital="${2:-}"
      shift 2
      ;;
    -h|--help)
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

if [[ -z "$name" ]]; then
  echo "Missing required value: --name" >&2
  usage >&2
  exit 1
fi

require_value "$acquisition" "acquisition"
require_value "$delivery" "delivery"
require_value "$compliance" "compliance"
require_value "$speed" "speed"
require_value "$margin" "margin"
require_value "$durability" "durability"
require_value "$capital" "capital"

raw_score=$((acquisition + delivery + compliance + speed + margin + durability + capital))
weighted_score=$((acquisition + delivery + (compliance * 2) + speed + margin + durability + capital))

combined_text="$(printf '%s\n%s' "$name" "$notes" | tr '[:upper:]' '[:lower:]')"
forbidden_pattern='sell(ing)?[[:space:]]+email|email[[:space:]-]?list|broker(age)?[[:space:]]+.*email|scrap(e|ing).*(inbox|gmail|mailbox)|spam|credential|captcha[[:space:]]+bypass|pump[[:space:]-]?and[[:space:]-]?dump'
forex_leverage_pattern='forex.*leverag|leverag.*forex'
safe_forex_exception='paper[[:space:]-]?trad|simulation[[:space:]]+only|no[[:space:]]+leverage'
policy_flag="clear"

if [[ "$combined_text" =~ $forbidden_pattern ]]; then
  policy_flag="forbidden_pattern"
elif [[ "$combined_text" =~ $forex_leverage_pattern ]] && ! [[ "$combined_text" =~ $safe_forex_exception ]]; then
  policy_flag="forbidden_pattern"
fi

decision="REJECT"
reason=""

if [[ "$policy_flag" != "clear" ]]; then
  decision="REJECT"
  reason="Policy flag triggered by venture description."
elif (( compliance < 3 )); then
  decision="REJECT"
  reason="Compliance score below minimum threshold."
elif (( weighted_score >= 29 && compliance >= 4 )); then
  decision="GO"
  reason="Meets launch threshold with strong compliance."
elif (( weighted_score >= 23 && compliance >= 3 )); then
  decision="HOLD"
  reason="Potentially viable, but not yet strong enough for immediate launch."
else
  decision="REJECT"
  reason="Insufficient score for launch or hold."
fi

printf 'Name: %s\n' "$name"
printf 'Raw Score: %d/35\n' "$raw_score"
printf 'Weighted Score: %d\n' "$weighted_score"
printf 'Decision: %s\n' "$decision"
printf 'Policy Flag: %s\n' "$policy_flag"
printf 'Reason: %s\n' "$reason"
