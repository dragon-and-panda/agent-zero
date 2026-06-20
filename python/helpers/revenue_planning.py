from __future__ import annotations

import re


RISK_LEVELS = {"low", "medium", "high"}
KNOWN_CONSENT = {"explicit", "contractual", "internal", "unknown", "none"}
KNOWN_PROVENANCE = {
    "first_party",
    "licensed",
    "opt_in",
    "public",
    "scraped",
    "purchased",
    "unknown",
}
PERSONAL_DATA_TERMS = (
    "email",
    "gmail",
    "inbox",
    "contact",
    "crm",
    "lead",
    "newsletter",
    "mailing list",
)
NEGATION_PREFIXES = (
    "no ",
    "not ",
    "without ",
    "avoid ",
    "avoiding ",
    "never ",
    "do not ",
    "don't ",
)
PROHIBITED_SIGNALS = (
    "sell email",
    "sell emails",
    "sell email list",
    "sell contact list",
    "sell the list",
    "sell lists",
    "broker email",
    "broker contacts",
    "rent list",
    "resell contacts",
    "resell email",
    "harvest email",
    "harvest contacts",
    "scrape gmail",
    "scrape inbox",
    "cold email blast",
    "unsolicited outreach",
    "buy leads",
)
BROKERAGE_TERMS = ("sell", "resell", "broker", "rent")
LIST_TERMS = ("email", "emails", "address", "addresses", "contact", "contacts", "list")


def normalize_level(value: str, default: str = "medium") -> str:
    cleaned = (value or default).strip().lower()
    return cleaned if cleaned in RISK_LEVELS else default


def normalize_value(value: str, allowed: set[str], default: str) -> str:
    cleaned = (
        (value or default).strip().lower().replace("-", "_").replace(" ", "_")
    )
    return cleaned if cleaned in allowed else default


def contains_signal(text: str, signals: tuple[str, ...]) -> bool:
    lowered = text.lower()
    for signal in signals:
        pattern = re.compile(rf"(?<!\\w){re.escape(signal)}(?!\\w)")
        for match in pattern.finditer(lowered):
            prefix_window = lowered[max(0, match.start() - 24) : match.start()]
            clause = prefix_window
            for delimiter in (".", ";", ":", "\n"):
                clause = clause.rsplit(delimiter, 1)[-1]
            clause = clause.strip()
            if not any(clause.startswith(prefix.strip()) for prefix in NEGATION_PREFIXES):
                return True
    return False


def implies_contact_list_resale(text: str) -> bool:
    lowered = text.lower()
    return contains_signal(lowered, BROKERAGE_TERMS) and any(
        term in lowered for term in LIST_TERMS
    )


def infer_personal_data_scope(*parts: str) -> bool:
    lowered = " ".join(parts).lower()
    return any(term in lowered for term in PERSONAL_DATA_TERMS)


def recommended_lanes(personal_data_scope: bool) -> list[str]:
    if personal_data_scope:
        return [
            "first-party CRM hygiene and segmentation",
            "owner-authorized inbox summarization for support or operations",
            "opt-in newsletter operations with documented consent",
            "anonymized analytics built from aggregated first-party data",
        ]
    return [
        "productized research or analytics service",
        "seller-authorized marketplace automation",
        "subscription software or internal copilot",
        "opt-in audience product or premium content",
    ]


def build_revenue_plan(
    objective: str,
    revenue_model: str = "",
    data_source: str = "",
    owner_authorized: bool = False,
    consent_status: str = "unknown",
    data_provenance: str = "unknown",
    platform_risk: str = "medium",
    notes: str = "",
) -> dict:
    consent = normalize_value(consent_status, KNOWN_CONSENT, "unknown")
    provenance = normalize_value(data_provenance, KNOWN_PROVENANCE, "unknown")
    platform = normalize_level(platform_risk)
    combined = " | ".join([objective, revenue_model, data_source, notes]).strip()
    personal_data_scope = infer_personal_data_scope(
        objective, revenue_model, data_source, notes
    )

    reasons: list[str] = []
    required_controls: list[str] = []
    safer_alternatives = recommended_lanes(personal_data_scope)
    verdict = "PASS"

    if contains_signal(combined, PROHIBITED_SIGNALS) or implies_contact_list_resale(
        combined
    ):
        verdict = "REJECT"
        reasons.append(
            "The request centers on list brokerage, inbox scraping, or unsolicited outreach."
        )

    if personal_data_scope and not owner_authorized:
        verdict = "REJECT"
        reasons.append("Personal-data workflows require explicit owner authorization.")

    if provenance in {"scraped", "purchased"}:
        verdict = "REJECT"
        reasons.append(
            "Scraped or purchased contact data has unacceptable provenance risk."
        )

    if provenance == "unknown":
        required_controls.append("Document data provenance before execution.")
        if verdict != "REJECT":
            verdict = "HOLD"

    if consent == "none":
        verdict = "REJECT"
        reasons.append("The workflow lacks required consent for the intended use.")
    elif consent == "unknown":
        required_controls.append("Verify and document consent status.")
        if personal_data_scope and verdict != "REJECT":
            verdict = "HOLD"

    if platform == "high":
        verdict = "REJECT"
        reasons.append("Platform risk is too high for autonomous execution.")
    elif platform == "medium" and verdict == "PASS":
        verdict = "HOLD"
        required_controls.append("Review target platform terms and anti-abuse rules.")

    if verdict == "PASS":
        next_steps = [
            "Define a narrow first release and success metric.",
            "Log the opportunity in docs/strategy/incoming.md.",
            "Record operating constraints in docs/policies/compliance_pack.md.",
        ]
        summary = "Opportunity is viable within the current compliance gates."
    elif verdict == "HOLD":
        next_steps = [
            "Resolve the required controls before execution.",
            "Prefer first-party, opt-in, or anonymized variants of the idea.",
            "Re-run planning after provenance, consent, and platform checks are documented.",
        ]
        summary = "Opportunity may be viable, but required controls are still missing."
    else:
        next_steps = [
            "Do not execute the requested workflow.",
            "Redirect to a safer revenue model from the recommended alternatives.",
            "Capture the rejected pattern so it stays blocked in future plans.",
        ]
        summary = "Opportunity should not be executed in its current form."

    return {
        "verdict": verdict,
        "summary": summary,
        "objective": objective,
        "revenue_model": revenue_model,
        "data_source": data_source,
        "personal_data_scope": personal_data_scope,
        "owner_authorized": owner_authorized,
        "consent_status": consent,
        "data_provenance": provenance,
        "platform_risk": platform,
        "reasons": reasons,
        "required_controls": required_controls,
        "recommended_alternatives": safer_alternatives,
        "next_steps": next_steps,
    }
