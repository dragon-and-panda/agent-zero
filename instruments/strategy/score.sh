#!/usr/bin/env bash
set -euo pipefail

LEGALITY="${1:-unknown}"
CONSENT="${2:-unknown}"
DATA_PROVENANCE="${3:-unknown}"
PLATFORM_RISK="${4:-unknown}"
REVERSIBILITY="${5:-unknown}"

normalize() {
  local value="${1:-unknown}"
  printf '%s' "$value" | tr '[:upper:]' '[:lower:]'
}

LEGALITY="$(normalize "$LEGALITY")"
CONSENT="$(normalize "$CONSENT")"
DATA_PROVENANCE="$(normalize "$DATA_PROVENANCE")"
PLATFORM_RISK="$(normalize "$PLATFORM_RISK")"
REVERSIBILITY="$(normalize "$REVERSIBILITY")"

score_level() {
  case "$1" in
    high) echo 3 ;;
    medium) echo 2 ;;
    low) echo 1 ;;
    *)
      echo "Unsupported score level: $1" >&2
      exit 2
      ;;
  esac
}

if [[ "$LEGALITY" != "high" ]]; then
  printf 'REJECT: legality gate failed (%s)\n' "$LEGALITY"
  exit 0
fi

if [[ "$CONSENT" == "low" ]]; then
  printf 'REJECT: consent gate failed (%s)\n' "$CONSENT"
  exit 0
fi

if [[ "$DATA_PROVENANCE" == "low" ]]; then
  printf 'REJECT: data provenance gate failed (%s)\n' "$DATA_PROVENANCE"
  exit 0
fi

if [[ "$PLATFORM_RISK" == "high" ]]; then
  printf 'HOLD: platform-risk gate failed (%s)\n' "$PLATFORM_RISK"
  exit 0
fi

TOTAL=0
TOTAL=$((TOTAL + $(score_level "$LEGALITY")))
TOTAL=$((TOTAL + $(score_level "$CONSENT")))
TOTAL=$((TOTAL + $(score_level "$DATA_PROVENANCE")))
TOTAL=$((TOTAL + $(score_level "$REVERSIBILITY")))

if (( TOTAL >= 11 )); then
  printf 'PASS: opportunity score=%d\n' "$TOTAL"
else
  printf 'HOLD: opportunity score=%d\n' "$TOTAL"
fi
