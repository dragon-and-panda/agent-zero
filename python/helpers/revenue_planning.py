from __future__ import annotations

from dataclasses import dataclass
import re


REJECT_PATTERNS = {
    "personal-data resale": [
        r"\bsell(?:ing)?\b.{0,40}\bemail list",
        r"\bemail list\b.{0,40}\b(?:sell|resell|broker|rent|monetiz)",
        r"\bcontact list\b.{0,40}\b(?:sell|resell|broker|rent)",
        r"\bbroker(?:ing)?\b.{0,40}\b(?:emails|contacts|leads)",
        r"\b(?:harvest|scrape|compile)\b.{0,40}\b(?:emails|addresses|contacts)",
    ],
    "inbox misuse": [
        r"\bgmail\b.{0,40}\b(?:sell|resell|list|broker|extract)",
        r"\bgoogle email\b.{0,40}\b(?:sell|resell|list|broker|extract)",
        r"\binbox\b.{0,40}\b(?:scrape|harvest|extract)",
        r"\bmailbox\b.{0,40}\b(?:scrape|harvest|extract)",
    ],
    "spam or non-consensual outreach": [
        r"\bcold outreach\b",
        r"\bmass outreach\b",
        r"\bunsolicited\b",
        r"\bspam\b",
    ],
}

POSITIVE_CONSENT_SIGNALS = (
    "authorized",
    "client-owned",
    "client owned",
    "first-party",
    "first party",
    "opt-in",
    "opt in",
    "consent",
    "crm hygiene",
    "newsletter subscribers",
)

POSITIVE_MODEL_SIGNALS = (
    "service",
    "subscription",
    "retainer",
    "listing",
    "software",
    "automation",
    "research",
    "product",
)


@dataclass
class RevenueAssessment:
    verdict: str
    summary: str
    legality: str
    consent: str
    provenance: str
    platform_compliance: str
    reasons: list[str]
    safer_alternatives: list[str]
    next_actions: list[str]


def _combined_text(
    mission: str,
    revenue_model: str,
    data_sources: str,
    operating_constraints: str,
) -> str:
    parts = [
        mission.strip(),
        revenue_model.strip(),
        data_sources.strip(),
        operating_constraints.strip(),
    ]
    return "\n".join(part for part in parts if part).lower()


def _find_reject_reasons(text: str) -> list[str]:
    reasons: list[str] = []
    for label, patterns in REJECT_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns):
            reasons.append(label)
    return reasons


def _has_any_signal(text: str, signals: tuple[str, ...]) -> bool:
    return any(signal in text for signal in signals)


def evaluate_revenue_plan(
    mission: str,
    revenue_model: str = "",
    data_sources: str = "",
    operating_constraints: str = "",
) -> RevenueAssessment:
    text = _combined_text(
        mission=mission,
        revenue_model=revenue_model,
        data_sources=data_sources,
        operating_constraints=operating_constraints,
    )

    reject_reasons = _find_reject_reasons(text)
    consent_signal = _has_any_signal(text, POSITIVE_CONSENT_SIGNALS)
    product_signal = _has_any_signal(text, POSITIVE_MODEL_SIGNALS)

    safer_alternatives = [
        "first-party inbox-to-CRM hygiene for an authorized client",
        "autonomous listing or resale services for owned inventory",
        "research products or software tools built from public or licensed data",
    ]

    if reject_reasons:
        return RevenueAssessment(
            verdict="REJECT",
            summary=(
                "This proposal relies on privacy-invasive or non-compliant monetization patterns."
            ),
            legality="low",
            consent="low",
            provenance="low",
            platform_compliance="low",
            reasons=[
                "Detected high-risk pattern: " + reason for reason in reject_reasons
            ],
            safer_alternatives=safer_alternatives,
            next_actions=[
                "Replace any resale or scraping objective with a first-party or opt-in workflow.",
                "Document account ownership, consent, and platform rules before proceeding.",
            ],
        )

    if not consent_signal:
        return RevenueAssessment(
            verdict="HOLD",
            summary=(
                "The proposal may be viable, but it lacks explicit consent, ownership, or provenance language."
            ),
            legality="medium",
            consent="medium",
            provenance="medium",
            platform_compliance="medium",
            reasons=[
                "No strong signal that the data or channel is first-party, client-authorized, or opt-in."
            ],
            safer_alternatives=safer_alternatives,
            next_actions=[
                "Clarify who owns the data, which contacts consented, and which platforms will be used.",
                "Run the lane through the scoring instrument after the operating scope is explicit.",
            ],
        )

    verdict = "PASS" if product_signal else "HOLD"
    summary = (
        "The proposal is aligned with compliant, first-party revenue operations."
        if verdict == "PASS"
        else "The proposal is compliant so far, but the business model needs more definition."
    )

    next_actions = [
        "Score the lane with instruments/strategy/score.sh.",
        "Limit execution to first-party or client-authorized datasets.",
        "Preserve consent and provenance in every exported record.",
    ]
    if verdict == "HOLD":
        next_actions.append(
            "Tighten the offer into a clearer service, product, or subscription model."
        )

    return RevenueAssessment(
        verdict=verdict,
        summary=summary,
        legality="high",
        consent="high",
        provenance="high",
        platform_compliance="high",
        reasons=[
            "Found explicit consent or authorization language.",
            "No personal-data resale or inbox-harvesting pattern was detected.",
        ],
        safer_alternatives=safer_alternatives,
        next_actions=next_actions,
    )


def format_assessment_markdown(assessment: RevenueAssessment) -> str:
    lines = [
        f"VERDICT: {assessment.verdict}",
        "",
        assessment.summary,
        "",
        "Hard-gate assessment:",
        f"- legality: {assessment.legality}",
        f"- consent: {assessment.consent}",
        f"- provenance: {assessment.provenance}",
        f"- platform_compliance: {assessment.platform_compliance}",
        "",
        "Reasons:",
    ]
    lines.extend(f"- {reason}" for reason in assessment.reasons)
    lines.extend(
        [
            "",
            "Safer alternatives:",
        ]
    )
    lines.extend(f"- {alternative}" for alternative in assessment.safer_alternatives)
    lines.extend(
        [
            "",
            "Next actions:",
        ]
    )
    lines.extend(f"- {action}" for action in assessment.next_actions)
    return "\n".join(lines)
