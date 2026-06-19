#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 <legality-risk> <consent-risk> <provenance-risk> <platform-risk>"
    echo "Each risk must be one of: low medium high"
}

validate_risk() {
    case "$1" in
        low|medium|high) ;;
        *)
            echo "Invalid risk value: $1" >&2
            usage
            exit 1
            ;;
    esac
}

if [ "$#" -ne 4 ]; then
    usage
    exit 1
fi

legality="$1"
consent="$2"
provenance="$3"
platform="$4"

validate_risk "$legality"
validate_risk "$consent"
validate_risk "$provenance"
validate_risk "$platform"

decision="PASS"
reasons=()

if [ "$legality" = "high" ]; then
    decision="REJECT"
    reasons+=("legality risk is high")
fi

if [ "$consent" = "high" ]; then
    decision="REJECT"
    reasons+=("consent risk is high")
fi

if [ "$decision" != "REJECT" ] && [ "$provenance" = "high" ]; then
    decision="HOLD"
    reasons+=("provenance risk is high")
fi

if [ "$decision" != "REJECT" ] && [ "$platform" = "high" ]; then
    decision="HOLD"
    reasons+=("platform risk is high")
fi

if [ "$decision" = "PASS" ] && { [ "$legality" = "medium" ] || [ "$consent" = "medium" ] || [ "$provenance" = "medium" ] || [ "$platform" = "medium" ]; }; then
    decision="HOLD"
    reasons+=("at least one risk factor is medium")
fi

echo "Decision: $decision"
echo "Legality risk: $legality"
echo "Consent risk: $consent"
echo "Provenance risk: $provenance"
echo "Platform risk: $platform"

if [ "${#reasons[@]}" -gt 0 ]; then
    echo "Reasons:"
    for reason in "${reasons[@]}"; do
        echo "- $reason"
    done
fi
