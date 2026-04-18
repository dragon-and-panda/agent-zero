#!/bin/bash

set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "Usage: $0 legality consent provenance tos time margin repeatability automation defensibility"
  echo "Each value must be one of: low medium high"
  exit 1
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    low|medium|high)
      printf '%s' "$value"
      ;;
    *)
      echo "Invalid value: $1. Use low, medium, or high." >&2
      exit 2
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
time="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"

score_for() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
  esac
}

hard_fail_reasons=()

if [ "$legality" != "high" ]; then
  hard_fail_reasons+=("legality must be high")
fi
if [ "$consent" = "low" ]; then
  hard_fail_reasons+=("consent cannot be low")
fi
if [ "$provenance" = "low" ]; then
  hard_fail_reasons+=("data provenance cannot be low")
fi
if [ "$tos" = "low" ]; then
  hard_fail_reasons+=("platform terms fit cannot be low")
fi

if [ "${#hard_fail_reasons[@]}" -gt 0 ]; then
  printf 'REJECT\n'
  printf 'Reasons:\n'
  for reason in "${hard_fail_reasons[@]}"; do
    printf -- '- %s\n' "$reason"
  done
  exit 0
fi

soft_lows=()
for pair in \
  "time:$time" \
  "margin:$margin" \
  "repeatability:$repeatability" \
  "automation:$automation" \
  "defensibility:$defensibility"
do
  name="${pair%%:*}"
  value="${pair##*:}"
  if [ "$value" = "low" ]; then
    soft_lows+=("$name")
  fi
done

total_score=$(
  expr \
    "$(score_for "$legality")" + \
    "$(score_for "$consent")" + \
    "$(score_for "$provenance")" + \
    "$(score_for "$tos")" + \
    "$(score_for "$time")" + \
    "$(score_for "$margin")" + \
    "$(score_for "$repeatability")" + \
    "$(score_for "$automation")" + \
    "$(score_for "$defensibility")"
)

if [ "${#soft_lows[@]}" -eq 0 ] && [ "$total_score" -ge 13 ]; then
  printf 'PASS\n'
  printf 'Summary:\n'
  printf -- '- hard gates cleared\n'
  printf -- '- no soft execution factor is low\n'
  printf -- '- total score: %s/18\n' "$total_score"
  exit 0
fi

printf 'HOLD\n'
printf 'Summary:\n'
printf -- '- hard gates cleared\n'
if [ "${#soft_lows[@]}" -gt 0 ]; then
  printf -- '- improve these low execution factors: %s\n' "$(IFS=', '; echo "${soft_lows[*]}")"
else
  printf -- '- raise overall quality before activation\n'
fi
printf -- '- total score: %s/18\n' "$total_score"
