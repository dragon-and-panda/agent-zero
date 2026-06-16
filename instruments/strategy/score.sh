#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "usage: $0 <legality> <consent> <provenance> <platform_risk> <durability> <automation_fit>"
  echo "accepted values: low medium high"
}

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid level: $1" >&2
      usage
      exit 2
      ;;
  esac
}

legality="${1:-}"
consent="${2:-}"
provenance="${3:-}"
platform_risk="${4:-}"
durability="${5:-}"
automation_fit="${6:-}"

if [[ -z "$automation_fit" ]]; then
  usage
  exit 2
fi

for value in "$legality" "$consent" "$provenance" "$platform_risk" "$durability" "$automation_fit"; do
  validate_level "$value"
done

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" ]]; then
  echo "REJECT: hard gate failed on legality consent or provenance"
  exit 0
fi

if [[ "$legality" == "medium" || "$consent" == "medium" || "$provenance" == "medium" ]]; then
  echo "HOLD: clarify legality consent or provenance before execution"
  exit 0
fi

if [[ "$platform_risk" == "high" ]]; then
  echo "HOLD: platform dependency risk is too high"
  exit 0
fi

score=0

case "$durability" in
  high) score=$((score + 2)) ;;
  medium) score=$((score + 1)) ;;
esac

case "$automation_fit" in
  high) score=$((score + 2)) ;;
  medium) score=$((score + 1)) ;;
esac

case "$platform_risk" in
  low) score=$((score + 1)) ;;
esac

if (( score >= 4 )); then
  echo "PASS: compliant and automation-friendly"
else
  echo "HOLD: compliant but weak on durability or automation fit"
fi
