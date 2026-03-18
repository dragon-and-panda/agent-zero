#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  bash score.sh opportunity="Name" legality=5 consent=5 time_to_cash=4 margin=4 automation_fit=5 defensibility=3 data_sensitivity=1 delivery_risk=2 reputation_risk=1 capital_required=1

All numeric fields must be integers from 1 to 5.
EOF
}

if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

declare -A input

for arg in "$@"; do
    if [[ "$arg" != *=* ]]; then
        echo "Invalid argument: $arg" >&2
        usage
        exit 1
    fi

    key="${arg%%=*}"
    value="${arg#*=}"
    input["$key"]="$value"
done

opportunity="${input[opportunity]:-unnamed-opportunity}"
legality="${input[legality]:-5}"
consent="${input[consent]:-5}"
time_to_cash="${input[time_to_cash]:-3}"
margin="${input[margin]:-3}"
automation_fit="${input[automation_fit]:-3}"
defensibility="${input[defensibility]:-3}"
data_sensitivity="${input[data_sensitivity]:-1}"
delivery_risk="${input[delivery_risk]:-2}"
reputation_risk="${input[reputation_risk]:-2}"
capital_required="${input[capital_required]:-2}"

validate_score() {
    local label="$1"
    local value="$2"

    if [[ ! "$value" =~ ^[1-5]$ ]]; then
        echo "Invalid score for $label: $value (expected 1-5)" >&2
        exit 1
    fi
}

validate_score legality "$legality"
validate_score consent "$consent"
validate_score time_to_cash "$time_to_cash"
validate_score margin "$margin"
validate_score automation_fit "$automation_fit"
validate_score defensibility "$defensibility"
validate_score data_sensitivity "$data_sensitivity"
validate_score delivery_risk "$delivery_risk"
validate_score reputation_risk "$reputation_risk"
validate_score capital_required "$capital_required"

declare -a hard_reject_reasons=()

if (( legality < 4 )); then
    hard_reject_reasons+=("legality below minimum threshold")
fi

if (( consent < 4 )); then
    hard_reject_reasons+=("consent below minimum threshold")
fi

if (( data_sensitivity > 2 )); then
    hard_reject_reasons+=("data sensitivity too high")
fi

if (( reputation_risk > 3 )); then
    hard_reject_reasons+=("reputation risk too high")
fi

score=$(( \
    legality * 5 + \
    consent * 4 + \
    time_to_cash * 3 + \
    margin * 3 + \
    automation_fit * 4 + \
    defensibility * 2 - \
    data_sensitivity * 4 - \
    delivery_risk * 2 - \
    reputation_risk * 3 - \
    capital_required * 2 \
))

verdict="REJECT"
next_action="Do not proceed in the current form."

if (( ${#hard_reject_reasons[@]} > 0 )); then
    verdict="REJECT"
    next_action="Redesign the opportunity until it clears the hard-gate checks."
elif (( score >= 48 )); then
    verdict="GO"
    next_action="Design the offer, define a pilot, and start customer outreach."
elif (( score >= 36 )); then
    verdict="HOLD"
    next_action="Refine delivery scope, risk controls, or positioning before launch."
fi

printf 'Opportunity Scorecard\n'
printf '=====================\n'
printf 'Opportunity: %s\n' "$opportunity"
printf 'Verdict: %s\n' "$verdict"
printf 'Weighted score: %s\n' "$score"
printf '\n'
printf '%-18s %s\n' "Signal" "Score"
printf '%-18s %s\n' "------" "-----"
printf '%-18s %s\n' "legality" "$legality"
printf '%-18s %s\n' "consent" "$consent"
printf '%-18s %s\n' "time_to_cash" "$time_to_cash"
printf '%-18s %s\n' "margin" "$margin"
printf '%-18s %s\n' "automation_fit" "$automation_fit"
printf '%-18s %s\n' "defensibility" "$defensibility"
printf '%-18s %s\n' "data_sensitivity" "$data_sensitivity"
printf '%-18s %s\n' "delivery_risk" "$delivery_risk"
printf '%-18s %s\n' "reputation_risk" "$reputation_risk"
printf '%-18s %s\n' "capital_required" "$capital_required"
printf '\n'

if (( ${#hard_reject_reasons[@]} > 0 )); then
    printf 'Hard-gate failures:\n'
    for reason in "${hard_reject_reasons[@]}"; do
        printf -- '- %s\n' "$reason"
    done
    printf '\n'
fi

printf 'Next action: %s\n' "$next_action"
