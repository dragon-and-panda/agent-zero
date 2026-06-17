from dataclasses import dataclass


REJECT_PATTERNS = (
    "sell email list",
    "selling email lists",
    "broker email list",
    "email list resale",
    "contact list resale",
    "data brokerage",
    "gmail scrape",
    "scrape gmail",
    "google email data",
    "harvest emails",
    "compiled email list",
    "cold email list",
)

HOLD_PATTERNS = (
    "trading",
    "wagering",
    "betting",
    "gambling",
    "financial advice",
    "securities",
)

PASS_PATTERNS = (
    "first-party",
    "first party",
    "client-authorized",
    "client authorized",
    "crm hygiene",
    "crm cleanup",
    "listing service",
    "marketplace optimization",
    "research brief",
    "opt-in",
    "newsletter",
    "affiliate",
)


@dataclass
class RevenuePlanAssessment:
    verdict: str
    summary: str
    reasons: list[str]
    safer_alternatives: list[str]
    next_actions: list[str]


def _normalize(*parts: str) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def assess_revenue_plan(
    mission: str,
    assets: str = "",
    constraints: str = "",
) -> RevenuePlanAssessment:
    text = _normalize(mission, assets, constraints)

    if _contains_any(text, REJECT_PATTERNS):
        return RevenuePlanAssessment(
            verdict="REJECT",
            summary="The plan depends on personal-data resale or non-consensual contact harvesting.",
            reasons=[
                "Contact-list brokerage and inbox-derived email resale are prohibited.",
                "The request creates privacy, anti-spam, and platform-policy risk.",
                "Revenue should come from consent-based services or first-party operations.",
            ],
            safer_alternatives=[
                "client-authorized inbox-to-CRM hygiene",
                "opt-in newsletter growth",
                "autonomous listing optimization",
                "lawful research products built from public or licensed data",
            ],
            next_actions=[
                "Redesign the lane around first-party value delivery.",
                "Preserve consent, suppression, and provenance metadata.",
                "Score the replacement lane before activation.",
            ],
        )

    if _contains_any(text, HOLD_PATTERNS):
        return RevenuePlanAssessment(
            verdict="HOLD",
            summary="The lane may be legal, but it needs tighter risk, licensing, and platform review before automation.",
            reasons=[
                "Higher-regulation revenue categories need explicit compliance review.",
                "Autonomous execution should stay limited until risk controls are defined.",
            ],
            safer_alternatives=[
                "simulation-only validation",
                "operator-reviewed pilots",
                "lower-regulation service lanes",
            ],
            next_actions=[
                "Document the regulatory surface area.",
                "Run a limited pilot with clear loss and policy thresholds.",
                "Only proceed after the hard gates score high enough.",
            ],
        )

    if _contains_any(text, PASS_PATTERNS):
        return RevenuePlanAssessment(
            verdict="PASS",
            summary="The lane fits a consent-based, auditable automation model.",
            reasons=[
                "The plan centers on first-party or client-authorized value creation.",
                "The monetization path can be packaged into repeatable operational workflows.",
            ],
            safer_alternatives=[
                "add an opt-in acquisition layer",
                "bundle delivery with reporting and CRM feedback loops",
            ],
            next_actions=[
                "Score the lane with instruments/strategy/score.sh.",
                "Define a small pilot and success metrics.",
                "Turn the winning flow into tools or instruments.",
            ],
        )

    return RevenuePlanAssessment(
        verdict="HOLD",
        summary="The idea needs clearer data provenance, consent, and monetization detail before execution.",
        reasons=[
            "The lane is not obviously prohibited, but its operating model is underspecified.",
            "Autonomy should follow a documented authorization and platform-compliance path.",
        ],
        safer_alternatives=[
            "tighten the offer around first-party operations",
            "use opt-in acquisition instead of purchased contacts",
        ],
        next_actions=[
            "Clarify who owns the data, who consented, and how the platform allows the workflow.",
            "Describe the revenue loop in enough detail to score it.",
        ],
    )


def format_assessment(assessment: RevenuePlanAssessment) -> str:
    sections = [
        f"verdict: {assessment.verdict}",
        f"summary: {assessment.summary}",
        "reasons:",
        *[f"- {reason}" for reason in assessment.reasons],
        "safer_alternatives:",
        *[f"- {alternative}" for alternative in assessment.safer_alternatives],
        "next_actions:",
        *[f"- {action}" for action in assessment.next_actions],
    ]
    return "\n".join(sections)
