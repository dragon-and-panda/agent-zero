#!/bin/bash

set -euo pipefail

lane=""
legality=""
consent=""
data_source=""
tos=""
automation=3
time_to_cash=3
margin=3
retention=3
complexity=3
notes=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --lane)
            lane="${2:-}"
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
        --data)
            data_source="${2:-}"
            shift 2
            ;;
        --tos)
            tos="${2:-}"
            shift 2
            ;;
        --automation)
            automation="${2:-}"
            shift 2
            ;;
        --time-to-cash)
            time_to_cash="${2:-}"
            shift 2
            ;;
        --margin)
            margin="${2:-}"
            shift 2
            ;;
        --retention)
            retention="${2:-}"
            shift 2
            ;;
        --complexity)
            complexity="${2:-}"
            shift 2
            ;;
        --notes)
            notes="${2:-}"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

python3 - "$lane" "$legality" "$consent" "$data_source" "$tos" \
    "$automation" "$time_to_cash" "$margin" "$retention" "$complexity" \
    "$notes" <<'PY'
import json
import sys

lane, legality, consent, data_source, tos, automation, time_to_cash, margin, retention, complexity, notes = sys.argv[1:]

if not lane:
    raise SystemExit("Missing required argument: --lane")

required = {
    "--legality": legality,
    "--consent": consent,
    "--data": data_source,
    "--tos": tos,
}
for flag, value in required.items():
    if not value:
        raise SystemExit(f"Missing required argument: {flag}")

def to_score(name: str, raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise SystemExit(f"{name} must be an integer from 1 to 5") from exc
    if value < 1 or value > 5:
        raise SystemExit(f"{name} must be an integer from 1 to 5")
    return value

automation = to_score("automation", automation)
time_to_cash = to_score("time_to_cash", time_to_cash)
margin = to_score("margin", margin)
retention = to_score("retention", retention)
complexity = to_score("complexity", complexity)

notes_lower = notes.lower()
blocked_keywords = [
    "sell email list",
    "selling email list",
    "email lists",
    "broker email",
    "contact brokerage",
    "gmail scrape",
    "scrape inbox",
    "harvest emails",
    "harvesting emails",
    "cold email database",
    "lead list resale",
]

reasons = []

if legality != "strong":
    reasons.append("Lawfulness is not strong.")

if consent not in {"explicit", "owner_only", "public_business"}:
    reasons.append("Consent or authority is insufficient.")

if data_source not in {
    "first_party",
    "client_authorized",
    "opt_in",
    "public_business",
    "licensed",
}:
    reasons.append("Data provenance is not compliant.")

if tos != "compliant":
    reasons.append("Platform terms are unclear or violating.")

for phrase in blocked_keywords:
    if phrase in notes_lower or phrase in lane.lower():
        reasons.append(f"Blocked keyword detected: '{phrase}'.")
        break

score = (
    automation * 25
    + time_to_cash * 20
    + margin * 20
    + retention * 20
    + (6 - complexity) * 15
) / 5

verdict = "PASS" if not reasons else "REJECT"

result = {
    "lane": lane,
    "verdict": verdict,
    "normalized_score": round(score, 1),
    "inputs": {
        "legality": legality,
        "consent": consent,
        "data_source": data_source,
        "tos": tos,
        "automation": automation,
        "time_to_cash": time_to_cash,
        "margin": margin,
        "retention": retention,
        "complexity": complexity,
        "notes": notes,
    },
    "reasons": reasons,
    "next_step": (
        "Promote to scoped experiment and log the result in the mission journal."
        if verdict == "PASS"
        else "Do not activate. Re-scope the lane to use compliant data and an allowed monetization model."
    ),
}

print(json.dumps(result, indent=2))
PY
