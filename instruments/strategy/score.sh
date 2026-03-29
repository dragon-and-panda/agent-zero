#!/usr/bin/env bash
set -euo pipefail

# Scores a candidate revenue lane on a 0-100 scale with
# legality/consent gates that can force an immediate reject.

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage:
  ./score.sh legality consent repeatability time_to_cash defensibility setup_effort

Inputs:
  legality       0-10
  consent        0-10
  repeatability  0-10
  time_to_cash   0-10
  defensibility  0-10
  setup_effort   0-10  (higher means easier to set up)

Hard gates:
  legality < 8  => REJECT
  consent  < 8  => REJECT
EOF
  exit 0
fi

if [[ "$#" -ne 6 ]]; then
  echo "Expected 6 numeric inputs. Use --help for details." >&2
  exit 1
fi

validate_score() {
  local name="$1"
  local value="$2"

  if ! [[ "$value" =~ ^([0-9]|10)$ ]]; then
    echo "Invalid ${name}: ${value}. Expected integer 0-10." >&2
    exit 1
  fi
}

legality="$1"
consent="$2"
repeatability="$3"
time_to_cash="$4"
defensibility="$5"
setup_effort="$6"

validate_score "legality" "$legality"
validate_score "consent" "$consent"
validate_score "repeatability" "$repeatability"
validate_score "time_to_cash" "$time_to_cash"
validate_score "defensibility" "$defensibility"
validate_score "setup_effort" "$setup_effort"

if (( legality < 8 )); then
  echo "REJECT: legality gate failed (${legality}/10)"
  exit 0
fi

if (( consent < 8 )); then
  echo "REJECT: consent gate failed (${consent}/10)"
  exit 0
fi

total=$(( legality * 25 + consent * 25 + repeatability * 15 + time_to_cash * 15 + defensibility * 10 + setup_effort * 10 ))
score=$(( total / 10 ))

decision="HOLD"
if (( score >= 80 )); then
  decision="GO"
elif (( score < 65 )); then
  decision="REJECT"
fi

printf 'Decision: %s\n' "$decision"
printf 'Score: %s/100\n' "$score"
printf 'Breakdown:\n'
printf '  legality      %s/10\n' "$legality"
printf '  consent       %s/10\n' "$consent"
printf '  repeatability %s/10\n' "$repeatability"
printf '  time_to_cash  %s/10\n' "$time_to_cash"
printf '  defensibility %s/10\n' "$defensibility"
printf '  setup_effort  %s/10\n' "$setup_effort"
