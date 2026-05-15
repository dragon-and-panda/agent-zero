import json

from python.helpers.tool import Response, Tool

LOW_VALUE = "low"
MEDIUM_VALUE = "medium"
HIGH_VALUE = "high"

DISALLOWED_PATTERNS = {
    "personal_data_resale": [
        "sell email list",
        "sell compiled email lists",
        "resell contacts",
        "broker email",
        "broker leads",
        "lead list resale",
        "contact list for sale",
    ],
    "inbox_scraping": [
        "google email data",
        "gmail data",
        "gmail scrape",
        "scrape inbox",
        "harvest inbox",
        "extract emails",
        "email harvesting",
        "compile email address lists",
    ],
    "spam_or_unsolicited_outreach": [
        "bulk cold email",
        "cold blast",
        "spam campaign",
        "unsolicited outreach",
        "mass outreach",
    ],
    "platform_evasion": [
        "bypass captcha",
        "evade detection",
        "stealth browser",
        "anti-bot bypass",
        "hide automation",
    ],
}

AUTHORIZED_PATTERNS = [
    "opt-in",
    "opt in",
    "consenting user",
    "authorized",
    "with permission",
    "revocable consent",
    "customer-owned",
    "customer owned",
    "first-party",
    "first party",
    "official api",
    "crm sync",
    "newsletter subscriber",
]

FIRST_PARTY_PATTERNS = [
    "first-party",
    "first party",
    "customer-owned",
    "customer owned",
    "user-connected",
    "user connected",
    "crm export",
    "merchant catalog",
    "seller inventory",
]

SOFTWARE_PATTERNS = [
    "subscription",
    "saas",
    "software",
    "template",
    "digital product",
    "newsletter",
    "research product",
    "alert product",
]

SERVICE_PATTERNS = [
    "service",
    "listing service",
    "done-for-you",
    "concierge",
    "managed",
]

AUTOMATION_PATTERNS = [
    "automation",
    "agent",
    "workflow",
    "sync",
    "api",
    "webhook",
    "scheduled",
]


def _normalize_text(*parts: str) -> str:
    cleaned = [part.strip().lower() for part in parts if isinstance(part, str) and part.strip()]
    return " | ".join(cleaned)


def _matched_patterns(text: str, patterns: list[str]) -> list[str]:
    return [pattern for pattern in patterns if pattern in text]


def _collect_red_flags(text: str) -> dict[str, list[str]]:
    return {
        label: _matched_patterns(text, patterns)
        for label, patterns in DISALLOWED_PATTERNS.items()
        if _matched_patterns(text, patterns)
    }


def _score_hard_gates(text: str, red_flags: dict[str, list[str]]) -> dict[str, str]:
    if red_flags:
        return {
            "legality": LOW_VALUE,
            "consent": LOW_VALUE,
            "provenance": LOW_VALUE,
            "platform_alignment": LOW_VALUE,
        }

    consent_hits = _matched_patterns(text, AUTHORIZED_PATTERNS)
    provenance_hits = _matched_patterns(text, FIRST_PARTY_PATTERNS)
    platform_hits = _matched_patterns(text, ["official api", "crm", "marketplace", "newsletter", "subscription"])

    legality = HIGH_VALUE if consent_hits and platform_hits else MEDIUM_VALUE
    consent = HIGH_VALUE if consent_hits else MEDIUM_VALUE
    provenance = HIGH_VALUE if provenance_hits else MEDIUM_VALUE
    platform_alignment = HIGH_VALUE if platform_hits else MEDIUM_VALUE

    return {
        "legality": legality,
        "consent": consent,
        "provenance": provenance,
        "platform_alignment": platform_alignment,
    }


