#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <legality> <consent> <data_provenance> <platform_risk> <repeatability> <margin>" >&2
  echo "Each value must be: low, medium, or high" >&2
}

normalize() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "Invalid level: $1" >&2
      usage
      exit 1
      ;;
  esac
}

if [[ $# -ne 6 ]]; then
  usage
  exit 1
fi

legality="$(normalize "$1")"
consent="$(normalize "$2")"
data_provenance="$(normalize "$3")"
platform_risk="$(normalize "$4")"
repeatability="$(normalize "$5")"
margin="$(normalize "$6")"

for level in "$legality" "$consent" "$data_provenance" "$platform_risk" "$repeatability" "$margin"; do
  validate_level "$level"
done

decision="PASS"
reasons=()

if [[ "$legality" != "high" ]]; then
  if [[ "$legality" == "low" ]]; then
    decision="REJECT"
    reasons+=("legality is low")
  else
    decision="HOLD"
    reasons+=("legality needs review")
  fi
fi

if [[ "$consent" == "low" ]]; then
  decision="REJECT"
  reasons+=("consent is low")
elif [[ "$consent" == "medium" && "$decision" != "REJECT" ]]; then
  decision="HOLD"
  reasons+=("consent is not explicit enough")
fi

if [[ "$data_provenance" == "low" ]]; then
  decision="REJECT"
  reasons+=("data provenance is weak")
elif [[ "$data_provenance" == "medium" && "$decision" != "REJECT" ]]; then
  decision="HOLD"
  reasons+=("data provenance should be strengthened")
fi

if [[ "$platform_risk" == "high" ]]; then
  decision="REJECT"
  reasons+=("platform risk is high")
elif [[ "$platform_risk" == "medium" && "$decision" != "REJECT" ]]; then
  decision="HOLD"
  reasons+=("platform risk needs mitigation")
fi

if [[ "$repeatability" == "low" && "$decision" == "PASS" ]]; then
  decision="HOLD"
  reasons+=("repeatability is low")
fi

if [[ "$margin" == "low" && "$decision" == "PASS" ]]; then
  decision="HOLD"
  reasons+=("margin is low")
fi

if [[ ${#reasons[@]} -eq 0 ]]; then
  reasons+=("compliance and economics are acceptable")
fi

printf 'DECISION=%s\n' "$decision"
printf 'LEGALITY=%s\n' "$legality"
printf 'CONSENT=%s\n' "$consent"
printf 'DATA_PROVENANCE=%s\n' "$data_provenance"
printf 'PLATFORM_RISK=%s\n' "$platform_risk"
printf 'REPEATABILITY=%s\n' "$repeatability"
printf 'MARGIN=%s\n' "$margin"
printf 'REASONS=%s\n' "$(IFS='; '; echo "${reasons[*]}")"
