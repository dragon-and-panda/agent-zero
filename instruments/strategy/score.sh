#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh --name NAME --legality N --consent N --profit N --automation N \
           --speed N --repeatability N --capital N --platform-risk N \
           --downside N [--notes TEXT]

All ratings are integers from 1 to 5.
EOF
}

require_value() {
  local key="$1"
  local value="$2"

  if [[ -z "$value" ]]; then
    echo "Missing required value for $key" >&2
    exit 1
  fi
}

validate_rating() {
  local key="$1"
  local value="$2"

  if [[ ! "$value" =~ ^[1-5]$ ]]; then
    echo "Invalid rating for $key: $value (expected 1-5)" >&2
    exit 1
  fi
}

name=""
notes=""
legality=""
consent=""
profit=""
automation=""
speed=""
repeatability=""
capital=""
platform_risk=""
downside=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      name="${2:-}"
      shift 2
      ;;
    --notes)
      notes="${2:-}"
      shift 2
      ;;
    --legality)
      legality="${2:-}"
      shift 2
      ;;
    --consent)
      consent="${2:-}"
      shift 2
      ;;
    --profit)
      profit="${2:-}"
      shift 2
      ;;
    --automation)
      automation="${2:-}"
      shift 2
      ;;
    --speed)
      speed="${2:-}"
      shift 2
      ;;
    --repeatability)
      repeatability="${2:-}"
      shift 2
      ;;
    --capital)
      capital="${2:-}"
      shift 2
      ;;
    --platform-risk)
      platform_risk="${2:-}"
      shift 2
      ;;
    --downside)
      downside="${2:-}"
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

require_value "--name" "$name"
require_value "--legality" "$legality"
require_value "--consent" "$consent"
require_value "--profit" "$profit"
require_value "--automation" "$automation"
require_value "--speed" "$speed"
require_value "--repeatability" "$repeatability"
require_value "--capital" "$capital"
require_value "--platform-risk" "$platform_risk"
require_value "--downside" "$downside"

validate_rating "--legality" "$legality"
validate_rating "--consent" "$consent"
validate_rating "--profit" "$profit"
validate_rating "--automation" "$automation"
validate_rating "--speed" "$speed"
validate_rating "--repeatability" "$repeatability"
validate_rating "--capital" "$capital"
validate_rating "--platform-risk" "$platform_risk"
validate_rating "--downside" "$downside"

notes_lc="$(printf '%s' "$notes" | tr '[:upper:]' '[:lower:]')"

decision=""
reason=""

if [[ "$legality" -lt 4 || "$consent" -lt 4 ]]; then
  decision="REJECT"
  reason="Legality and consent must both score at least 4."
fi

if [[ -z "$decision" && "$notes_lc" =~ (email[[:space:]-]?list|sell[[:space:]]+contacts|spam|phishing|scrape[[:space:]]+inbox|bcc|cc[[:space:]]+harvest|credential|bypass[[:space:]]+captcha) ]]; then
  decision="REJECT"
  reason="Notes match prohibited acquisition or abuse patterns."
fi

if [[ -z "$decision" && "$notes_lc" =~ (forex|options|leveraged|prop[[:space:]-]?trading|day[[:space:]-]?trading) ]]; then
  decision="HOLD"
  reason="Trading ideas require a separate risk-review gate and paper trading first."
fi

weighted_sum=$(( \
  legality * 20 + \
  consent * 20 + \
  profit * 15 + \
  automation * 10 + \
  speed * 10 + \
  repeatability * 10 + \
  (6 - capital) * 5 + \
  (6 - platform_risk) * 5 + \
  (6 - downside) * 5 \
))
score=$(( weighted_sum / 5 ))

if [[ -z "$decision" ]]; then
  if [[ "$score" -ge 75 ]]; then
    decision="GO"
    reason="Score meets launch threshold."
  elif [[ "$score" -ge 60 ]]; then
    decision="HOLD"
    reason="Promising, but missing enough strength for immediate launch."
  else
    decision="REJECT"
    reason="Score is too low for a resilient opportunity."
  fi
fi

echo "Opportunity: $name"
echo "Decision: $decision"
echo "Score: ${score}/100"
echo "Reason: $reason"
echo "Ratings:"
echo "  legality=$legality"
echo "  consent=$consent"
echo "  profit=$profit"
echo "  automation=$automation"
echo "  speed=$speed"
echo "  repeatability=$repeatability"
echo "  capital=$capital"
echo "  platform_risk=$platform_risk"
echo "  downside=$downside"

if [[ -n "$notes" ]]; then
  echo "Notes: $notes"
fi
