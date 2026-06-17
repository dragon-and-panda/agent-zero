#!/usr/bin/env bash
set -euo pipefail

normalize_level() {
    case "${1:-medium}" in
        high|medium|low)
            printf '%s\n' "$1"
            ;;
        *)
            printf 'medium\n'
            ;;
    esac
}

declare -A ratings=(
    [legality]=medium
    [consent]=medium
    [provenance]=medium
    [platform_risk]=medium
    [time]=medium
    [margin]=medium
    [repeatability]=medium
    [automation]=medium
    [defensibility]=medium
)

for arg in "$@"; do
    key="${arg%%=*}"
    value="${arg#*=}"
    if [[ -n "${ratings[$key]+x}" ]]; then
        ratings["$key"]="$(normalize_level "$value")"
    fi
done

hard_factors=(legality consent provenance platform_risk)
soft_factors=(time margin repeatability automation defensibility)

hard_failures=()
hard_holds=()
soft_lows=()
soft_high_count=0

for factor in "${hard_factors[@]}"; do
    value="${ratings[$factor]}"
    if [[ "$value" == "low" ]]; then
        hard_failures+=("$factor")
    elif [[ "$value" != "high" ]]; then
        hard_holds+=("$factor")
    fi
done

for factor in "${soft_factors[@]}"; do
    value="${ratings[$factor]}"
    if [[ "$value" == "low" ]]; then
        soft_lows+=("$factor")
    fi
    if [[ "$value" == "high" ]]; then
        soft_high_count=$((soft_high_count + 1))
    fi
done

decision="HOLD"
summary="Hard gates need more evidence or execution quality is not strong enough yet."

if (( ${#hard_failures[@]} > 0 )); then
    decision="REJECT"
    summary="At least one hard gate failed."
elif (( ${#hard_holds[@]} == 0 && ${#soft_lows[@]} == 0 && soft_high_count >= 3 )); then
    decision="PASS"
    summary="All hard gates are clear and the opportunity is attractive enough to execute."
fi

printf 'decision=%s\n' "$decision"
printf 'summary=%s\n' "$summary"

for factor in "${hard_factors[@]}"; do
    printf '%s=%s\n' "$factor" "${ratings[$factor]}"
done

for factor in "${soft_factors[@]}"; do
    printf '%s=%s\n' "$factor" "${ratings[$factor]}"
done

if (( ${#hard_failures[@]} > 0 )); then
    printf 'hard_failures=%s\n' "$(IFS=,; echo "${hard_failures[*]}")"
fi

if (( ${#hard_holds[@]} > 0 )); then
    printf 'hard_holds=%s\n' "$(IFS=,; echo "${hard_holds[*]}")"
fi

if (( ${#soft_lows[@]} > 0 )); then
    printf 'soft_lows=%s\n' "$(IFS=,; echo "${soft_lows[*]}")"
fi

printf 'soft_high_count=%s\n' "$soft_high_count"
