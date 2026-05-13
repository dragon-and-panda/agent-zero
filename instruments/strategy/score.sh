#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: score.sh <legality_confidence> <consent_strength> <data_rights_confidence> <platform_risk>"
  exit 1
fi

legality="$1"
consent="$2"
data_rights="$3"
platform_risk="$4"

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid value: $1 (expected low|medium|high)"
      exit 1
      ;;
  esac
}

validate_level "$legality"
validate_level "$consent"
validate_level "$data_rights"
validate_level "$platform_risk"

decision="PASS"
reason="clear to move into planning"

if [[ "$legality" != "high" ]]; then
  decision="REJECT"
  reason="legality confidence must be high"
elif [[ "$consent" == "low" || "$data_rights" == "low" ]]; then
  decision="REJECT"
  reason="consent and data rights cannot be low"
elif [[ "$platform_risk" == "high" ]]; then
  decision="REJECT"
  reason="platform risk is too high"
elif [[ "$consent" != "high" || "$data_rights" != "high" || "$platform_risk" == "medium" ]]; then
  decision="HOLD"
  reason="add controls or evidence before planning"
fi

printf 'decision=%s\n' "$decision"
printf 'legality_confidence=%s\n' "$legality"
printf 'consent_strength=%s\n' "$consent"
printf 'data_rights_confidence=%s\n' "$data_rights"
printf 'platform_risk=%s\n' "$platform_risk"
printf 'reason=%s\n' "$reason"
