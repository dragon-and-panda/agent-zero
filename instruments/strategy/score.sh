#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: $0 legality consent provenance tos time margin repeatability automation defensibility"
  exit 2
fi

validate_level() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid value: $1 (expected low|medium|high)"
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
tos="$4"
time="$5"
margin="$6"
repeatability="$7"
automation="$8"
defensibility="$9"

hard_factors=(
  "legality:$legality"
  "consent:$consent"
  "provenance:$provenance"
  "tos:$tos"
)

soft_factors=(
  "time:$time"
  "margin:$margin"
  "repeatability:$repeatability"
  "automation:$automation"
  "defensibility:$defensibility"
)

has_reject=0
has_hold=0
reasons=()

for factor in "${hard_factors[@]}"; do
  name="${factor%%:*}"
  value="${factor##*:}"
  if [ "$value" = "low" ]; then
    has_reject=1
    reasons+=("$name is low")
  elif [ "$value" != "high" ]; then
    has_hold=1
    reasons+=("$name is not yet high")
  fi
done

if [ "$has_reject" -eq 0 ]; then
  for factor in "${soft_factors[@]}"; do
    name="${factor%%:*}"
    value="${factor##*:}"
    if [ "$value" = "low" ]; then
      has_hold=1
      reasons+=("$name is low")
    fi
  done
fi

if [ "$has_reject" -eq 1 ]; then
  verdict="REJECT"
elif [ "$has_hold" -eq 1 ]; then
  verdict="HOLD"
else
  verdict="PASS"
fi

echo "VERDICT: $verdict"
echo "hard_gates: legality=$legality consent=$consent provenance=$provenance tos=$tos"
echo "soft_factors: time=$time margin=$margin repeatability=$repeatability automation=$automation defensibility=$defensibility"

if [ "${#reasons[@]}" -gt 0 ]; then
  echo "reasons:"
  for reason in "${reasons[@]}"; do
    echo "- $reason"
  done
fi
