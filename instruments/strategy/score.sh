#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <legality-risk> <consent-risk> <provenance-risk> <platform-risk>" >&2
  echo "Each risk must be one of: low, medium, high" >&2
}

normalize() {
  local value
  value="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s\n' "$value"
      ;;
    *)
      return 1
      ;;
  esac
}

if [ "$#" -ne 4 ]; then
  usage
  exit 1
fi

legality="$(normalize "$1")" || { usage; exit 1; }
consent="$(normalize "$2")" || { usage; exit 1; }
provenance="$(normalize "$3")" || { usage; exit 1; }
platform="$(normalize "$4")" || { usage; exit 1; }

if [ "$legality" = "high" ] || [ "$provenance" = "high" ]; then
  printf 'REJECT: legality or provenance risk is high.\n'
  exit 0
fi

if [ "$consent" = "high" ] || [ "$platform" = "high" ]; then
  printf 'REJECT: consent or platform risk is high.\n'
  exit 0
fi

if [ "$legality" = "medium" ] || [ "$consent" = "medium" ] || [ "$provenance" = "medium" ] || [ "$platform" = "medium" ]; then
  printf 'HOLD: at least one risk area needs clarification or mitigation.\n'
  exit 0
fi

printf 'PASS: opportunity clears the initial compliance gate.\n'
