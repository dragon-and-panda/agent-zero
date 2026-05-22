#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 9 ]; then
  echo "usage: score.sh legality consent provenance platform_alignment time_to_cash margin repeatability automation defensibility" >&2
  exit 1
fi

ratings=("$@")
names=(
  legality
  consent
  provenance
  platform_alignment
  time_to_cash
  margin
  repeatability
  automation
  defensibility
)

validate_rating() {
  case "$1" in
    low|medium|high) ;;
    *)
      echo "invalid rating: $1" >&2
      exit 1
      ;;
  esac
}

join_by() {
  local separator="$1"
  shift || true
  local first=1
  for item in "$@"; do
    if [ $first -eq 1 ]; then
      printf "%s" "$item"
      first=0
    else
      printf "%s%s" "$separator" "$item"
    fi
  done
}

hard_failures=()
hard_warnings=()
soft_lows=()
soft_highs=()

for rating in "${ratings[@]}"; do
  validate_rating "$rating"
done

for i in "${!names[@]}"; do
  name="${names[$i]}"
  rating="${ratings[$i]}"
  case "$name" in
    legality|consent|provenance|platform_alignment)
      if [ "$rating" = "low" ]; then
        hard_failures+=("$name")
      elif [ "$rating" = "medium" ]; then
        hard_warnings+=("$name")
      fi
      ;;
    *)
      if [ "$rating" = "low" ]; then
        soft_lows+=("$name")
      elif [ "$rating" = "high" ]; then
        soft_highs+=("$name")
      fi
      ;;
  esac
done

decision="HOLD"
rationale="Compliant lane needs stronger economics or clearer evidence."

if [ "${#hard_failures[@]}" -gt 0 ]; then
  decision="REJECT"
  rationale="One or more hard gates failed."
elif [ "${#hard_warnings[@]}" -gt 0 ]; then
  decision="HOLD"
  rationale="Hard gates are not yet strong enough for execution."
elif [ "${#soft_lows[@]}" -gt 0 ]; then
  decision="HOLD"
  rationale="Compliance gates passed, but one or more soft factors are weak."
elif [ "${#soft_highs[@]}" -ge 3 ]; then
  decision="PASS"
  rationale="Hard gates passed and enough soft factors are strong."
fi

echo "decision=$decision"
echo "rationale=$rationale"
echo "hard_failures=$(join_by , "${hard_failures[@]:-}")"
echo "hard_warnings=$(join_by , "${hard_warnings[@]:-}")"
echo "soft_lows=$(join_by , "${soft_lows[@]:-}")"
echo "soft_highs=$(join_by , "${soft_highs[@]:-}")"
