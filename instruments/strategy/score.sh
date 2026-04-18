#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality consent provenance tos time margin repeatability automation defensibility

Inputs:
  legality, consent, provenance, tos, time, margin, repeatability, automation, defensibility
  Each value must be one of: low, medium, high

Output:
  REJECT when any hard gate fails.
  HOLD when hard gates pass but execution quality is not strong enough.
  PASS when hard gates pass and execution quality is strong.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -ne 9 ]]; then
  usage >&2
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
      printf 'invalid'
      ;;
  esac
}

score_value() {
  case "$1" in
    low) printf '1' ;;
    medium) printf '2' ;;
    high) printf '3' ;;
    *) printf '0' ;;
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

for field in "$legality" "$consent" "$provenance" "$tos" "$time" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$field" == "invalid" ]]; then
    echo "Invalid input. All arguments must be low, medium, or high." >&2
    exit 1
  fi
done

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" || "$tos" == "low" ]]; then
  echo "REJECT"
  exit 0
fi

if [[ "$legality" != "high" || "$consent" != "high" || "$provenance" == "medium" || "$tos" == "medium" ]]; then
  echo "HOLD"
  exit 0
fi

for field in "$time" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$field" == "low" ]]; then
    echo "HOLD"
    exit 0
  fi
done

total=0
for field in "$time" "$margin" "$repeatability" "$automation" "$defensibility"; do
  total=$((total + $(score_value "$field")))
done

if (( total >= 12 )); then
  echo "PASS"
else
  echo "HOLD"
fi
