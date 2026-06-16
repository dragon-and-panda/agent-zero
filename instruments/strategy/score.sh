#!/usr/bin/env bash
set -euo pipefail

declare -A ratings=(
  [legality]=unknown
  [consent]=unknown
  [provenance]=unknown
  [tos]=unknown
  [time]=medium
  [margin]=medium
  [repeatability]=medium
  [automation]=medium
  [defensibility]=medium
)

lane="unnamed-lane"

normalize_rating() {
  local value
  value="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' )"
  case "$value" in
    high|yes|true|clear|allowed|pass|opt_in|opt-in) printf 'high' ;;
    low|no|false|blocked|reject) printf 'low' ;;
    medium|unknown|unclear|needs_review|needs-review|manual) printf 'medium' ;;
    *) printf '%s' "$value" ;;
  esac
}

for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  value="$(normalize_rating "$value")"
  case "$key" in
    lane) lane="$value" ;;
    legality|consent|provenance|tos|time|margin|repeatability|automation|defensibility)
      ratings["$key"]="$value"
      ;;
    *)
      printf 'Unknown key: %s\n' "$key" >&2
      exit 1
      ;;
  esac
done

hard_fields=(legality consent provenance tos)
soft_fields=(time margin repeatability automation defensibility)

hard_failures=()
hard_unclear=()
soft_lows=0
soft_highs=0

for field in "${hard_fields[@]}"; do
  case "${ratings[$field]}" in
    low) hard_failures+=("$field") ;;
    high) ;;
    *) hard_unclear+=("$field") ;;
  esac
done

for field in "${soft_fields[@]}"; do
  case "${ratings[$field]}" in
    low) soft_lows=$((soft_lows + 1)) ;;
    high) soft_highs=$((soft_highs + 1)) ;;
  esac
done

decision="HOLD"
reason="Needs clearer compliance facts or stronger economics."

if ((${#hard_failures[@]} > 0)); then
  decision="REJECT"
  reason="At least one hard gate failed."
elif ((${#hard_unclear[@]} > 0)); then
  decision="HOLD"
  reason="At least one hard gate is not yet clearly high."
elif ((soft_lows > 0)); then
  decision="HOLD"
  reason="A soft execution factor is low."
elif ((soft_highs >= 3)); then
  decision="PASS"
  reason="All hard gates are high and enough soft factors are attractive."
fi

printf 'lane=%s\n' "$lane"
for field in "${hard_fields[@]}" "${soft_fields[@]}"; do
  printf '%s=%s\n' "$field" "${ratings[$field]}"
done
printf 'soft_highs=%s\n' "$soft_highs"
printf 'decision=%s\n' "$decision"
printf 'reason=%s\n' "$reason"

