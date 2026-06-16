#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage:
  score.sh "lane=<name>" "legality=high|medium|low" "consent=high|medium|low" \
           "provenance=high|medium|low" "tos=high|medium|low" \
           "time=high|medium|low" "margin=high|medium|low" \
           "repeatability=high|medium|low" "automation=high|medium|low" \
           "defensibility=high|medium|low" ["notes=<freeform>"]

Outputs:
  STATUS: PASS | HOLD | REJECT
  along with a short reason and normalized score details.
EOF
  exit 0
fi

declare -A args=()
for arg in "$@"; do
  key="${arg%%=*}"
  value="${arg#*=}"
  args["$key"]="$value"
done

required=(
  lane legality consent provenance tos
  time margin repeatability automation defensibility
)

for key in "${required[@]}"; do
  if [[ -z "${args[$key]:-}" ]]; then
    echo "ERROR: missing required argument '$key'" >&2
    exit 2
  fi
done

score_value() {
  case "$1" in
    high) echo 2 ;;
    medium) echo 1 ;;
    low) echo 0 ;;
    *)
      echo "ERROR"
      return 1
      ;;
  esac
}

is_low() {
  [[ "$1" == "low" ]]
}

is_high() {
  [[ "$1" == "high" ]]
}

for key in legality consent provenance tos time margin repeatability automation defensibility; do
  if ! score_value "${args[$key]}" >/dev/null 2>&1; then
    echo "ERROR: '$key' must be one of high, medium, low" >&2
    exit 2
  fi
done

hard_keys=(legality consent provenance tos)
soft_keys=(time margin repeatability automation defensibility)

hard_score=0
soft_score=0
soft_high_count=0
soft_low_keys=()
hard_low_keys=()

for key in "${hard_keys[@]}"; do
  value="${args[$key]}"
  hard_score=$((hard_score + $(score_value "$value")))
  if is_low "$value"; then
    hard_low_keys+=("$key")
  fi
done

for key in "${soft_keys[@]}"; do
  value="${args[$key]}"
  soft_score=$((soft_score + $(score_value "$value")))
  if is_low "$value"; then
    soft_low_keys+=("$key")
  fi
  if is_high "$value"; then
    soft_high_count=$((soft_high_count + 1))
  fi
done

status="HOLD"
reason="compliant but not yet attractive enough for autonomous activation"

if [[ "${#hard_low_keys[@]}" -gt 0 ]]; then
  status="REJECT"
  reason="hard gate failed: ${hard_low_keys[*]}"
elif [[ "${#soft_low_keys[@]}" -gt 0 ]]; then
  status="HOLD"
  reason="soft execution weakness: ${soft_low_keys[*]}"
elif [[ "$soft_high_count" -lt 3 ]]; then
  status="HOLD"
  reason="needs at least three strong execution factors"
elif [[ "$hard_score" -eq 8 && "$soft_score" -ge 8 ]]; then
  status="PASS"
  reason="all hard gates clear and execution profile is attractive"
else
  status="HOLD"
  reason="compliant lane needs stronger execution profile"
fi

echo "LANE: ${args[lane]}"
echo "STATUS: $status"
echo "REASON: $reason"
echo "HARD_SCORE: $hard_score/8"
echo "SOFT_SCORE: $soft_score/10"
echo "SOFT_HIGH_COUNT: $soft_high_count/5"
if [[ -n "${args[notes]:-}" ]]; then
  echo "NOTES: ${args[notes]}"
fi
