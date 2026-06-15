#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 6 ]]; then
  echo "Usage: $0 <legal> <consent> <data_provenance> <platform_risk> <automation_level> <margin_profile>"
  exit 1
fi

legal="$1"
consent="$2"
data_provenance="$3"
platform_risk="$4"
automation_level="$5"
margin_profile="$6"

level_to_points() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
    *)
      echo "Unsupported level: $1" >&2
      exit 1
      ;;
  esac
}

reasons=()

if [[ "$legal" == "no" ]]; then
  reasons+=("legal basis failed")
  printf 'REJECT\nReasons: %s\n' "${reasons[*]}"
  exit 0
fi

if [[ "$data_provenance" == "private" ]]; then
  reasons+=("private or restricted data source")
  printf 'REJECT\nReasons: %s\n' "${reasons[*]}"
  exit 0
fi

if [[ "$consent" == "no" ]]; then
  reasons+=("missing consent for the proposed use")
  printf 'REJECT\nReasons: %s\n' "${reasons[*]}"
  exit 0
fi

status="PASS"

if [[ "$consent" == "unclear" ]]; then
  status="HOLD"
  reasons+=("consent needs verification")
fi

if [[ "$data_provenance" == "unclear" ]]; then
  status="HOLD"
  reasons+=("data provenance is unclear")
fi

if [[ "$data_provenance" != "first_party" && "$data_provenance" != "licensed" && "$data_provenance" != "public" && "$data_provenance" != "unclear" && "$data_provenance" != "private" ]]; then
  echo "Unsupported data provenance: $data_provenance" >&2
  exit 1
fi

if [[ "$platform_risk" == "high" ]]; then
  status="HOLD"
  reasons+=("high platform dependency or enforcement risk")
fi

score=$(( $(level_to_points "$automation_level") + $(level_to_points "$margin_profile") ))

if (( score <= 2 )); then
  status="HOLD"
  reasons+=("weak automation and margin profile")
fi

if [[ ${#reasons[@]} -eq 0 ]]; then
  reasons+=("lawful data source and acceptable operating profile")
fi

printf '%s\n' "$status"
printf 'Reasons: %s\n' "$(IFS='; '; echo "${reasons[*]}")"
