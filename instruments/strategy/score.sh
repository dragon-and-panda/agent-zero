#!/bin/bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash score.sh \
    --name "Opportunity Name" \
    --revenue 0-10 \
    --speed 0-10 \
    --automation 0-10 \
    --resilience 0-10 \
    --trust 0-10 \
    --capital 0-10 \
    --legal 0-10 \
    --platform 0-10 \
    [--notes "optional description"]

Scoring rules:
  - Higher is better for every field except --platform.
  - --platform means platform dependency; lower is better.
  - Any idea that depends on personal-data resale, spam, or inbox scraping
    for resale is automatically rejected.
EOF
}

require_value() {
  local key="$1"
  local value="$2"

  if [[ -z "$value" ]]; then
    echo "Missing value for $key" >&2
    exit 1
  fi
}

validate_score() {
  local key="$1"
  local value="$2"

  if ! [[ "$value" =~ ^([0-9]|10)$ ]]; then
    echo "Invalid value for $key: '$value' (expected integer 0-10)" >&2
    exit 1
  fi
}

name=""
notes=""
revenue=""
speed=""
automation=""
resilience=""
trust=""
capital=""
legal=""
platform=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      require_value "$1" "${2:-}"
      name="$2"
      shift 2
      ;;
    --notes)
      require_value "$1" "${2:-}"
      notes="$2"
      shift 2
      ;;
    --revenue)
      require_value "$1" "${2:-}"
      revenue="$2"
      shift 2
      ;;
    --speed)
      require_value "$1" "${2:-}"
      speed="$2"
      shift 2
      ;;
    --automation)
      require_value "$1" "${2:-}"
      automation="$2"
      shift 2
      ;;
    --resilience)
      require_value "$1" "${2:-}"
      resilience="$2"
      shift 2
      ;;
    --trust)
      require_value "$1" "${2:-}"
      trust="$2"
      shift 2
      ;;
    --capital)
      require_value "$1" "${2:-}"
      capital="$2"
      shift 2
      ;;
    --legal)
      require_value "$1" "${2:-}"
      legal="$2"
      shift 2
      ;;
    --platform)
      require_value "$1" "${2:-}"
      platform="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

for pair in \
  "name:$name" \
  "revenue:$revenue" \
  "speed:$speed" \
  "automation:$automation" \
  "resilience:$resilience" \
  "trust:$trust" \
  "capital:$capital" \
  "legal:$legal" \
  "platform:$platform"; do
  key="${pair%%:*}"
  value="${pair#*:}"
  require_value "$key" "$value"
done

for pair in \
  "revenue:$revenue" \
  "speed:$speed" \
  "automation:$automation" \
  "resilience:$resilience" \
  "trust:$trust" \
  "capital:$capital" \
  "legal:$legal" \
  "platform:$platform"; do
  key="${pair%%:*}"
  value="${pair#*:}"
  validate_score "$key" "$value"
done

combined_text="${name} ${notes}"
combined_text="${combined_text,,}"

blocked=0
blocked_reason=""

for banned in \
  "sell email" \
  "email list" \
  "contact list" \
  "mailbox resale" \
  "resell contacts" \
  "scraped emails" \
  "spam campaign" \
  "cold email blast"; do
  if [[ "$combined_text" == *"$banned"* ]]; then
    blocked=1
    blocked_reason="Detected banned pattern: $banned"
    break
  fi
done

score=$(
  awk \
    -v revenue="$revenue" \
    -v speed="$speed" \
    -v automation="$automation" \
    -v resilience="$resilience" \
    -v trust="$trust" \
    -v capital="$capital" \
    -v legal="$legal" \
    -v platform="$platform" \
    'BEGIN {
      weighted = ((revenue * 2.00) + (speed * 1.50) + (automation * 1.50) + (resilience * 1.25) + (trust * 1.25) + (capital * 1.00) + (legal * 2.50) + ((10 - platform) * 1.00));
      normalized = (weighted / 120.0) * 100.0;
      printf "%.1f", normalized;
    }'
)

recommendation="GO"
reason="Strong balance of revenue, speed, automation, and legal safety."

if [[ "$blocked" -eq 1 ]]; then
  recommendation="REJECT"
  reason="$blocked_reason"
elif (( legal < 6 )); then
  recommendation="REJECT"
  reason="Legal safety is below minimum threshold."
elif awk "BEGIN { exit !($score < 60.0) }"; then
  recommendation="REJECT"
  reason="Composite score is below execution threshold."
elif (( legal < 8 )) || awk "BEGIN { exit !($score < 75.0) }"; then
  recommendation="HOLD"
  reason="Needs more validation or risk reduction before execution."
fi

cat <<EOF
Opportunity: $name
Composite Score: $score / 100
Recommendation: $recommendation
Reason: $reason

Inputs
  revenue: $revenue
  speed: $speed
  automation: $automation
  resilience: $resilience
  trust: $trust
  capital_efficiency: $capital
  legal_safety: $legal
  platform_dependency: $platform
EOF

if [[ -n "$notes" ]]; then
  printf 'Notes: %s\n' "$notes"
fi
