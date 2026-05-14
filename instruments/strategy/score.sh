#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "usage: $0 legality consent provenance platform_alignment time_to_cash margin repeatability automation_fit defensibility" >&2
    echo "each value must be: low | medium | high" >&2
}

if [[ $# -ne 9 ]]; then
    usage
    exit 1
fi

validate() {
    local value="$1"
    case "$value" in
        low|medium|high) ;;
        *)
            echo "invalid value: $value" >&2
            usage
            exit 1
            ;;
    esac
}

for arg in "$@"; do
    validate "$arg"
done

legality="$1"
consent="$2"
provenance="$3"
platform_alignment="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation_fit="$8"
defensibility="$9"

hard_factors=("$legality" "$consent" "$provenance" "$platform_alignment")
soft_factors=("$time_to_cash" "$margin" "$repeatability" "$automation_fit" "$defensibility")

for factor in "${hard_factors[@]}"; do
    if [[ "$factor" == "low" ]]; then
        echo "REJECT"
        exit 0
    fi
done

for factor in "${hard_factors[@]}"; do
    if [[ "$factor" != "high" ]]; then
        echo "HOLD"
        exit 0
    fi
done

soft_high=0
for factor in "${soft_factors[@]}"; do
    if [[ "$factor" == "low" ]]; then
        echo "HOLD"
        exit 0
    fi
    if [[ "$factor" == "high" ]]; then
        ((soft_high+=1))
    fi
done

if (( soft_high >= 3 )); then
    echo "PASS"
else
    echo "HOLD"
fi
