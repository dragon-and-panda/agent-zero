#!/usr/bin/env bash
set -euo pipefail

hard_keys=(legality consent provenance tos)
soft_keys=(time margin repeatability automation defensibility)

declare -A values

for arg in "$@"; do
    key="${arg%%=*}"
    value="${arg#*=}"
    values["$key"]="$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]')"
done

normalize_hard() {
    case "$1" in
        pass|yes|true|clear|compliant|authorized|opt-in|documented)
            printf 'pass'
            ;;
        fail|no|false|unclear|unknown|scraped|unauthorized|noncompliant)
            printf 'fail'
            ;;
        *)
            printf 'fail'
            ;;
    esac
}

normalize_soft() {
    case "$1" in
        high|strong|fast|good)
            printf 'high'
            ;;
        medium|moderate|ok|okay)
            printf 'medium'
            ;;
        low|weak|slow|poor)
            printf 'low'
            ;;
        *)
            printf 'unknown'
            ;;
    esac
}

hard_failures=()
soft_lows=()
soft_unknowns=()
soft_high_count=0

for key in "${hard_keys[@]}"; do
    normalized="$(normalize_hard "${values[$key]:-}")"
    if [[ "$normalized" != "pass" ]]; then
        hard_failures+=("$key=${values[$key]:-missing}")
    fi
done

for key in "${soft_keys[@]}"; do
    normalized="$(normalize_soft "${values[$key]:-}")"
    case "$normalized" in
        high)
            ((soft_high_count+=1))
            ;;
        medium)
            ;;
        low)
            soft_lows+=("$key=${values[$key]:-missing}")
            ;;
        *)
            soft_unknowns+=("$key=${values[$key]:-missing}")
            ;;
    esac
done

decision="PASS"
reason="All hard gates are clear and the lane is attractive enough to activate."

if (( ${#hard_failures[@]} > 0 )); then
    decision="REJECT"
    reason="One or more hard gates failed or were unclear."
elif (( ${#soft_lows[@]} > 0 || ${#soft_unknowns[@]} > 0 || soft_high_count < 3 )); then
    decision="HOLD"
    reason="The lane is compliant but execution strength is not yet strong enough."
fi

printf 'decision=%s\n' "$decision"
printf 'reason=%s\n' "$reason"
printf 'hard_failures=%s\n' "${hard_failures[*]:-none}"
printf 'soft_lows=%s\n' "${soft_lows[*]:-none}"
printf 'soft_unknowns=%s\n' "${soft_unknowns[*]:-none}"
printf 'soft_high_count=%s\n' "$soft_high_count"
