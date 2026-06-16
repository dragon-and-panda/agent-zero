from dataclasses import dataclass
from typing import Iterable


REJECT_PHRASES = (
    "sell compiled email lists",
    "sell email lists",
    "sell the email list",
    "resell email lists",
    "email list resale",
    "list brokerage",
    "contact brokerage",
    "broker email lists",
    "harvest inbox contacts",
    "scrape inbox contacts",
    "scrape gmail",
    "gmail scraping",
    "google email data",
    "cold outreach without consent",
    "spam campaign",
)

HIGH_RISK_DATA_PHRASES = (
    "gmail",
    "google workspace",
    "google email",
    "mailbox",
    "inbox",
    "email export",
)

SAFE_SIGNAL_PHRASES = (
    "owner-authorized",
    "owner authorized",
    "client-authorized",
    "client authorized",
    "first-party",
    "first party",
    "opt-in",
    "opted-in",
    "opted in",
    "crm hygiene",
    "customer export",
    "public data",
    "public sources",
)


@dataclass
class RevenuePlanAssessment:
    decision: str
    summary: str
    reasons: list[str]
    safer_alternatives: list[str]
    next_steps: list[str]


def _normalize_text(parts: Iterable[str]) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def assess_revenue_plan(
    mission: str = "",
    data_sources: str = "",
    monetization: str = "",
    delivery: str = "",
    constraints: str = "",
) -> RevenuePlanAssessment:
    text = _normalize_text([mission, data_sources, monetization, delivery, constraints])
    reasons: list[str] = []
    safer_alternatives: list[str] = []
    next_steps: list[str] = []

    if _contains_any(text, REJECT_PHRASES):
        reasons.append(
            "The plan depends on email-list resale, inbox harvesting, or other privacy-invasive contact monetization."
        )
        reasons.append(
            "Private mailbox data and compiled personal contact lists cannot be turned into third-party inventory."
        )
        safer_alternatives.extend(
            [
                "Convert the workflow into owner-authorized CRM hygiene for first-party use.",
                "Build a public-data research product instead of selling personal contacts.",
                "Use opt-in audience growth or listing services as the monetization lane.",
            ]
        )
        next_steps.extend(
            [
                "Remove any resale, brokerage, or cold-outreach assumptions.",
                "Document a lawful data source and consent basis.",
                "Rescore the replacement lane with the strategy instrument.",
            ]
        )
        return RevenuePlanAssessment(
            decision="REJECT",
            summary="Rejected: the requested monetization path relies on non-consensual or resale-oriented contact data use.",
            reasons=reasons,
            safer_alternatives=safer_alternatives,
            next_steps=next_steps,
        )

    if _contains_any(text, HIGH_RISK_DATA_PHRASES):
        reasons.append(
            "Mailbox and email-content workflows require explicit owner authorization and a first-party purpose."
        )
        if _contains_any(text, SAFE_SIGNAL_PHRASES):
            reasons.append(
                "The plan includes signals consistent with first-party or owner-authorized processing."
            )
            safer_alternatives.extend(
                [
                    "Limit the workflow to CRM cleanup, support triage, or customer-success enrichment.",
                    "Keep extracted contacts inside the owner's systems and do not resell them.",
                ]
            )
            next_steps.extend(
                [
                    "Record owner authorization and consent basis.",
                    "Use the consent-contact extraction instrument on exported files only.",
                    "Run the lane through the strategy scorer before activation.",
                ]
            )
            return RevenuePlanAssessment(
                decision="PASS",
                summary="Pass with guardrails: mailbox data may be processed only for first-party, owner-authorized operations.",
                reasons=reasons,
                safer_alternatives=safer_alternatives,
                next_steps=next_steps,
            )

        reasons.append(
            "The plan does not clearly establish authorization, consent basis, or a first-party use case."
        )
        safer_alternatives.extend(
            [
                "Reframe the mission as owner-authorized CRM hygiene.",
                "Switch to public-data research if first-party authorization is unavailable.",
            ]
        )
        next_steps.extend(
            [
                "Document who owns the mailbox or export.",
                "Specify the lawful purpose and consent basis.",
                "Do not proceed until the ambiguity is resolved.",
            ]
        )
        return RevenuePlanAssessment(
            decision="HOLD",
            summary="Hold: mailbox data is involved, but authorization or consent details are incomplete.",
            reasons=reasons,
            safer_alternatives=safer_alternatives,
            next_steps=next_steps,
        )

    if _contains_any(text, SAFE_SIGNAL_PHRASES):
        reasons.append(
            "The plan appears to use first-party, consent-based, or public data sources."
        )
        safer_alternatives.extend(
            [
                "Prefer recurring services, subscriptions, or productized research over one-off execution.",
                "Capture provenance and scoring notes in the strategy intake queue.",
            ]
        )
        next_steps.extend(
            [
                "Run the lane through the strategy scorer.",
                "Add the lane to docs/strategy/incoming.md with a PASS or HOLD decision.",
            ]
        )
        return RevenuePlanAssessment(
            decision="PASS",
            summary="Pass: the lane looks compatible with a lawful, consent-based revenue system.",
            reasons=reasons,
            safer_alternatives=safer_alternatives,
            next_steps=next_steps,
        )

    reasons.append(
        "The mission may be commercially valid, but the data rights, channel rules, or consent basis are underspecified."
    )
    safer_alternatives.extend(
        [
            "Use public-data research, opt-in audience growth, or listing services while clarifying data rights.",
            "Prefer first-party customer operations over third-party data acquisition.",
        ]
    )
    next_steps.extend(
        [
            "Clarify data provenance, consent basis, and platform terms.",
            "Score the lane before any automation or outreach begins.",
        ]
    )
    return RevenuePlanAssessment(
        decision="HOLD",
        summary="Hold: more detail is needed before the lane can be approved for autonomous execution.",
        reasons=reasons,
        safer_alternatives=safer_alternatives,
        next_steps=next_steps,
    )


def format_assessment(assessment: RevenuePlanAssessment) -> str:
    sections = [
        f"Decision: {assessment.decision}",
        f"Summary: {assessment.summary}",
        "Reasons:",
        *[f"- {reason}" for reason in assessment.reasons],
        "Safer alternatives:",
        *[f"- {alternative}" for alternative in assessment.safer_alternatives],
        "Next steps:",
        *[f"- {step}" for step in assessment.next_steps],
    ]
    return "\n".join(sections)
