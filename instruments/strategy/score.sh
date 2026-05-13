#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <legality> <consent> <data_provenance> <platform_risk>"
  echo "Allowed values: low medium high"
}

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "Invalid value: $1"
      usage
      exit 2
      ;;
  esac
}

if [ "$#" -ne 4 ]; then
  usage
  exit 2
fi

legality="$1"
consent="$2"
data_provenance="$3"
platform_risk="$4"

validate_level "$legality"
validate_level "$consent"
validate_level "$data_provenance"
validate_level "$platform_risk"

reasons=()
status="PASS"

if [ "$legality" = "low" ]; then
  reasons+=("legality is low")
fi

if [ "$consent" = "low" ]; then
  reasons+=("consent is low")
fi

if [ "$data_provenance" = "low" ]; then
  reasons+=("data provenance is low")
fi

if [ "$platform_risk" = "high" ]; then
  reasons+=("platform risk is high")
fi

if [ "${#reasons[@]}" -gt 0 ]; then
  status="REJECT"
elif [ "$legality" = "medium" ] || [ "$consent" = "medium" ] || [ "$data_provenance" = "medium" ] || [ "$platform_risk" != "low" ]; then
  status="HOLD"
  reasons+=("one or more controls need clarification")
else
  reasons+=("all governance gates passed")
fi

printf "STATUS: %s\n" "$status"
printf "LEGALITY: %s\n" "$legality"
printf "CONSENT: %s\n" "$consent"
printf "DATA_PROVENANCE: %s\n" "$data_provenance"
printf "PLATFORM_RISK: %s\n" "$platform_risk"
printf "REASONS:\n"

for reason in "${reasons[@]}"; do
  printf -- "- %s\n" "$reason"
done
