#!/bin/bash

set -euo pipefail

if [ "${1-}" = "" ]; then
  echo "Usage: bash opportunity_score.sh <path-to-json>"
  exit 1
fi

INPUT_PATH="$1"

python3 - "$INPUT_PATH" <<'PY'
import json
import os
import sys


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def as_float(data, key, default=0.0):
    value = data.get(key, default)
    try:
        return clamp(float(value))
    except (TypeError, ValueError):
        return clamp(float(default))


def as_bool(data, key, default=False):
    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def normalize_channel(channel: str) -> str:
    return channel.strip().lower().replace("-", "_").replace(" ", "_")


path = sys.argv[1]
if not os.path.exists(path):
    print(json.dumps({"error": f"Input file not found: {path}"}, indent=2))
    sys.exit(1)

with open(path, "r", encoding="utf-8") as handle:
    data = json.load(handle)

name = data.get("name", "Unnamed opportunity")
consent_model = str(data.get("consent_model", "unknown")).strip().lower()
channels = [normalize_channel(item) for item in data.get("acquisition_channels", [])]
requires_personal_data = as_bool(data, "requires_personal_data", False)

fulfillment_automation = as_float(data, "fulfillment_automation", 0.0)
margin_profile = as_float(data, "margin_profile", 0.0)
time_to_revenue = as_float(data, "time_to_revenue", 0.0)
defensibility = as_float(data, "defensibility", 0.0)
legal_risk = as_float(data, "legal_risk", 1.0)

consent_scores = {
    "explicit_opt_in": 1.0,
    "first_party_customer": 0.95,
    "existing_customer": 0.85,
    "transactional_only": 0.7,
    "public_business_contact": 0.65,
    "unclear": 0.25,
    "none": 0.0,
    "unknown": 0.1,
}
consent_score = consent_scores.get(consent_model, 0.1)

good_channels = {
    "seo",
    "content",
    "affiliate",
    "referrals",
    "marketplaces",
    "opt_in_email",
    "newsletter",
    "community",
    "inbound_demo",
    "repeat_customers",
    "partnerships",
}
bad_channels = {
    "bought_email_lists",
    "sold_email_lists",
    "scraped_emails",
    "harvested_emails",
    "inbox_harvest",
    "cold_spam",
    "bot_evasion",
    "identity_spoofing",
}

channel_points = []
for channel in channels:
    if channel in good_channels:
        channel_points.append(1.0)
    elif channel in bad_channels:
        channel_points.append(0.0)
    else:
        channel_points.append(0.5)
channel_quality = sum(channel_points) / len(channel_points) if channel_points else 0.5

legal_safety = 1.0 - legal_risk

blockers = []
warnings = []

if any(channel in bad_channels for channel in channels):
    blockers.append("Uses a prohibited acquisition channel.")

if requires_personal_data and consent_score < 0.8:
    blockers.append("Depends on personal data without strong consent.")

if consent_model in {"none", "unknown", "unclear"}:
    warnings.append("Consent basis is weak or undefined.")

if legal_risk >= 0.7:
    blockers.append("Legal risk is too high.")
elif legal_risk >= 0.4:
    warnings.append("Legal risk needs review before launch.")

if margin_profile < 0.4:
    warnings.append("Margin profile may be too thin for automation overhead.")

if fulfillment_automation < 0.4:
    warnings.append("Low automation potential; may stay labor-heavy.")

if time_to_revenue < 0.4:
    warnings.append("Slow path to first revenue.")

score = (
    consent_score * 0.25
    + legal_safety * 0.20
    + margin_profile * 0.15
    + fulfillment_automation * 0.15
    + time_to_revenue * 0.10
    + defensibility * 0.10
    + channel_quality * 0.05
)
score = round(score * 100, 1)

if blockers:
    recommendation = "NO_GO"
elif score >= 75:
    recommendation = "GO"
elif score >= 55:
    recommendation = "INVESTIGATE"
else:
    recommendation = "NO_GO"

result = {
    "name": name,
    "score": score,
    "recommendation": recommendation,
    "subscores": {
        "consent_score": round(consent_score, 3),
        "legal_safety": round(legal_safety, 3),
        "margin_profile": round(margin_profile, 3),
        "fulfillment_automation": round(fulfillment_automation, 3),
        "time_to_revenue": round(time_to_revenue, 3),
        "defensibility": round(defensibility, 3),
        "channel_quality": round(channel_quality, 3),
    },
    "blockers": blockers,
    "warnings": warnings,
    "notes": data.get("notes", ""),
}

print(json.dumps(result, indent=2))
PY
