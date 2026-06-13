#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 8 ]]; then
  echo "usage: $0 legality consent provenance tos time margin repeatability automation" >&2
  echo "values: low medium high" >&2
  exit 2
fi

for value in "$@"; do
  case "$value" in
    low|medium|high) ;;
    *)
      echo "invalid value: $value" >&2
      exit 2
      ;;
  esac
done

legality="$1"
consent="$2"
provenance="$3"
tos="$4"
time_to_cash="$5"
margin="$6"
repeatability="$7"
automation="$8"

hard_fail=0
soft_hold=0
soft_low=0

for value in "$legality" "$consent" "$provenance" "$tos"; do
  if [[ "$value" == "low" ]]; then
    hard_fail=1
  elif [[ "$value" == "medium" ]]; then
    soft_hold=1
  fi
done

for value in "$time_to_cash" "$margin" "$repeatability" "$automation"; do
  if [[ "$value" == "low" ]]; then
    soft_low=1
  elif [[ "$value" == "medium" ]]; then
    soft_hold=1
  fi
done

if [[ "$hard_fail" -eq 1 ]]; then
  echo "REJECT"
elif [[ "$soft_hold" -eq 1 || "$soft_low" -eq 1 ]]; then
  echo "HOLD"
else
  echo "PASS"
fi
