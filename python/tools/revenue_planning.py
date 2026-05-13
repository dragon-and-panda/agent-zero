import json
from typing import Any

from python.helpers.dirty_json import DirtyJson
from python.helpers.tool import Response, Tool

LOW = "low"
MEDIUM = "medium"
HIGH = "high"

HARD_FACTORS = ("legality", "consent", "provenance", "platform_risk")
SOFT_FACTORS = ("time", "margin", "repeatability", "automation", "defensibility")

UNSAFE_DATA_PATTERNS = (
    "sell email list",
    "sell email lists",
    "email list brokerage",
    "broker email list",
    "broker contact list",
    "resell contacts",
    "resell emails",
    "sell leads from gmail",
    "harvest email",
    "harvest emails",
    "scrape gmail",
    "scrape inbox",
    "gmail extraction for resale",
    "contact list sale",
    "personal data resale",
)

UNSAFE_OUTREACH_PATTERNS = (
    "unsolicited bulk outreach",
    "mass cold email",
    "cold email blast",
    "spam campaign",
    "bypass captcha",
    "bypass rate limit",
    "evade terms",
    "evade tos",
)

SAFE_SIGNAL_PATTERNS = (
    "opt-in",
    "first-party",
    "first party",
    "customer-authorized",
    "customer authorized",
    "authorized",
    "consensual",
    "owned audience",
    "crm",
    "listing service",
    "research brief",
    "template pack",
    "newsletter",
    "affiliate",
)

COMPLIANT_ALTERNATIVES = [
    "Customer-authorized inbox-to-CRM automation",
    "Opt-in newsletter or lead magnet funnel",
    "Autonomous listing concierge service",
    "Research brief or intelligence subscription",
    "Workflow automation templates or managed services",
]


def normalize_rating(value: str, default: str = MEDIUM) -> str:
    value = (value or "").strip().lower()
    if value in {LOW, MEDIUM, HIGH}:
        return value
    return default


