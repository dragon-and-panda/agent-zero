#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  score.sh <customer_value> <execution_feasibility> <repeatability> <legal_risk> <consent_risk> <data_provenance_risk> <platform_risk>

Each input must be one of:
  low | medium | high

Outputs:
  STATUS: PASS | HOLD | REJECT
  UPSIDE_SCORE
  RISK_SCORE
  SUMMARY
EOF
}

normalize() {
    local value
    value="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')"
    case "$value" in
        low|medium|high) printf '%s\n' "$value" ;;
        *) return 1 ;;
    esac
}

value_score() {
    case "$1" in
        low) printf '1\n' ;;
        medium) printf '2\n' ;;
        high) printf '3\n' ;;
    esac
}

if [ "$#" -ne 7 ]; then
    usage
    exit 1
fi

customer_value="$(normalize "$1")" || { usage; exit 1; }
execution_feasibility="$(normalize "$2")" || { usage; exit 1; }
repeatability="$(normalize "$3")" || { usage; exit 1; }
legal_risk="$(normalize "$4")" || { usage; exit 1; }
consent_risk="$(normalize "$5")" || { usage; exit 1; }
data_provenance_risk="$(normalize "$6")" || { usage; exit 1; }
platform_risk="$(normalize "$7")" || { usage; exit 1; }

upside_score=$(( \
    $(value_score "$customer_value") + \
    $(value_score "$execution_feasibility") + \
    $(value_score "$repeatability") \
))

risk_score=$(( \
    $(value_score "$legal_risk") + \
    $(value_score "$consent_risk") + \
    $(value_score "$data_provenance_risk") + \
    $(value_score "$platform_risk") \
))

if [ "$legal_risk" = "high" ]; then
    printf 'STATUS: REJECT\n'
    printf 'UPSIDE_SCORE: %s\n' "$upside_score"
    printf 'RISK_SCORE: %s\n' "$risk_score"
    printf 'SUMMARY: legal risk is too high for autonomous execution.\n'
    exit 0
fi

if [ "$consent_risk" = "high" ]; then
    printf 'STATUS: REJECT\n'
    printf 'UPSIDE_SCORE: %s\n' "$upside_score"
    printf 'RISK_SCORE: %s\n' "$risk_score"
    printf 'SUMMARY: consent risk is too high; use opt-in or owner-authorized data only.\n'
    exit 0
fi

if [ "$data_provenance_risk" = "high" ]; then
    printf 'STATUS: REJECT\n'
    printf 'UPSIDE_SCORE: %s\n' "$upside_score"
    printf 'RISK_SCORE: %s\n' "$risk_score"
    printf 'SUMMARY: data provenance is too weak; prefer first-party, public, or licensed data.\n'
    exit 0
fi

if [ "$platform_risk" = "high" ]; then
    printf 'STATUS: HOLD\n'
    printf 'UPSIDE_SCORE: %s\n' "$upside_score"
    printf 'RISK_SCORE: %s\n' "$risk_score"
    printf 'SUMMARY: platform dependence is too risky; require a more durable acquisition path.\n'
    exit 0
fi

if [ "$upside_score" -ge 8 ] && [ "$risk_score" -le 7 ]; then
    printf 'STATUS: PASS\n'
    printf 'UPSIDE_SCORE: %s\n' "$upside_score"
    printf 'RISK_SCORE: %s\n' "$risk_score"
    printf 'SUMMARY: strong candidate with acceptable compliance and platform risk.\n'
    exit 0
fi

printf 'STATUS: HOLD\n'
printf 'UPSIDE_SCORE: %s\n' "$upside_score"
printf 'RISK_SCORE: %s\n' "$risk_score"
printf 'SUMMARY: promising but needs tighter positioning, data controls, or execution proof.\n'
