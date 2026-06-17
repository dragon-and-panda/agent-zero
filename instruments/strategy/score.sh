#!/usr/bin/env bash

set -euo pipefail

lane=""
legality=""
consent=""
tos=""
evidence=""
reserve=""
risk=""
time_score=""
margin=""
repeatability=""
automation=""
defensibility=""

usage() {
    cat <<'EOF'
Usage:
  bash /workspace/instruments/strategy/score.sh \
    --lane "Inbox-to-CRM" \
    --legality 5 \
    --consent 5 \
    --tos 5 \
    --evidence 4 \
    --reserve 4 \
    --risk 4 \
    --time 3 \
    --margin 4 \
    --repeatability 4 \
    --automation 5 \
    --defensibility 3

Scores use a 0-5 scale where 5 is strongest.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --lane) lane="${2:-}"; shift 2 ;;
        --legality) legality="${2:-}"; shift 2 ;;
        --consent) consent="${2:-}"; shift 2 ;;
        --tos) tos="${2:-}"; shift 2 ;;
        --evidence) evidence="${2:-}"; shift 2 ;;
        --reserve) reserve="${2:-}"; shift 2 ;;
        --risk) risk="${2:-}"; shift 2 ;;
        --time) time_score="${2:-}"; shift 2 ;;
        --margin) margin="${2:-}"; shift 2 ;;
        --repeatability) repeatability="${2:-}"; shift 2 ;;
        --automation) automation="${2:-}"; shift 2 ;;
        --defensibility) defensibility="${2:-}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

required=(
    lane legality consent tos evidence reserve risk
    time_score margin repeatability automation defensibility
)

for field in "${required[@]}"; do
    if [[ -z "${!field}" ]]; then
        echo "Missing required field: ${field}" >&2
        usage >&2
        exit 2
    fi
done

validate_score() {
    local name="$1"
    local value="$2"
    if [[ ! "$value" =~ ^[0-5]$ ]]; then
        echo "Invalid score for ${name}: ${value}. Use an integer from 0 to 5." >&2
        exit 2
    fi
}

validate_score "legality" "$legality"
validate_score "consent" "$consent"
validate_score "tos" "$tos"
validate_score "evidence" "$evidence"
validate_score "reserve" "$reserve"
validate_score "risk" "$risk"
validate_score "time" "$time_score"
validate_score "margin" "$margin"
validate_score "repeatability" "$repeatability"
validate_score "automation" "$automation"
validate_score "defensibility" "$defensibility"

status="HOLD"
reason="Compliant lane but execution factors need more proof."

# Hard reject gates.
if (( legality < 4 )); then
    status="REJECT"
    reason="Legality is too weak."
elif (( consent < 4 )); then
    status="REJECT"
    reason="Consent or provenance is too weak."
elif (( tos < 4 )); then
    status="REJECT"
    reason="Platform/TOS compatibility is too weak."
elif (( evidence < 3 )); then
    status="REJECT"
    reason="Demand or evidence threshold not met."
elif (( reserve < 3 )); then
    status="REJECT"
    reason="Reserve threshold not met."
elif (( risk < 3 )); then
    status="REJECT"
    reason="Operational risk is too high."
else
    low_soft=0
    for value in "$time_score" "$margin" "$repeatability" "$automation" "$defensibility"; do
        if (( value < 3 )); then
            low_soft=1
            break
        fi
    done

    if (( low_soft == 0 )) && \
       (( time_score >= 4 )) && \
       (( margin >= 4 )) && \
       (( repeatability >= 4 )) && \
       (( automation >= 4 )) && \
       (( defensibility >= 3 )); then
        status="PASS"
        reason="Hard gates clear and execution factors are strong."
    else
        status="HOLD"
        reason="Hard gates clear, but execution factors are not yet strong enough for activation."
    fi
fi

total=$((legality + consent + tos + evidence + reserve + risk + time_score + margin + repeatability + automation + defensibility))
average=$(awk -v total="$total" 'BEGIN { printf "%.2f", total / 11 }')

printf 'lane=%s\n' "$lane"
printf 'status=%s\n' "$status"
printf 'reason=%s\n' "$reason"
printf 'average=%s\n' "$average"
printf 'scores=legality:%s consent:%s tos:%s evidence:%s reserve:%s risk:%s time:%s margin:%s repeatability:%s automation:%s defensibility:%s\n' \
    "$legality" "$consent" "$tos" "$evidence" "$reserve" "$risk" "$time_score" "$margin" "$repeatability" "$automation" "$defensibility"
