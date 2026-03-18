#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  score.sh lane="<name>" legality=<0-5> consent=<0-5> automation=<0-5> \
    time_to_cash=<0-5> redundancy=<0-5> capex=<0-5> market_access=<0-5> \
    data_risk=<0-5>

Notes:
  - Higher is better for all fields except data_risk.
  - legality and consent below 4 trigger automatic rejection.
EOF
}

lane="unnamed_lane"
legality=""
consent=""
automation=""
time_to_cash=""
redundancy=""
capex=""
market_access=""
data_risk=""

for arg in "$@"; do
    case "$arg" in
        lane=*) lane="${arg#*=}" ;;
        legality=*) legality="${arg#*=}" ;;
        consent=*) consent="${arg#*=}" ;;
        automation=*) automation="${arg#*=}" ;;
        time_to_cash=*) time_to_cash="${arg#*=}" ;;
        redundancy=*) redundancy="${arg#*=}" ;;
        capex=*) capex="${arg#*=}" ;;
        market_access=*) market_access="${arg#*=}" ;;
        data_risk=*) data_risk="${arg#*=}" ;;
        -h|--help) usage; exit 0 ;;
        *)
            echo "Unknown argument: $arg" >&2
            usage >&2
            exit 1
            ;;
    esac
done

require_value() {
    local name="$1"
    local value="$2"
    if [[ -z "$value" ]]; then
        echo "Missing required argument: $name" >&2
        usage >&2
        exit 1
    fi
    if ! [[ "$value" =~ ^[0-5]$ ]]; then
        echo "Invalid value for $name: $value (expected 0-5)" >&2
        exit 1
    fi
}

require_value "legality" "$legality"
require_value "consent" "$consent"
require_value "automation" "$automation"
require_value "time_to_cash" "$time_to_cash"
require_value "redundancy" "$redundancy"
require_value "capex" "$capex"
require_value "market_access" "$market_access"
require_value "data_risk" "$data_risk"

positive_score=$((legality + consent + automation + time_to_cash + redundancy + capex + market_access))
score=$((positive_score - data_risk))
decision="HOLD"
next_action="de-risk and tighten the lane definition"

if (( legality < 4 || consent < 4 )); then
    decision="REJECT"
    next_action="discard or reframe around first-party, consent-based operations"
elif (( data_risk >= 4 )); then
    decision="HOLD"
    next_action="reduce data exposure and add stronger controls before activation"
elif (( score >= 24 && time_to_cash >= 3 && automation >= 3 )); then
    decision="GO"
    next_action="activate the lane and prepare the smallest paid deliverable"
elif (( score < 18 || market_access <= 1 )); then
    decision="REJECT"
    next_action="replace this lane with a clearer, faster, lower-risk option"
fi

printf 'lane=%s\n' "$lane"
printf 'decision=%s\n' "$decision"
printf 'score=%s\n' "$score"
printf 'positive_score=%s\n' "$positive_score"
printf 'data_risk=%s\n' "$data_risk"
printf 'next_action=%s\n' "$next_action"
