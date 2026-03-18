#!/usr/bin/env bash
set -euo pipefail

name=""
summary=""
time_to_cash=3
repeatability=3
compliance=3
resilience=3
capital=3

usage() {
  echo "Usage: $0 --name NAME --summary TEXT [--time-to-cash 1-5] [--repeatability 1-5] [--compliance 1-5] [--resilience 1-5] [--capital 1-5]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      name="${2:-}"
      shift 2
      ;;
    --summary)
      summary="${2:-}"
      shift 2
      ;;
    --time-to-cash)
      time_to_cash="${2:-}"
      shift 2
      ;;
    --repeatability)
      repeatability="${2:-}"
      shift 2
      ;;
    --compliance)
      compliance="${2:-}"
      shift 2
      ;;
    --resilience)
      resilience="${2:-}"
      shift 2
      ;;
    --capital)
      capital="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$name" || -z "$summary" ]]; then
  usage
  exit 1
fi

for value in "$time_to_cash" "$repeatability" "$compliance" "$resilience" "$capital"; do
  if ! [[ "$value" =~ ^[1-5]$ ]]; then
    echo "Scores must be integers from 1 to 5." >&2
    exit 1
  fi
done

lower_summary="$(printf '%s' "$summary" | tr '[:upper:]' '[:lower:]')"
decision="HOLD"
reason=""

if [[ "$lower_summary" =~ (email\ list|lead\ list|mailing\ list|contact\ list|scraped\ contact|gmail\ export|gmail\ inbox|inbox\ export|bulk\ email) ]]; then
  decision="REJECT"
  reason="Personal contact data resale is prohibited."
elif [[ "$lower_summary" =~ (live\ forex|leveraged\ trading|managed\ account|guaranteed\ return|trading\ signals?|crypto\ signals?|options\ alerts?) ]]; then
  decision="REJECT"
  reason="Live leveraged trading and financial-promotion schemes are out of scope."
fi

weighted_score=$((time_to_cash * 20 + repeatability * 20 + compliance * 20 + resilience * 20 + capital * 20))

if [[ "$decision" != "REJECT" ]]; then
  if [[ "$lower_summary" =~ (paper\ trading|trading\ simulation|simulated\ trading|research\ only) ]]; then
    decision="HOLD"
    reason="Simulation-only trading research is allowed later, but it is not an immediate revenue lane."
  elif (( weighted_score >= 75 )); then
    decision="GO"
    reason="Strong candidate for near-term execution."
  elif (( weighted_score >= 55 )); then
    decision="HOLD"
    reason="Promising, but not strong enough to prioritize yet."
  else
    decision="REJECT"
    reason="Score is too low to justify automation effort."
  fi
fi

printf 'name=%s\n' "$name"
printf 'decision=%s\n' "$decision"
printf 'score=%s\n' "$weighted_score"
printf 'reason=%s\n' "$reason"
