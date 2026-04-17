#!/usr/bin/env bash

set -euo pipefail

declare -A values=()

for arg in "$@"; do
    key="${arg%%=*}"
    value="${arg#*=}"
    values["$key"]="$value"
done

required_keys=(
    legality
    consent
    provenance
    tos
    time
    margin
    repeatability
    automation
    defensibility
)

valid_levels=("low" "medium" "high")

is_valid_level() {
    local candidate="$1"
    local level
    for level in "${valid_levels[@]}"; do
        if [[ "$candidate" == "$level" ]]; then
            return 0
        fi
    done
    return 1
}

for key in "${required_keys[@]}"; do
    if [[ -z "${values[$key]:-}" ]]; then
        echo "ERROR missing required input: $key" >&2
        exit 1
    fi

    if ! is_valid_level "${values[$key]}"; then
        echo "ERROR invalid level for $key: ${values[$key]}" >&2
        echo "Expected one of: low, medium, high" >&2
        exit 1
    fi
done

hard_gates=(legality consent provenance tos)
soft_factors=(time margin repeatability automation defensibility)

for key in "${hard_gates[@]}"; do
    if [[ "${values[$key]}" != "high" ]]; then
        echo "REJECT"
        echo "reason=hard_gate_failed:$key"
        exit 0
    fi
done

for key in "${soft_factors[@]}"; do
    if [[ "${values[$key]}" == "low" ]]; then
        echo "HOLD"
        echo "reason=soft_factor_low:$key"
        exit 0
    fi
done

echo "PASS"
echo "reason=all_hard_gates_clear"
