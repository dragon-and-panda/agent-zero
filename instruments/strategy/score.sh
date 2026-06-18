#!/bin/bash

set -euo pipefail

if [ "$#" -ne 5 ]; then
  echo "usage: bash /workspace/instruments/strategy/score.sh <legality> <consent> <provenance> <platform_risk> <unit_economics>"
  exit 1
fi

legality="$1"
consent="$2"
provenance="$3"
platform_risk="$4"
unit_economics="$5"

for value in "$legality" "$consent" "$provenance" "$platform_risk" "$unit_economics"; do
  case "$value" in
    low|medium|high) ;;
    *)
      echo "all inputs must be one of: low medium high"
      exit 1
      ;;
  esac
done

decision="PASS"
reason="controls look acceptable for a small compliant experiment"

if [ "$legality" != "high" ]; then
  decision="REJECT"
  reason="legality confidence must be high"
elif [ "$consent" != "high" ]; then
  decision="REJECT"
  reason="consent quality must be high"
elif [ "$provenance" = "low" ]; then
  decision="REJECT"
  reason="data provenance is too weak"
elif [ "$platform_risk" = "high" ]; then
  decision="REJECT"
  reason="platform enforcement risk is too high"
elif [ "$provenance" = "medium" ] || [ "$platform_risk" = "medium" ] || [ "$unit_economics" = "low" ]; then
  decision="HOLD"
  reason="improve controls or economics before proceeding"
fi

printf '%s\n' "decision=$decision"
printf '%s\n' "reason=$reason"
printf '%s\n' "inputs=legality:$legality consent:$consent provenance:$provenance platform_risk:$platform_risk unit_economics:$unit_economics"
