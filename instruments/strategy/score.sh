#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "usage: $0 <legality> <consent> <provenance> <platform> <time_to_cash> <margin> <repeatability> <automation> <defensibility>" >&2
}

if [ "$#" -ne 9 ]; then
  usage
  exit 2
fi

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid level: $1" >&2
      usage
      exit 2
      ;;
  esac
}

for level in "$@"; do
  validate_level "$level"
done

legality="$1"
consent="$2"
provenance="$3"
platform="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

if [ "$legality" = "low" ] || [ "$consent" = "low" ] || [ "$provenance" = "low" ] || [ "$platform" = "low" ]; then
  echo "REJECT hard_gates=failed legality=$legality consent=$consent provenance=$provenance platform=$platform"
  exit 0
fi

soft_levels=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility")
soft_high=0

for level in "${soft_levels[@]}"; do
  if [ "$level" = "low" ]; then
    echo "HOLD soft_factor=low time_to_cash=$time_to_cash margin=$margin repeatability=$repeatability automation=$automation defensibility=$defensibility"
    exit 0
  fi
  if [ "$level" = "high" ]; then
    soft_high=$((soft_high + 1))
  fi
done

if [ "$soft_high" -ge 3 ]; then
  echo "PASS hard_gates=clear soft_high=$soft_high"
  exit 0
fi

echo "HOLD hard_gates=clear soft_high=$soft_high"
