import json

from python.helpers.tool import Response, Tool


RISK_WEIGHTS = {"low": 1, "medium": 2, "high": 3}
LIST_BROKER_KEYWORDS = (
    "email list",
    "contact list",
    "lead list",
    "mailing list",
    "data broker",
    "brokerage",
    "resell",
    "resale",
    "rent list",
    "sell contacts",
    "sell emails",
)
UNCONSENTED_OUTREACH_KEYWORDS = (
    "cold email",
    "cold outreach",
    "mass outreach",
    "blast",
    "bulk send",
    "spam",
)


def normalize_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def normalize_risk(value, default: str = "medium") -> str:
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in RISK_WEIGHTS:
            return lowered
    return default


def contains_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)


def summarize_status(status: str) -> str:
    if status == "REJECT":
        return "Rejected. The plan depends on behavior that is not acceptable for autonomous execution."
    if status == "HOLD":
        return "Hold. The plan may be viable, but it needs tighter controls or a safer go-to-market path."
    return "Pass. The plan appears compatible with a lawful, consent-respecting revenue program."


def evaluate_plan(
    objective: str,
    customer_value: str,
    acquisition_model: str,
    monetization_model: str,
    data_source: str,
    owner_authorized,
    has_explicit_consent,
    personal_data_involved,
    value_strength,
    execution_feasibility,
    repeatability,
    legal_risk,
    consent_risk,
    data_provenance_risk,
    platform_risk,
) -> dict:
    owner_authorized = normalize_bool(owner_authorized)
    has_explicit_consent = normalize_bool(has_explicit_consent)
    personal_data_involved = normalize_bool(personal_data_involved)

    value_strength = normalize_risk(value_strength)
    execution_feasibility = normalize_risk(execution_feasibility)
    repeatability = normalize_risk(repeatability)
    legal_risk = normalize_risk(legal_risk)
    consent_risk = normalize_risk(consent_risk)
    data_provenance_risk = normalize_risk(data_provenance_risk)
    platform_risk = normalize_risk(platform_risk)

    combined_text = " ".join(
        [
            objective or "",
            acquisition_model or "",
            monetization_model or "",
            data_source or "",
        ]
    ).strip()

    reasons: list[str] = []
    required_controls: list[str] = []
    next_actions: list[str] = []
    safe_alternatives = [
        "Build a first-party, opt-in newsletter or waitlist.",
        "Sell a productized service or software workflow instead of contact data.",
        "Use owner-authorized mailbox RAG only for internal summaries, support, or operations.",
        "Rely on public, licensed, or anonymized datasets for market research.",
    ]

    status = "PASS"

    if contains_keyword(combined_text, LIST_BROKER_KEYWORDS):
        status = "REJECT"
        reasons.append("The plan appears to involve list brokerage or personal contact-data resale.")

    if legal_risk == "high":
        status = "REJECT"
        reasons.append("Legal risk is too high for autonomous execution.")

    if data_provenance_risk == "high":
        status = "REJECT"
        reasons.append("Data provenance is too weak; use first-party, public, or licensed data instead.")

    if personal_data_involved and not owner_authorized:
        status = "REJECT"
        reasons.append("Personal data is involved without clear owner authorization.")

    if contains_keyword(combined_text, UNCONSENTED_OUTREACH_KEYWORDS) and not has_explicit_consent:
        if status != "REJECT":
            status = "HOLD"
        reasons.append("Outreach model appears non-consensual or insufficiently permissioned.")

    if consent_risk == "high":
        if status != "REJECT":
            status = "HOLD"
        reasons.append("Consent risk is high and should be resolved before execution.")

    if platform_risk == "high":
        if status != "REJECT":
            status = "HOLD"
        reasons.append("Platform dependence is too risky; the venture needs a more durable channel.")

    if not customer_value.strip():
        if status == "PASS":
            status = "HOLD"
        reasons.append("Customer value is underspecified.")

    upside_score = (
        RISK_WEIGHTS[value_strength]
        + RISK_WEIGHTS[execution_feasibility]
        + RISK_WEIGHTS[repeatability]
    )
    risk_score = (
        RISK_WEIGHTS[legal_risk]
        + RISK_WEIGHTS[consent_risk]
        + RISK_WEIGHTS[data_provenance_risk]
        + RISK_WEIGHTS[platform_risk]
    )

    if status == "PASS" and (upside_score < 6 or risk_score > 7):
        status = "HOLD"
        reasons.append("The opportunity needs stronger upside or lower operational risk.")

    if personal_data_involved:
        required_controls.append("Document authorization, retention limits, and data handling boundaries.")
    if not has_explicit_consent:
        required_controls.append("Avoid unsolicited outreach unless a lawful, compliant channel is clearly established.")
    if owner_authorized:
        required_controls.append("Keep private-data outputs inside the authorized environment unless explicitly approved for export.")

    if status == "REJECT":
        next_actions.extend(
            [
                "Replace the business model with a first-party or owner-authorized workflow.",
                "Remove any dependence on personal-data resale, scraping, or non-consensual outreach.",
            ]
        )
    elif status == "HOLD":
        next_actions.extend(
            [
                "Clarify customer value and target buyer.",
                "Reduce platform or consent risk before execution.",
                "Run the shell scoring instrument to compare alternatives.",
            ]
        )
    else:
        next_actions.extend(
            [
                "Add the opportunity to docs/strategy/incoming.md with a score.",
                "Define a tight pilot offer and success metric.",
                "Capture lessons in the financial-system journal after the first run.",
            ]
        )

    return {
        "status": status,
        "summary": summarize_status(status),
        "objective": objective,
        "customer_value": customer_value,
        "acquisition_model": acquisition_model,
        "monetization_model": monetization_model,
        "data_source": data_source,
        "normalized_inputs": {
            "owner_authorized": owner_authorized,
            "has_explicit_consent": has_explicit_consent,
            "personal_data_involved": personal_data_involved,
            "value_strength": value_strength,
            "execution_feasibility": execution_feasibility,
            "repeatability": repeatability,
            "legal_risk": legal_risk,
            "consent_risk": consent_risk,
            "data_provenance_risk": data_provenance_risk,
            "platform_risk": platform_risk,
        },
        "scores": {"upside_score": upside_score, "risk_score": risk_score},
        "reasons": reasons,
        "required_controls": required_controls,
        "next_actions": next_actions,
        "safe_alternatives": safe_alternatives,
    }


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        customer_value: str = "",
        acquisition_model: str = "",
        monetization_model: str = "",
        data_source: str = "",
        owner_authorized=False,
        has_explicit_consent=False,
        personal_data_involved=False,
        value_strength: str = "medium",
        execution_feasibility: str = "medium",
        repeatability: str = "medium",
        legal_risk: str = "medium",
        consent_risk: str = "medium",
        data_provenance_risk: str = "medium",
        platform_risk: str = "medium",
        **kwargs,
    ) -> Response:
        result = evaluate_plan(
            objective=objective,
            customer_value=customer_value,
            acquisition_model=acquisition_model,
            monetization_model=monetization_model,
            data_source=data_source,
            owner_authorized=owner_authorized,
            has_explicit_consent=has_explicit_consent,
            personal_data_involved=personal_data_involved,
            value_strength=value_strength,
            execution_feasibility=execution_feasibility,
            repeatability=repeatability,
            legal_risk=legal_risk,
            consent_risk=consent_risk,
            data_provenance_risk=data_provenance_risk,
            platform_risk=platform_risk,
        )
        return Response(message=json.dumps(result, indent=2), break_loop=False)
