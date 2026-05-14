#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 5 ]; then
  echo "usage: $0 <legality> <consent> <provenance> <platform_risk> <offer_clarity>" >&2
  echo "levels: low medium high" >&2
  exit 2
fi

normalize_level() {
  case "$1" in
    low|medium|high) echo "$1" ;;
    *)
      echo "invalid level: $1" >&2
      exit 2
      ;;
  esac
}

level_score() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
  esac
}

legality="$(normalize_level "$1")"
consent="$(normalize_level "$2")"
provenance="$(normalize_level "$3")"
platform_risk="$(normalize_level "$4")"
offer_clarity="$(normalize_level "$5")"

if [ "$legality" = "low" ]; then
  echo "REJECT: legal confidence is too low"
  exit 0
fi

if [ "$consent" = "low" ]; then
  echo "REJECT: consent quality is too low"
  exit 0
fi

if [ "$provenance" = "low" ]; then
  echo "REJECT: data provenance is too weak"
  exit 0
fi

if [ "$platform_risk" = "high" ]; then
  echo "REJECT: platform risk is too high"
  exit 0
fi

total=$(( $(level_score "$legality") + $(level_score "$consent") + $(level_score "$provenance") + $(level_score "$offer_clarity") ))

if [ "$platform_risk" = "medium" ]; then
  total=$(( total - 1 ))
fi

if [ "$total" -ge 6 ]; then
  echo "PASS: compliant candidate with enough clarity to prototype"
else
  echo "HOLD: improve offer clarity or reduce operational risk before building"
fi
