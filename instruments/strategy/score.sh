#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="${1:-docs/strategy/incoming.md}"

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file not found: $INPUT_FILE" >&2
  exit 1
fi

trim() {
  local value="$*"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

is_rule_row() {
  [[ "$1" =~ ^-+$ ]]
}

score_tmp="$(mktemp)"
best_tmp="$(mktemp)"
trap 'rm -f "$score_tmp" "$best_tmp"' EXIT

while IFS='|' read -r _ c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 _; do
  id="$(trim "${c1:-}")"
  opportunity="$(trim "${c2:-}")"
  compliance="$(trim "${c3:-}")"
  automation_fit="$(trim "${c4:-}")"
  speed_to_revenue="$(trim "${c5:-}")"
  effort="$(trim "${c6:-}")"
  risk="$(trim "${c7:-}")"
  capital_required="$(trim "${c8:-}")"
  redundancy="$(trim "${c9:-}")"
  notes="$(trim "${c10:-}")"

  [[ -z "$id" ]] && continue
  [[ "$id" == "id" ]] && continue
  is_rule_row "$id" && continue

  if [[ "$compliance" == "REJECT" ]]; then
    score=0
    decision="REJECT"
  else
    weighted_total=$(( \
      automation_fit * 25 + \
      speed_to_revenue * 20 + \
      redundancy * 15 + \
      (6 - effort) * 10 + \
      (6 - risk) * 20 + \
      (6 - capital_required) * 10 \
    ))
    score=$(( weighted_total / 5 ))

    if [[ "$compliance" == "HOLD" ]]; then
      decision="HOLD"
    elif (( score >= 75 )); then
      decision="GO"
    elif (( score >= 60 )); then
      decision="VALIDATE"
    else
      decision="HOLD"
    fi
  fi

  printf '%s\t%s\t%d\t%s\t%s\n' \
    "$id" "$compliance" "$score" "$decision" "$opportunity" >> "$score_tmp"

  if [[ "$decision" == "GO" || "$decision" == "VALIDATE" ]]; then
    printf '%d\t%s\t%s\t%s\n' \
      "$score" "$id" "$decision" "$opportunity" >> "$best_tmp"
  fi
done < "$INPUT_FILE"

echo "# Strategy Scores"
echo
printf '| %-24s | %-10s | %-5s | %-8s | %s |\n' "id" "compliance" "score" "decision" "opportunity"
printf '|-%-24s-|-%-10s-|-%-5s-|-%-8s-|-%s-|\n' "------------------------" "----------" "-----" "--------" "-----------"

sort -t $'\t' -k3,3nr -k1,1 "$score_tmp" | while IFS=$'\t' read -r id compliance score decision opportunity; do
  printf '| %-24s | %-10s | %-5s | %-8s | %s |\n' \
    "$id" "$compliance" "$score" "$decision" "$opportunity"
done

echo
echo "## Immediate start queue"

if [[ -s "$best_tmp" ]]; then
  sort -t $'\t' -k1,1nr -k2,2 "$best_tmp" | head -n 3 | while IFS=$'\t' read -r score id decision opportunity; do
    printf -- '- %s (%s, score %d): %s\n' "$id" "$decision" "$score" "$opportunity"
  done
else
  echo "- No active GO or VALIDATE opportunities."
fi
