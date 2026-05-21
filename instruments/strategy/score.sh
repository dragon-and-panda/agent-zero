#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <legality> <consent> <data_provenance> <platform_risk> <unit_economics> <automation_fit>" >&2
  echo "Each value must be: low | medium | high" >&2
}

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "Invalid level: $1" >&2
      usage
      exit 2
      ;;
  esac
}

score_level() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
  esac
}

if [[ $# -ne 6 ]]; then
  usage
  exit 2
fi

legality="$1"
consent="$2"
data_provenance="$3"
platform_risk="$4"
unit_economics="$5"
automation_fit="$6"

for level in "$legality" "$consent" "$data_provenance" "$platform_risk" "$unit_economics" "$automation_fit"; do
  validate_level "$level"
done

if [[ "$legality" != "high" ]]; then
  echo "decision=REJECT"
  echo "reason=legal_basis_insufficient"
  exit 0
fi

if [[ "$consent" != "high" ]]; then
  echo "decision=REJECT"
  echo "reason=consent_insufficient"
  exit 0
fi

if [[ "$data_provenance" != "high" ]]; then
  echo "decision=REJECT"
  echo "reason=data_provenance_insufficient"
  exit 0
fi

if [[ "$platform_risk" == "high" ]]; then
  echo "decision=REJECT"
  echo "reason=platform_risk_too_high"
  exit 0
fi

economics_score="$(score_level "$unit_economics")"
automation_score="$(score_level "$automation_fit")"

if [[ "$platform_risk" == "medium" ]]; then
  echo "decision=HOLD"
  echo "reason=platform_risk_requires_review"
  echo "execution_score=$((economics_score + automation_score))/6"
  exit 0
fi

if [[ "$unit_economics" == "low" || "$automation_fit" == "low" ]]; then
  echo "decision=HOLD"
  echo "reason=execution_fundamentals_too_weak"
  echo "execution_score=$((economics_score + automation_score))/6"
  exit 0
fi

if [[ "$unit_economics" == "high" || "$automation_fit" == "high" ]]; then
  echo "decision=PASS"
  echo "reason=compliant_with_workable_upside"
  echo "execution_score=$((economics_score + automation_score))/6"
  exit 0
fi

echo "decision=HOLD"
echo "reason=compliant_but_needs_stronger_upside"
echo "execution_score=$((economics_score + automation_score))/6"
