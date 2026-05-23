#!/usr/bin/env bash

set -euo pipefail

legality=medium
consent=medium
provenance=medium
platform=medium
time=medium
margin=medium
repeatability=medium
automation=medium
defensibility=medium

while [[ $# -gt 0 ]]; do
  case "$1" in
    --legality) legality="${2:-}"; shift 2 ;;
    --consent) consent="${2:-}"; shift 2 ;;
    --provenance) provenance="${2:-}"; shift 2 ;;
    --platform) platform="${2:-}"; shift 2 ;;
    --time) time="${2:-}"; shift 2 ;;
    --margin) margin="${2:-}"; shift 2 ;;
    --repeatability) repeatability="${2:-}"; shift 2 ;;
    --automation) automation="${2:-}"; shift 2 ;;
    --defensibility) defensibility="${2:-}"; shift 2 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

validate_rating() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "Invalid rating: $1 (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

for rating in \
  "$legality" "$consent" "$provenance" "$platform" \
  "$time" "$margin" "$repeatability" "$automation" "$defensibility"
do
  validate_rating "$rating"
done

hard_names=(legality consent provenance platform)
hard_values=("$legality" "$consent" "$provenance" "$platform")
soft_names=(time margin repeatability automation defensibility)
soft_values=("$time" "$margin" "$repeatability" "$automation" "$defensibility")

hard_medium=0
soft_low=0
soft_high=0

for i in "${!hard_names[@]}"; do
  if [[ "${hard_values[$i]}" == "low" ]]; then
    echo "REJECT"
    exit 0
  fi
  if [[ "${hard_values[$i]}" == "medium" ]]; then
    hard_medium=1
  fi
done

for i in "${!soft_names[@]}"; do
  if [[ "${soft_values[$i]}" == "low" ]]; then
    soft_low=1
  fi
  if [[ "${soft_values[$i]}" == "high" ]]; then
    soft_high=$((soft_high + 1))
  fi
done

if [[ "$hard_medium" -eq 1 || "$soft_low" -eq 1 || "$soft_high" -lt 3 ]]; then
  echo "HOLD"
else
  echo "PASS"
fi
