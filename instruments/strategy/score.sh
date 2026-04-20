#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh legality consent provenance tos privacy time margin repeatability automation defensibility

Each input must be one of: high, medium, low

Output:
  RESULT=<PASS|HOLD|REJECT>
  hard_gates=...
  soft_high=...
  soft_low=...
  rationale=...
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -ne 10 ]]; then
  usage >&2
  exit 1
fi

normalize() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    high|medium|low)
      printf '%s' "$value"
      ;;
    *)
      printf 'invalid'
      ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
tos="$(normalize "$4")"
privacy="$(normalize "$5")"
time="$(normalize "$6")"
margin="$(normalize "$7")"
repeatability="$(normalize "$8")"
automation="$(normalize "$9")"
defensibility="$(normalize "${10}")"

for value in "$legality" "$consent" "$provenance" "$tos" "$privacy" "$time" "$margin" "$repeatability" "$automation" "$defensibility"; do
  if [[ "$value" == "invalid" ]]; then
    echo "All inputs must be one of: high, medium, low" >&2
    exit 2
  fi
done

hard_failures=()

[[ "$legality" == "high" ]] || hard_failures+=("legality")
[[ "$consent" == "high" ]] || hard_failures+=("consent")
[[ "$provenance" == "high" ]] || hard_failures+=("provenance")
[[ "$tos" == "high" ]] || hard_failures+=("tos")
[[ "$privacy" == "high" ]] || hard_failures+=("privacy")

soft_values=("$time" "$margin" "$repeatability" "$automation" "$defensibility")
soft_names=("time" "margin" "repeatability" "automation" "defensibility")
soft_high=0
soft_low=0
soft_low_names=()

for idx in "${!soft_values[@]}"; do
  value="${soft_values[$idx]}"
  name="${soft_names[$idx]}"
  if [[ "$value" == "high" ]]; then
    soft_high=$((soft_high + 1))
  fi
  if [[ "$value" == "low" ]]; then
    soft_low=$((soft_low + 1))
    soft_low_names+=("$name")
  fi
done

if (( ${#hard_failures[@]} > 0 )); then
  echo "RESULT=REJECT"
  echo "hard_gates=$(IFS=,; echo "${hard_failures[*]}")"
  echo "soft_high=${soft_high}"
  echo "soft_low=${soft_low}"
  echo "rationale=One or more hard compliance gates failed."
  exit 0
fi

if (( soft_low > 0 )); then
  echo "RESULT=HOLD"
  echo "hard_gates=clear"
  echo "soft_high=${soft_high}"
  echo "soft_low=${soft_low}"
  echo "rationale=Compliant lane, but weak execution factor(s): $(IFS=,; echo "${soft_low_names[*]}")."
  exit 0
fi

if (( soft_high >= 3 )); then
  echo "RESULT=PASS"
  echo "hard_gates=clear"
  echo "soft_high=${soft_high}"
  echo "soft_low=${soft_low}"
  echo "rationale=Compliant lane with at least three strong execution factors."
  exit 0
fi

echo "RESULT=HOLD"
echo "hard_gates=clear"
echo "soft_high=${soft_high}"
echo "soft_low=${soft_low}"
echo "rationale=Compliant lane, but not enough high-confidence execution factors yet."
