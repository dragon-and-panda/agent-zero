#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 10 ]; then
    echo "Usage: score.sh <legal> <consent> <provenance> <platform_terms> <delivery> <time_to_cash> <margin> <repeatability> <automation_fit> <defensibility>" >&2
    exit 64
fi

lower() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

is_clear_gate() {
    case "$1" in
        yes)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

is_clear_provenance() {
    case "$1" in
        first-party|client-owned|owner-authorized|public-business|public-nonpersonal|synthetic)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

is_high() {
    [ "$1" = "high" ]
}

is_low() {
    [ "$1" = "low" ]
}

legal=$(lower "$1")
consent=$(lower "$2")
provenance=$(lower "$3")
platform_terms=$(lower "$4")
delivery=$(lower "$5")
time_to_cash=$(lower "$6")
margin=$(lower "$7")
repeatability=$(lower "$8")
automation_fit=$(lower "$9")
defensibility=$(lower "${10}")

hard_failures=()
soft_lows=()
high_count=0

if ! is_clear_gate "$legal"; then
    hard_failures+=("legal")
fi

if ! is_clear_gate "$consent"; then
    hard_failures+=("consent")
fi

if ! is_clear_provenance "$provenance"; then
    hard_failures+=("provenance")
fi

if ! is_clear_gate "$platform_terms"; then
    hard_failures+=("platform_terms")
fi

if ! is_clear_gate "$delivery"; then
    hard_failures+=("delivery")
fi

for entry in \
    "time_to_cash:$time_to_cash" \
    "margin:$margin" \
    "repeatability:$repeatability" \
    "automation_fit:$automation_fit" \
    "defensibility:$defensibility"; do
    label=${entry%%:*}
    value=${entry#*:}

    if is_high "$value"; then
        high_count=$((high_count + 1))
    fi

    if is_low "$value"; then
        soft_lows+=("$label")
    fi
done

decision="HOLD"
reason="Hard gates cleared, but the lane still needs stronger attractiveness."

if [ "${#hard_failures[@]}" -gt 0 ]; then
    decision="REJECT"
    reason="Failed hard gates: ${hard_failures[*]}"
elif [ "${#soft_lows[@]}" -eq 0 ] && [ "$high_count" -ge 3 ]; then
    decision="PASS"
    reason="Hard gates cleared, no soft factor is low, and at least three soft factors are high."
fi

printf 'decision=%s\n' "$decision"
printf 'reason=%s\n' "$reason"
printf 'hard_gates legal=%s consent=%s provenance=%s platform_terms=%s delivery=%s\n' \
    "$legal" "$consent" "$provenance" "$platform_terms" "$delivery"
printf 'soft_factors time_to_cash=%s margin=%s repeatability=%s automation_fit=%s defensibility=%s high_count=%s\n' \
    "$time_to_cash" "$margin" "$repeatability" "$automation_fit" "$defensibility" "$high_count"
