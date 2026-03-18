#!/bin/bash

set -euo pipefail

legality=""
consent=""
automation_fit=""
time_to_cash=""
recurring_revenue=""
startup_cost=""
downside_containment=""
data_risk=""
reputation_risk=""

for arg in "$@"; do
    key="${arg%%=*}"
    value="${arg#*=}"

    case "$key" in
        legality|consent|automation_fit|time_to_cash|recurring_revenue|startup_cost|downside_containment|data_risk|reputation_risk)
            printf -v "$key" '%s' "$value"
            ;;
        *)
            echo "Unknown argument: $key" >&2
            exit 1
            ;;
    esac
done

require_score() {
    local name="$1"
    local value="$2"

    if [[ -z "$value" ]]; then
        echo "Missing required score: $name" >&2
        exit 1
    fi

    if [[ ! "$value" =~ ^[1-5]$ ]]; then
        echo "Invalid score for $name: $value (expected 1-5)" >&2
        exit 1
    fi
}

require_score "legality" "$legality"
require_score "consent" "$consent"
require_score "automation_fit" "$automation_fit"
require_score "time_to_cash" "$time_to_cash"
require_score "recurring_revenue" "$recurring_revenue"
require_score "startup_cost" "$startup_cost"
require_score "downside_containment" "$downside_containment"
require_score "data_risk" "$data_risk"
require_score "reputation_risk" "$reputation_risk"

if (( legality < 4 )); then
    echo "REJECT"
    echo "Reason: legality score below minimum threshold."
    exit 0
fi

if (( consent < 4 )); then
    echo "REJECT"
    echo "Reason: consent score below minimum threshold."
    exit 0
fi

if (( data_risk > 2 )); then
    echo "REJECT"
    echo "Reason: data risk exceeds acceptable threshold."
    exit 0
fi

if (( reputation_risk > 3 )); then
    echo "REJECT"
    echo "Reason: reputation risk exceeds acceptable threshold."
    exit 0
fi

score=$(( legality + consent + automation_fit + time_to_cash + recurring_revenue + startup_cost + downside_containment + (6 - data_risk) + (6 - reputation_risk) ))

echo "Total score: $score"

if (( score >= 36 )); then
    echo "GO"
    echo "Reason: strong compliance posture and attractive operating profile."
elif (( score >= 28 )); then
    echo "HOLD"
    echo "Reason: viable, but needs tighter packaging, proof, or controls before activation."
else
    echo "REJECT"
    echo "Reason: low strategic value relative to safer alternatives."
fi
