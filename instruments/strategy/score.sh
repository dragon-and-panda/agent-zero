#!/usr/bin/env bash
set -euo pipefail

declare -A RATINGS=()
REQUIRED_KEYS=(
  legality
  consent
  provenance
  platform_risk
  time
  margin
  repeatability
  automation
  defensibility
)

usage() {
  echo "Usage: $0 key=value ..." >&2
  echo "Required keys: ${REQUIRED_KEYS[*]}" >&2
}

normalize_rating() {
  local value="${1:-}"
  case "${value,,}" in
    low|medium|high)
      printf '%s\n' "${value,,}"
      ;;
    *)
      return 1
      ;;
  esac
}

for arg in "$@"; do
  if [[ "$arg" != *=* ]]; then
    usage
    exit 1
  fi
  key="${arg%%=*}"
  value="${arg#*=}"
  if ! rating="$(normalize_rating "$value")"; then
    echo "Invalid rating for $key: $value" >&2
    exit 1
  fi
  RATINGS["$key"]="$rating"
done

for key in "${REQUIRED_KEYS[@]}"; do
  if [[ -z "${RATINGS[$key]:-}" ]]; then
    echo "Missing required key: $key" >&2
    usage
    exit 1
  fi
done

hard_failures=()
hard_holds=()

case "${RATINGS[legality]}" in
  low) hard_failures+=("legality is low") ;;
  medium) hard_holds+=("legality is not yet high") ;;
esac

case "${RATINGS[consent]}" in
  low) hard_failures+=("consent is low") ;;
  medium) hard_holds+=("consent is not yet high") ;;
esac

case "${RATINGS[provenance]}" in
  low) hard_failures+=("data provenance is low") ;;
  medium) hard_holds+=("data provenance is not yet high") ;;
esac

case "${RATINGS[platform_risk]}" in
  high) hard_failures+=("platform risk is high") ;;
  medium) hard_holds+=("platform risk is not yet low") ;;
esac

soft_high=0
soft_low=0
for key in time margin repeatability automation defensibility; do
  case "${RATINGS[$key]}" in
    high) ((soft_high += 1)) ;;
    low) ((soft_low += 1)) ;;
  esac
done

decision="PASS"
message="All hard gates cleared and soft factors support activation."

if (( ${#hard_failures[@]} > 0 )); then
  decision="REJECT"
  message="At least one hard gate failed."
elif (( ${#hard_holds[@]} > 0 )); then
  decision="HOLD"
  message="Hard gates are incomplete or still medium."
elif (( soft_low > 0 )); then
  decision="HOLD"
  message="Hard gates cleared, but at least one soft execution factor is low."
elif (( soft_high < 3 )); then
  decision="HOLD"
  message="Hard gates cleared, but fewer than three soft factors are high."
fi

printf 'decision=%s\n' "$decision"
printf 'hard_failures=%s\n' "${#hard_failures[@]}"
printf 'hard_holds=%s\n' "${#hard_holds[@]}"
printf 'soft_high=%s\n' "$soft_high"
printf 'soft_low=%s\n' "$soft_low"
printf 'message=%s\n' "$message"

index=1
for reason in "${hard_failures[@]}"; do
  printf 'reason_%s=%s\n' "$index" "$reason"
  ((index += 1))
done
for reason in "${hard_holds[@]}"; do
  printf 'reason_%s=%s\n' "$index" "$reason"
  ((index += 1))
done
