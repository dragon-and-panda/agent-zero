#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  score.sh <lane_name> <revenue> <speed> <defensibility> <automation_fit> <operational_ease> <legality> <consent> <provenance> <tos>

Scoring inputs:
  revenue, speed, defensibility, automation_fit, operational_ease: integers from 1 to 5

Hard gates:
  legality, consent, provenance, tos: yes|no

Output:
  PASS if all hard gates pass and weighted score >= 70
  HOLD if all hard gates pass and weighted score < 70
  REJECT if any hard gate fails

Example:
  score.sh "Inbox-to-CRM" 4 4 4 5 4 yes yes yes yes
  score.sh "Email list resale" 5 5 2 4 4 yes no no no
EOF
}

require_args() {
    if [ "$#" -ne 10 ]; then
        usage >&2
        exit 1
    fi
}

normalize_gate() {
    case "${1,,}" in
        y|yes|true|1) echo "yes" ;;
        n|no|false|0) echo "no" ;;
        *)
            echo "Invalid gate value: $1" >&2
            exit 1
            ;;
    esac
}

validate_score() {
    local name="$1"
    local value="$2"

    case "$value" in
        1|2|3|4|5) ;;
        *)
            echo "Invalid $name score: $value (expected 1-5)" >&2
            exit 1
            ;;
    esac
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    usage
    exit 0
fi

require_args "$@"

lane_name="$1"
revenue="$2"
speed="$3"
defensibility="$4"
automation_fit="$5"
operational_ease="$6"
legality="$(normalize_gate "$7")"
consent="$(normalize_gate "$8")"
provenance="$(normalize_gate "$9")"
tos="$(normalize_gate "${10}")"

validate_score "revenue" "$revenue"
validate_score "speed" "$speed"
validate_score "defensibility" "$defensibility"
validate_score "automation_fit" "$automation_fit"
validate_score "operational_ease" "$operational_ease"

weighted_total=$(( revenue * 30 + speed * 20 + defensibility * 20 + automation_fit * 20 + operational_ease * 10 ))
normalized_score=$(( weighted_total / 5 ))

decision="PASS"
exit_code=0

if [ "$legality" = "no" ] || [ "$consent" = "no" ] || [ "$provenance" = "no" ] || [ "$tos" = "no" ]; then
    decision="REJECT"
    exit_code=3
elif [ "$normalized_score" -lt 70 ]; then
    decision="HOLD"
    exit_code=2
fi

printf 'Lane: %s\n' "$lane_name"
printf 'Decision: %s\n' "$decision"
printf 'Weighted score: %s/100\n' "$normalized_score"
printf 'Inputs: revenue=%s speed=%s defensibility=%s automation_fit=%s operational_ease=%s\n' \
    "$revenue" "$speed" "$defensibility" "$automation_fit" "$operational_ease"
printf 'Hard gates: legality=%s consent=%s provenance=%s tos=%s\n' \
    "$legality" "$consent" "$provenance" "$tos"

if [ "$decision" = "REJECT" ]; then
    echo "Reason: at least one hard gate failed."
elif [ "$decision" = "HOLD" ]; then
    echo "Reason: hard gates passed but the weighted score is below the activation threshold."
else
    echo "Reason: hard gates passed and the lane cleared the activation threshold."
fi

exit "$exit_code"