def contains_pattern(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def build_text(*parts: str) -> str:
    return " ".join(part.strip() for part in parts if part).lower()


def blank_reason_map() -> dict[str, list[str]]:
    return {factor: [] for factor in HARD_FACTORS}


def infer_hard_factors(
    idea: str,
    customer: str,
    data_sources: str,
    distribution: str,
    constraints: str,
    ratings: dict[str, str],
) -> tuple[dict[str, str], dict[str, list[str]]]:
    text = build_text(idea, customer, data_sources, distribution, constraints)
    reasons = blank_reason_map()

    if contains_pattern(text, UNSAFE_DATA_PATTERNS):
        ratings["legality"] = LOW
        ratings["consent"] = LOW
        ratings["provenance"] = LOW
        reasons["legality"].append("Idea depends on personal contact-data resale or inbox harvesting.")
        reasons["consent"].append("Personal email resale does not preserve specific, revocable consent.")
        reasons["provenance"].append("Data provenance is unsafe or resale-oriented.")

    if contains_pattern(text, UNSAFE_OUTREACH_PATTERNS):
        ratings["platform_risk"] = LOW
        reasons["platform_risk"].append("Distribution plan suggests spam, anti-bot bypass, or platform-rule evasion.")

    if "gmail" in text or "workspace" in text or "inbox" in text:
        if ratings["provenance"] != LOW and not contains_pattern(text, SAFE_SIGNAL_PATTERNS):
            ratings["provenance"] = MEDIUM
            reasons["provenance"].append("Inbox usage requires explicit first-party authorization and limited scope.")
        if ratings["consent"] != LOW and not contains_pattern(text, SAFE_SIGNAL_PATTERNS):
            ratings["consent"] = MEDIUM
            reasons["consent"].append("Inbox workflows need explicit, revocable authorization.")

    if contains_pattern(text, SAFE_SIGNAL_PATTERNS):
        for factor in HARD_FACTORS:
            if ratings[factor] == MEDIUM:
                ratings[factor] = HIGH

    return ratings, reasons


def summarize_decision(
    decision: str,
    hard_failures: dict[str, list[str]],
    hard_holds: dict[str, list[str]],
    soft_lows: list[str],
    soft_high_count: int,
) -> str:
    if decision == "REJECT":
        failures = ", ".join(sorted(hard_failures.keys()))
        return f"Rejected because hard compliance gates failed: {failures}."
    if decision == "PASS":
        return (
            "Approved for execution because hard gates are clear, no soft factor is low, "
            f"and {soft_high_count} soft factors are high."
        )

    hold_reasons = sorted(hard_holds.keys())
    if soft_lows:
        hold_reasons.extend(soft_lows)
    hold_text = ", ".join(hold_reasons) if hold_reasons else "insufficient execution strength"
    return f"Held for clarification or improvement: {hold_text}."


def collect_hard_gate_details(
    ratings: dict[str, str],
    reasons: dict[str, list[str]],
    target_rating: str,
    fallback_prefix: str,
) -> dict[str, list[str]]:
    details: dict[str, list[str]] = {}
    for factor in HARD_FACTORS:
        if ratings[factor] != target_rating:
            continue
        factor_reasons = reasons.get(factor, [])
        if factor_reasons:
            details[factor] = factor_reasons
        else:
            details[factor] = [f"{fallback_prefix}: {factor} is rated {target_rating}."]
    return details


def build_fallback_plan(idea: str, customer: str, distribution: str) -> dict[str, Any]:
    return {
        "offer": idea or "Define a narrow, lawful revenue offer",
        "customer": customer or "Pick a clearly served customer segment",
        "acquisition": distribution or "Use opt-in, first-party channels",
        "delivery": "Start with a narrow service loop, then automate the repeated steps.",
        "compliance_checks": [
            "Confirm legality, consent, provenance, and platform compatibility",
            "Document retention and deletion rules for any customer data",
            "Avoid personal-data resale and unsolicited bulk outreach",
        ],
        "next_steps": [
            "Define the exact customer problem and paid deliverable",
            "Write the data-scope and consent checklist",
            "Run a small pilot before scaling automation",
        ],
    }


async def build_execution_plan(
    tool: "RevenuePlanning",
    idea: str,
    customer: str,
    data_sources: str,
    distribution: str,
    constraints: str,
    hard_ratings: dict[str, str],
    soft_ratings: dict[str, str],
) -> dict[str, Any]:
    system = """
You are a revenue planning assistant.
Return a JSON object with keys:
- offer
- customer
- acquisition
- delivery
- compliance_checks
- next_steps
Keep the plan lawful, privacy-preserving, first-party, and platform-compliant.
Never suggest personal-data resale, unsolicited bulk outreach, or inbox/contact harvesting for resale.
""".strip()

    message = json.dumps(
        {
            "idea": idea,
            "customer": customer,
            "data_sources": data_sources,
            "distribution": distribution,
            "constraints": constraints,
            "hard_ratings": hard_ratings,
            "soft_ratings": soft_ratings,
        },
        indent=2,
    )

    try:
        raw_plan = await tool.agent.call_utility_model(system=system, message=message)
        parsed = DirtyJson.parse_string(raw_plan)
        if isinstance(parsed, dict) and parsed:
            return parsed
    except Exception:
        pass

    return build_fallback_plan(idea, customer, distribution)


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        customer: str = "",
        data_sources: str = "",
        distribution: str = "",
        constraints: str = "",
        legality: str = MEDIUM,
        consent: str = MEDIUM,
        provenance: str = MEDIUM,
        platform_risk: str = MEDIUM,
        time: str = MEDIUM,
        margin: str = MEDIUM,
        repeatability: str = MEDIUM,
        automation: str = MEDIUM,
        defensibility: str = MEDIUM,
        **kwargs,
    ) -> Response:
        hard_ratings = {
            "legality": normalize_rating(legality),
            "consent": normalize_rating(consent),
            "provenance": normalize_rating(provenance),
            "platform_risk": normalize_rating(platform_risk),
        }
        soft_ratings = {
            "time": normalize_rating(time),
            "margin": normalize_rating(margin),
            "repeatability": normalize_rating(repeatability),
            "automation": normalize_rating(automation),
            "defensibility": normalize_rating(defensibility),
        }

        hard_ratings, hard_reasons = infer_hard_factors(
            idea=idea,
            customer=customer,
            data_sources=data_sources,
            distribution=distribution,
            constraints=constraints,
            ratings=hard_ratings,
        )

        hard_failures = collect_hard_gate_details(
            ratings=hard_ratings,
            reasons=hard_reasons,
            target_rating=LOW,
            fallback_prefix="Hard gate failed",
        )
        hard_holds = collect_hard_gate_details(
            ratings=hard_ratings,
            reasons=hard_reasons,
            target_rating=MEDIUM,
            fallback_prefix="Needs clarification",
        )
        soft_lows = [factor for factor in SOFT_FACTORS if soft_ratings[factor] == LOW]
        soft_high_count = sum(1 for factor in SOFT_FACTORS if soft_ratings[factor] == HIGH)

        decision = "HOLD"
        if hard_failures:
            decision = "REJECT"
        elif all(value == HIGH for value in hard_ratings.values()) and not soft_lows and soft_high_count >= 3:
            decision = "PASS"

        plan = None
        if decision != "REJECT":
            plan = await build_execution_plan(
                tool=self,
                idea=idea,
                customer=customer,
                data_sources=data_sources,
                distribution=distribution,
                constraints=constraints,
                hard_ratings=hard_ratings,
                soft_ratings=soft_ratings,
            )

        result = {
            "decision": decision,
            "summary": summarize_decision(
                decision=decision,
                hard_failures=hard_failures,
                hard_holds=hard_holds,
                soft_lows=soft_lows,
                soft_high_count=soft_high_count,
            ),
            "idea": idea,
            "customer": customer,
            "scorecard": {
                "hard": hard_ratings,
                "soft": soft_ratings,
                "soft_high_count": soft_high_count,
            },
            "hard_failures": hard_failures,
            "hard_holds": hard_holds,
            "soft_lows": soft_lows,
            "required_controls": [
                "Use only first-party, public, licensed, synthetic, or customer-authorized data",
                "Do not resell personal contact data or run unsolicited bulk outreach",
                "Document consent, retention, deletion, and platform constraints before launch",
            ],
            "compliant_alternatives": COMPLIANT_ALTERNATIVES if decision == "REJECT" else [],
            "execution_plan": plan,
        }

        return Response(message=json.dumps(result, indent=2), break_loop=False)
