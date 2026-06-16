#!/usr/bin/env bash
set -euo pipefail

impact="medium"
effort="medium"
durability="medium"
leverage="medium"
legality="unclear"
consent="missing"
provenance="unclear"
platform_risk="medium"

for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  case "${key}" in
    impact|effort|durability|leverage|legality|consent|provenance|platform_risk)
      printf -v "${key}" "%s" "${value,,}"
      ;;
    *)
      echo "unknown_input=${key}"
      ;;
  esac
done

score_value() {
  case "$1" in
    low) echo 1 ;;
    medium) echo 2 ;;
    high) echo 3 ;;
    *) echo 0 ;;
  esac
}

reject_reasons=()
hold_reasons=()

case "${legality}" in
  blocked|illegal|no)
    reject_reasons+=("legality_blocked")
    ;;
  unclear|unknown)
    reject_reasons+=("legality_unclear")
    ;;
esac

case "${consent}" in
  missing|none|no)
    reject_reasons+=("consent_missing")
    ;;
  limited|partial)
    hold_reasons+=("consent_limited")
    ;;
esac

case "${provenance}" in
  scraped|purchased|brokered|leaked)
    reject_reasons+=("provenance_disallowed")
    ;;
  unclear|unknown)
    reject_reasons+=("provenance_unclear")
    ;;
  licensed)
    hold_reasons+=("licensed_data_verify_terms")
    ;;
esac

case "${platform_risk}" in
  high)
    hold_reasons+=("platform_risk_high")
    ;;
esac

impact_score="$(score_value "${impact}")"
effort_score="$(score_value "${effort}")"
durability_score="$(score_value "${durability}")"
leverage_score="$(score_value "${leverage}")"

numeric_score=$(( impact_score + durability_score + leverage_score - effort_score ))

decision="PASS"
summary="controls acceptable"

if (( ${#reject_reasons[@]} > 0 )); then
  decision="REJECT"
  summary="hard gate failed"
elif (( ${#hold_reasons[@]} > 0 )); then
  decision="HOLD"
  summary="needs controls before execution"
elif (( numeric_score < 4 )); then
  decision="HOLD"
  hold_reasons+=("weak_unit_economics_or_leverage")
  summary="commercial score too weak for automatic execution"
fi

echo "decision=${decision}"
echo "summary=${summary}"
echo "score=${numeric_score}"
echo "impact=${impact}"
echo "effort=${effort}"
echo "durability=${durability}"
echo "leverage=${leverage}"
echo "legality=${legality}"
echo "consent=${consent}"
echo "provenance=${provenance}"
echo "platform_risk=${platform_risk}"

if (( ${#reject_reasons[@]} > 0 )); then
  printf 'reject_reasons=%s\n' "$(IFS=,; echo "${reject_reasons[*]}")"
fi

if (( ${#hold_reasons[@]} > 0 )); then
  printf 'hold_reasons=%s\n' "$(IFS=,; echo "${hold_reasons[*]}")"
fi
