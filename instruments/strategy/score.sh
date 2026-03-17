#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./instruments/strategy/score.sh \
    --name "Opportunity Name" \
    --legal 1-5 \
    --consent 1-5 \
    --automation 1-5 \
    --margin 1-5 \
    --time-to-cash 1-5 \
    --repeatability 1-5 \
    --resilience 1-5 \
    --platform-dependency 1-5 \
    --capital-intensity 1-5 \
    --regulatory-exposure 1-5

Higher is better for:
  legal, consent, automation, margin, time-to-cash, repeatability, resilience

Higher is worse for:
  platform-dependency, capital-intensity, regulatory-exposure
EOF
}

require_value() {
  local key="$1"
  local value="$2"
  if [[ -z "${value}" ]]; then
    echo "Missing value for ${key}" >&2
    exit 1
  fi
}

require_score() {
  local key="$1"
  local value="$2"

  if ! [[ "${value}" =~ ^[1-5]$ ]]; then
    echo "Invalid score for ${key}: ${value}. Expected an integer from 1 to 5." >&2
    exit 1
  fi
}

name=""
legal=""
consent=""
automation=""
margin=""
time_to_cash=""
repeatability=""
resilience=""
platform_dependency=""
capital_intensity=""
regulatory_exposure=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      require_value "$1" "${2:-}"
      name="$2"
      shift 2
      ;;
    --legal)
      require_value "$1" "${2:-}"
      legal="$2"
      shift 2
      ;;
    --consent)
      require_value "$1" "${2:-}"
      consent="$2"
      shift 2
      ;;
    --automation)
      require_value "$1" "${2:-}"
      automation="$2"
      shift 2
      ;;
    --margin)
      require_value "$1" "${2:-}"
      margin="$2"
      shift 2
      ;;
    --time-to-cash)
      require_value "$1" "${2:-}"
      time_to_cash="$2"
      shift 2
      ;;
    --repeatability)
      require_value "$1" "${2:-}"
      repeatability="$2"
      shift 2
      ;;
    --resilience)
      require_value "$1" "${2:-}"
      resilience="$2"
      shift 2
      ;;
    --platform-dependency)
      require_value "$1" "${2:-}"
      platform_dependency="$2"
      shift 2
      ;;
    --capital-intensity)
      require_value "$1" "${2:-}"
      capital_intensity="$2"
      shift 2
      ;;
    --regulatory-exposure)
      require_value "$1" "${2:-}"
      regulatory_exposure="$2"
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

for field in \
  name \
  legal \
  consent \
  automation \
  margin \
  time_to_cash \
  repeatability \
  resilience \
  platform_dependency \
  capital_intensity \
  regulatory_exposure; do
  value="${!field}"
  if [[ -z "${value}" ]]; then
    echo "Missing required field: ${field}" >&2
    usage >&2
    exit 1
  fi
done

for scored_field in \
  legal \
  consent \
  automation \
  margin \
  time_to_cash \
  repeatability \
  resilience \
  platform_dependency \
  capital_intensity \
  regulatory_exposure; do
  require_score "${scored_field}" "${!scored_field}"
done

quality=$((legal * 25 \
  + consent * 20 \
  + automation * 10 \
  + margin * 15 \
  + time_to_cash * 10 \
  + repeatability * 10 \
  + resilience * 10))

risk_penalty=$((platform_dependency * 5 \
  + capital_intensity * 5 \
  + regulatory_exposure * 10))

score=$(((quality - risk_penalty) / 5))

if (( score >= 80 )); then
  band="STRONG"
  guidance="Proceed with launch planning and define the first deliverable."
elif (( score >= 65 )); then
  band="PROMISING"
  guidance="Proceed only after de-risking the weakest inputs."
elif (( score >= 50 )); then
  band="SANDBOX"
  guidance="Keep this in validation mode; do not rely on it as the primary revenue engine yet."
else
  band="REJECT_OR_REDESIGN"
  guidance="Reject or redesign before further effort."
fi

gate="PASS"
gate_note="Legal and consent posture meet the minimum promotion threshold."
if (( legal < 4 || consent < 4 )); then
  gate="FAIL"
  gate_note="Do not promote this opportunity: legal or consent score is below 4."
fi

lowest_metric_name=""
lowest_metric_value=6
for scored_field in legal consent automation margin time_to_cash repeatability resilience; do
  value="${!scored_field}"
  if (( value < lowest_metric_value )); then
    lowest_metric_name="${scored_field}"
    lowest_metric_value="${value}"
  fi
done

highest_risk_name=""
highest_risk_value=0
for risk_field in platform_dependency capital_intensity regulatory_exposure; do
  value="${!risk_field}"
  if (( value > highest_risk_value )); then
    highest_risk_name="${risk_field}"
    highest_risk_value="${value}"
  fi
done

printf 'Opportunity: %s\n' "${name}"
printf 'Score: %s/100\n' "${score}"
printf 'Band: %s\n' "${band}"
printf 'Gate: %s\n' "${gate}"
printf 'Guidance: %s\n' "${guidance}"
printf 'Promotion rule: %s\n' "${gate_note}"
printf 'Weakest positive metric: %s (%s/5)\n' "${lowest_metric_name}" "${lowest_metric_value}"
printf 'Largest risk factor: %s (%s/5)\n' "${highest_risk_name}" "${highest_risk_value}"