def _score_soft_factors(text: str, red_flags: dict[str, list[str]]) -> dict[str, str]:
    if red_flags:
        return {
            "time_to_cash": LOW_VALUE,
            "margin": LOW_VALUE,
            "repeatability": LOW_VALUE,
            "automation_fit": LOW_VALUE,
            "defensibility": LOW_VALUE,
        }

    software_hits = _matched_patterns(text, SOFTWARE_PATTERNS)
    service_hits = _matched_patterns(text, SERVICE_PATTERNS)
    automation_hits = _matched_patterns(text, AUTOMATION_PATTERNS)
    first_party_hits = _matched_patterns(text, FIRST_PARTY_PATTERNS)

    time_to_cash = HIGH_VALUE if service_hits else MEDIUM_VALUE
    margin = HIGH_VALUE if software_hits else MEDIUM_VALUE
    repeatability = HIGH_VALUE if software_hits or automation_hits else MEDIUM_VALUE
    automation_fit = HIGH_VALUE if automation_hits else MEDIUM_VALUE
    defensibility = HIGH_VALUE if first_party_hits else MEDIUM_VALUE

    return {
        "time_to_cash": time_to_cash,
        "margin": margin,
        "repeatability": repeatability,
        "automation_fit": automation_fit,
        "defensibility": defensibility,
    }


def _decision(hard_gates: dict[str, str], soft_scores: dict[str, str]) -> str:
    if any(value == LOW_VALUE for value in hard_gates.values()):
        return "REJECT"
    if any(value != HIGH_VALUE for value in hard_gates.values()):
        return "HOLD"
    if any(value == LOW_VALUE for value in soft_scores.values()):
        return "HOLD"
    soft_high_count = sum(1 for value in soft_scores.values() if value == HIGH_VALUE)
    if soft_high_count >= 3:
        return "PASS"
    return "HOLD"


def evaluate_plan(
    strategy: str = "",
    revenue_model: str = "",
    data_sources: str = "",
    channel: str = "",
    notes: str = "",
) -> dict[str, object]:
    text = _normalize_text(strategy, revenue_model, data_sources, channel, notes)
    red_flags = _collect_red_flags(text)
    hard_gates = _score_hard_gates(text, red_flags)
    soft_scores = _score_soft_factors(text, red_flags)
    decision = _decision(hard_gates, soft_scores)

    if decision == "REJECT":
        summary = (
            "Rejected because the plan appears to depend on privacy-invasive data use, "
            "weak consent, or platform-abuse patterns."
        )
        next_steps = [
            "remove any scraping, resale, or inbox-harvesting step",
            "rewrite the lane around first-party or opt-in data",
            "prefer customer-owned integrations and official APIs",
        ]
    elif decision == "PASS":
        summary = (
            "The plan clears the hard compliance gates and looks viable enough for a small, "
            "reversible pilot."
        )
        next_steps = [
            "define a narrow pilot and success metric",
            "record the lane in docs/strategy/incoming.md and the mission journal",
            "cross-check with instruments/strategy/score.sh before execution",
        ]
    else:
        summary = (
            "Hold for clarification. The plan is not clearly disallowed, but legality, consent, "
            "provenance, or platform alignment is not yet strong enough."
        )
        next_steps = [
            "document the consent model and data provenance",
            "switch to official APIs or customer-owned data sources where possible",
            "tighten the offer and pilot scope before launch",
        ]

    safer_alternatives = [
        "inbox-to-CRM processing for consenting account owners",
        "autonomous listing services for sellers",
        "research summaries, benchmarks, or alert products",
        "opt-in newsletter, template, or micro-SaaS products",
    ]

    return {
        "decision": decision,
        "summary": summary,
        "hard_gates": hard_gates,
        "soft_scores": soft_scores,
        "red_flags": red_flags,
        "safer_alternatives": safer_alternatives,
        "next_steps": next_steps,
    }


class RevenuePlanning(Tool):
    async def execute(
        self,
        strategy: str = "",
        revenue_model: str = "",
        data_sources: str = "",
        channel: str = "",
        notes: str = "",
        **kwargs,
    ):
        result = evaluate_plan(
            strategy=strategy,
            revenue_model=revenue_model,
            data_sources=data_sources,
            channel=channel,
            notes=notes,
        )
        return Response(message=json.dumps(result, indent=2), break_loop=False)
