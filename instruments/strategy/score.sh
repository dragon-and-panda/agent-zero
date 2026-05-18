#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <legality_risk> <consent_risk> <provenance_risk> <platform_risk> <automation_risk>"
  echo "Each risk must be one of: low medium high"
}

score_of() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
    *)
      echo "Invalid risk level: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

if [ "$#" -ne 5 ]; then
  usage >&2
  exit 1
fi

legality_risk="$1"
consent_risk="$2"
provenance_risk="$3"
platform_risk="$4"
automation_risk="$5"

if [ "$legality_risk" = "high" ] || [ "$consent_risk" = "high" ] || [ "$provenance_risk" = "high" ]; then
  decision="REJECT"
  rationale="Hard stop: legality, consent, and data provenance cannot be high risk."
else
  total=$(( \
    $(score_of "$legality_risk") + \
    $(score_of "$consent_risk") + \
    $(score_of "$provenance_risk") + \
    $(score_of "$platform_risk") + \
    $(score_of "$automation_risk") \
  ))

  if [ "$platform_risk" = "high" ]; then
    decision="HOLD"
    rationale="Platform risk is too high; rework the channel or operating model first."
  elif [ "$total" -le 1 ]; then
    decision="PASS"
    rationale="Low aggregate risk across legality, consent, provenance, platform, and automation."
  elif [ "$total" -le 4 ]; then
    decision="HOLD"
    rationale="Potentially viable, but controls or narrower scope are required before execution."
  else
    decision="REJECT"
    rationale="Aggregate risk is too high for autonomous execution."
  fi
fi

printf 'DECISION=%s\n' "$decision"
printf 'LEGALITY_RISK=%s\n' "$legality_risk"
printf 'CONSENT_RISK=%s\n' "$consent_risk"
printf 'PROVENANCE_RISK=%s\n' "$provenance_risk"
printf 'PLATFORM_RISK=%s\n' "$platform_risk"
printf 'AUTOMATION_RISK=%s\n' "$automation_risk"
printf 'RATIONALE=%s\n' "$rationale"
