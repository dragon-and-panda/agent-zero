#!/bin/bash

set -euo pipefail

usage() {
    echo "Usage: $0 <legality> <consent> <data_rights> <time_to_cash> <automation_fit> <unit_economics>" >&2
}

if [ "$#" -ne 6 ]; then
    usage
    exit 2
fi

names=(legality consent data_rights time_to_cash automation_fit unit_economics)
values=("$@")

for i in "${!values[@]}"; do
    value="${values[$i]}"
    if ! [[ "$value" =~ ^([0-9]|10)$ ]]; then
        echo "Invalid ${names[$i]} score: $value (expected integer 0-10)" >&2
        exit 2
    fi
done

legality=${values[0]}
consent=${values[1]}
data_rights=${values[2]}
time_to_cash=${values[3]}
automation_fit=${values[4]}
unit_economics=${values[5]}

if [ "$legality" -lt 8 ] || [ "$consent" -lt 8 ] || [ "$data_rights" -lt 8 ]; then
    decision="REJECT"
    reason="Hard gate failed: legality, consent, and data_rights must each be at least 8."
else
    weighted_score=$(
        awk -v legality="$legality" \
            -v consent="$consent" \
            -v data_rights="$data_rights" \
            -v time_to_cash="$time_to_cash" \
            -v automation_fit="$automation_fit" \
            -v unit_economics="$unit_economics" \
            'BEGIN {
                score = (legality * 0.25) + (consent * 0.20) + (data_rights * 0.20) + (time_to_cash * 0.10) + (automation_fit * 0.15) + (unit_economics * 0.10);
                printf "%.1f", score * 10;
            }'
    )

    score_floor=${weighted_score%.*}
    if [ "$score_floor" -ge 75 ]; then
        decision="GO"
        reason="Hard gates passed and weighted score is strong."
    elif [ "$score_floor" -ge 60 ]; then
        decision="HOLD"
        reason="Hard gates passed but the lane needs better economics, speed, or automation fit."
    else
        decision="REJECT"
        reason="Hard gates passed, but the weighted score is too weak to activate."
    fi
fi

if [ -z "${weighted_score:-}" ]; then
    weighted_score="n/a"
fi

printf "legality=%s\n" "$legality"
printf "consent=%s\n" "$consent"
printf "data_rights=%s\n" "$data_rights"
printf "time_to_cash=%s\n" "$time_to_cash"
printf "automation_fit=%s\n" "$automation_fit"
printf "unit_economics=%s\n" "$unit_economics"
printf "weighted_score=%s\n" "$weighted_score"
printf "decision=%s\n" "$decision"
printf "reason=%s\n" "$reason"
