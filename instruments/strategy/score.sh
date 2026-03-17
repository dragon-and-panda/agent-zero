#!/bin/bash

set -euo pipefail

name=""
speed=""
margin=""
repeatability=""
automation=""
compliance=""
capital_efficiency=""
risk=""
complexity=""
concentration=""

usage() {
  echo "Usage: bash score.sh --name <name> --speed 1-5 --margin 1-5 --repeatability 1-5 --automation 1-5 --compliance 1-5 --capital-efficiency 1-5 --risk 1-5 --complexity 1-5 --concentration 1-5" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      name="${2:-}"
      shift 2
      ;;
    --speed)
      speed="${2:-}"
      shift 2
      ;;
    --margin)
      margin="${2:-}"
      shift 2
      ;;
    --repeatability)
      repeatability="${2:-}"
      shift 2
      ;;
    --automation)
      automation="${2:-}"
      shift 2
      ;;
    --compliance)
      compliance="${2:-}"
      shift 2
      ;;
    --capital-efficiency)
      capital_efficiency="${2:-}"
      shift 2
      ;;
    --risk)
      risk="${2:-}"
      shift 2
      ;;
    --complexity)
      complexity="${2:-}"
      shift 2
      ;;
    --concentration)
      concentration="${2:-}"
      shift 2
      ;;
    --help|-h)
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

for required in name speed margin repeatability automation compliance capital_efficiency risk complexity concentration; do
  if [[ -z "${!required}" ]]; then
    echo "Missing required argument: ${required}" >&2
    usage
    exit 1
  fi
done

python3 - "$name" "$speed" "$margin" "$repeatability" "$automation" "$compliance" "$capital_efficiency" "$risk" "$complexity" "$concentration" <<'PY'
import json
import sys

(
    name,
    speed,
    margin,
    repeatability,
    automation,
    compliance,
    capital_efficiency,
    risk,
    complexity,
    concentration,
) = sys.argv[1:]

fields = {
    "speed": int(speed),
    "margin": int(margin),
    "repeatability": int(repeatability),
    "automation": int(automation),
    "compliance": int(compliance),
    "capital_efficiency": int(capital_efficiency),
    "risk": int(risk),
    "complexity": int(complexity),
    "concentration": int(concentration),
}

for field_name, value in fields.items():
    if value < 1 or value > 5:
        raise SystemExit(f"{field_name} must be between 1 and 5")

benefit_weights = {
    "speed": 0.20,
    "margin": 0.15,
    "repeatability": 0.20,
    "automation": 0.15,
    "compliance": 0.20,
    "capital_efficiency": 0.10,
}

penalty_weights = {
    "risk": 0.45,
    "complexity": 0.30,
    "concentration": 0.25,
}

def normalize(value: int) -> float:
    return ((value - 1) / 4) * 100

benefit_score = sum(normalize(fields[key]) * weight for key, weight in benefit_weights.items())
penalty_score = sum(normalize(fields[key]) * weight for key, weight in penalty_weights.items())
overall_score = round((benefit_score * 0.80) + ((100 - penalty_score) * 0.20), 1)

notes = []
gated = False

if fields["compliance"] <= 2:
    gated = True
    notes.append("Rejected by compliance gate: legal/privacy safety is too weak.")
if fields["risk"] >= 5:
    gated = True
    notes.append("Rejected by risk gate: downside is too high for autonomous launch.")
if fields["concentration"] >= 5:
    notes.append("Severe concentration risk: add a backup channel before launch.")
if fields["automation"] <= 2:
    notes.append("Automation leverage is low: simplify delivery before scaling.")
if fields["speed"] <= 2:
    notes.append("Time to first dollar is slow: consider a faster cash-flow offer.")

if gated:
    recommendation = "reject"
elif overall_score >= 80:
    recommendation = "launch_candidate"
elif overall_score >= 65:
    recommendation = "improve_then_launch"
elif overall_score >= 50:
    recommendation = "hold_for_redesign"
else:
    recommendation = "reject"

output = {
    "opportunity": name,
    "inputs": fields,
    "benefit_score": round(benefit_score, 1),
    "penalty_score": round(penalty_score, 1),
    "overall_score": overall_score,
    "recommendation": recommendation,
    "gated": gated,
    "notes": notes,
}

print(json.dumps(output, indent=2, sort_keys=True))
PY
