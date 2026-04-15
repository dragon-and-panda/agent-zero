#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 6 ]; then
    echo "Usage: $0 legality consent time_to_cash repeatability margin repo_fit" >&2
    exit 1
fi

labels=(
    "legality"
    "consent"
    "time_to_cash"
    "repeatability"
    "margin"
    "repo_fit"
)

scores=("$@")
sum=0

for i in "${!scores[@]}"; do
    value="${scores[$i]}"
    if ! [[ "$value" =~ ^[0-9]+$ ]]; then
        echo "Invalid ${labels[$i]} score: $value (expected integer 0-10)" >&2
        exit 1
    fi
    if [ "$value" -lt 0 ] || [ "$value" -gt 10 ]; then
        echo "Out-of-range ${labels[$i]} score: $value (expected integer 0-10)" >&2
        exit 1
    fi
    sum=$((sum + value))
done

legality="${scores[0]}"
consent="${scores[1]}"
percent=$((sum * 100 / 60))

decision="HOLD"
rationale="Needs more evidence before activation."

if [ "$legality" -lt 8 ]; then
    decision="REJECT"
    rationale="Legality gate failed."
elif [ "$consent" -lt 8 ]; then
    decision="REJECT"
    rationale="Consent gate failed."
elif [ "$sum" -ge 46 ]; then
    decision="GO"
    rationale="Compliant and strong enough to prototype now."
elif [ "$sum" -ge 36 ]; then
    decision="HOLD"
    rationale="Compliant, but economics or execution fit need work."
else
    decision="HOLD"
    rationale="Too weak on speed, repeatability, margin, or repo fit."
fi

printf 'scores: legality=%s consent=%s time_to_cash=%s repeatability=%s margin=%s repo_fit=%s\n' \
    "${scores[0]}" "${scores[1]}" "${scores[2]}" "${scores[3]}" "${scores[4]}" "${scores[5]}"
printf 'total: %s/60 (%s%%)\n' "$sum" "$percent"
printf 'decision: %s\n' "$decision"
printf 'rationale: %s\n' "$rationale"
