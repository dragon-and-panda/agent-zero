#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 7 ]; then
  echo "usage: $0 legality consent provenance platform_risk margin speed defensibility"
  exit 1
fi

to_score() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
    *)
      echo "invalid input: $1 (expected low|medium|high)" >&2
      exit 1
      ;;
  esac
}

invert_score() {
  case "$1" in
    low) echo 2 ;;
    medium) echo 1 ;;
    high) echo 0 ;;
    *)
      echo "invalid input: $1 (expected low|medium|high)" >&2
      exit 1
      ;;
  esac
}

legality="$1"
consent="$2"
provenance="$3"
platform_risk="$4"
margin="$5"
speed="$6"
defensibility="$7"

notes=()

if [ "$legality" != "high" ]; then
  notes+=("legality must be high")
  verdict="REJECT"
fi

if [ "$consent" = "low" ]; then
  notes+=("consent is too weak")
  verdict="REJECT"
fi

if [ "$provenance" = "low" ]; then
  notes+=("data provenance is too weak")
  verdict="REJECT"
fi

if [ "$platform_risk" = "high" ]; then
  notes+=("platform risk is too high")
  verdict="REJECT"
fi

if [ "${verdict:-}" != "REJECT" ] && { [ "$consent" = "medium" ] || [ "$provenance" = "medium" ]; }; then
  verdict="HOLD"
  notes+=("clarify consent and provenance before execution")
fi

score=$(( \
  $(to_score "$legality") + \
  $(to_score "$consent") + \
  $(to_score "$provenance") + \
  $(invert_score "$platform_risk") + \
  $(to_score "$margin") + \
  $(to_score "$speed") + \
  $(to_score "$defensibility") \
))

if [ -z "${verdict:-}" ]; then
  if [ "$score" -ge 10 ]; then
    verdict="PASS"
  else
    verdict="HOLD"
    notes+=("economics or defensibility need improvement")
  fi
fi

echo "verdict=$verdict"
echo "score=$score/14"
if [ "${#notes[@]}" -gt 0 ]; then
  printf 'notes=%s\n' "$(IFS='; '; echo "${notes[*]}")"
fi
