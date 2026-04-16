#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh "Opportunity name" legality consent data_provenance tos_alignment repeatability monetization_clarity

Ratings must be one of: low, medium, high

Hard gates:
  legality
  consent
  data_provenance
  tos_alignment

Results:
  REJECT -> any hard gate is low
  HOLD   -> no hard gate is low, but at least one hard gate is medium
  PASS/HOLD after business scoring when all hard gates are high
EOF
}

if [[ $# -ne 7 ]]; then
  usage
  exit 1
fi

opportunity="$1"
legality="$2"
consent="$3"
data_provenance="$4"
tos_alignment="$5"
repeatability="$6"
monetization_clarity="$7"

normalize_level() {
  case "$1" in
    low|medium|high)
      printf '%s' "$1"
      ;;
    *)
      echo "Invalid rating: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
}

level_to_score() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
  esac
}

legality="$(normalize_level "$legality")"
consent="$(normalize_level "$consent")"
data_provenance="$(normalize_level "$data_provenance")"
tos_alignment="$(normalize_level "$tos_alignment")"
repeatability="$(normalize_level "$repeatability")"
monetization_clarity="$(normalize_level "$monetization_clarity")"

hard_gate_reasons=()
hold_reasons=()

check_hard_gate() {
  local label="$1"
  local value="$2"

  if [[ "$value" == "low" ]]; then
    hard_gate_reasons+=("$label is low")
  elif [[ "$value" == "medium" ]]; then
    hold_reasons+=("$label is medium")
  fi
}

check_hard_gate "legality" "$legality"
check_hard_gate "consent" "$consent"
check_hard_gate "data_provenance" "$data_provenance"
check_hard_gate "tos_alignment" "$tos_alignment"

if [[ ${#hard_gate_reasons[@]} -gt 0 ]]; then
  printf 'Result: REJECT\n'
  printf 'Opportunity: %s\n' "$opportunity"
  printf 'Reason: hard gate failure (%s)\n' "$(IFS='; '; echo "${hard_gate_reasons[*]}")"
  exit 0
fi

if [[ ${#hold_reasons[@]} -gt 0 ]]; then
  printf 'Result: HOLD\n'
  printf 'Opportunity: %s\n' "$opportunity"
  printf 'Reason: compliance review needed (%s)\n' "$(IFS='; '; echo "${hold_reasons[*]}")"
  exit 0
fi

repeatability_score="$(level_to_score "$repeatability")"
monetization_score="$(level_to_score "$monetization_clarity")"
business_total=$((repeatability_score + monetization_score))

printf 'Opportunity: %s\n' "$opportunity"
printf 'Business score: %s/6\n' "$business_total"

if (( business_total >= 5 )); then
  printf 'Result: PASS\n'
  printf 'Reason: all hard gates are high and the offer looks repeatable with clear monetization.\n'
else
  printf 'Result: HOLD\n'
  printf 'Reason: compliant, but repeatability or monetization clarity is not yet strong enough.\n'
fi
