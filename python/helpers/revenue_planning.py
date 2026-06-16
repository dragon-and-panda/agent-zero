from __future__ import annotations

from dataclasses import dataclass


DISALLOWED_DATA_BROKERAGE = (
    "sell email list",
    "sell email lists",
    "sell the email list",
    "rent email list",
    "broker email list",
    "trade email list",
    "compiled email list",
    "email address list",
    "contact list resale",
)

DISALLOWED_UNAUTHORIZED_ACCESS = (
    "gmail",
    "google email",
    "google mail",
    "inbox",
    "mailbox",
    "scrape email",
    "harvest email",
    "extract email addresses",
    "pull contacts from email",
)

REQUIRES_CONSENT_REVIEW = (
    "lead generation",
    "cold email",
    "outreach",
    "prospecting",
    "list building",
    "contact enrichment",
)

SAFE_DATA_HINTS = (
    "first-party",
    "first party",
    "opt-in",
    "opt in",
    "consent",
    "authorized",
    "crm",
    "newsletter",
    "customer",
    "subscriber",
)

SAFE_REVENUE_LANES = (
    "Build first-party opt-in funnels such as lead magnets newsletters or webinars.",
    "Offer productized services where the agent helps research qualify and draft work for real clients.",
    "Use RAG on user-authorized internal mail or docs for productivity and support only, not for contact resale.",
    "Run CRM hygiene tasks such as consent auditing deduplication segmentation and suppression handling.",
    "Create affiliate or content workflows that monetize audience trust without selling personal data.",
)


@dataclass
class PlanAssessment:
    decision: str
    summary: str
    reasons: list[str]
    required_evidence: list[str]
    safer_alternatives: list[str]
    flags: list[str]


def _normalize(*parts: str) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def _mentions_safe_data(text: str) -> bool:
    return _contains_any(text, SAFE_DATA_HINTS)


def assess_revenue_plan(
    mission: str,
    data_sources: str = "",
    consent_basis: str = "",
    monetization_target: str = "",
    notes: str = "",
) -> PlanAssessment:
    text = _normalize(mission, data_sources, consent_basis, monetization_target, notes)
    reasons: list[str] = []
    required_evidence: list[str] = []
    safer_alternatives = list(SAFE_REVENUE_LANES)
    flags: list[str] = []

    data_brokerage = _contains_any(text, DISALLOWED_DATA_BROKERAGE)
    unauthorized_mail = _contains_any(text, DISALLOWED_UNAUTHORIZED_ACCESS) and (
        "sell" in text
        or "compile" in text
        or "list" in text
        or "monetiz" in text
        or "extract" in text
    )
    consent_risk = _contains_any(text, REQUIRES_CONSENT_REVIEW) and not _mentions_safe_data(
        text
    )

    if data_brokerage:
        flags.append("personal-data-resale")
        reasons.append(
            "The plan involves selling or brokering personal contact data, which is not a compliant revenue model."
        )

    if unauthorized_mail:
        flags.append("unauthorized-inbox-extraction")
        reasons.append(
            "The plan relies on extracting contacts from inbox or mailbox content for monetization, which is privacy-invasive and high risk."
        )

    if data_brokerage or unauthorized_mail:
        required_evidence.extend(
            [
                "Use only first-party or explicitly authorized records for any future contact workflow.",
                "Document recipient consent, lawful purpose, retention rules, and suppression handling before outreach.",
            ]
        )
        return PlanAssessment(
            decision="REJECT",
            summary=(
                "Reject this plan and redirect to first-party, consent-based revenue systems. "
                "Do not harvest inbox contacts or sell email lists."
            ),
            reasons=reasons,
            required_evidence=required_evidence,
            safer_alternatives=safer_alternatives,
            flags=flags,
        )

    if consent_risk:
        flags.append("missing-consent-details")
        reasons.append(
            "The plan mentions outreach or lead generation but does not establish a clear consent basis or authorized data source."
        )
        required_evidence.extend(
            [
                "Name the data source and prove it is first-party or explicitly authorized.",
                "Show the consent mechanism or existing business relationship that allows outreach.",
                "Define unsubscribe or suppression handling before any automation is used.",
            ]
        )
        return PlanAssessment(
            decision="HOLD",
            summary=(
                "Pause implementation until consent, provenance, and platform-policy facts are documented."
            ),
            reasons=reasons,
            required_evidence=required_evidence,
            safer_alternatives=safer_alternatives,
            flags=flags,
        )

    if _mentions_safe_data(text):
        reasons.append(
            "The plan references first-party or consent-based data, which can be workable if processing stays within documented permissions."
        )
        required_evidence.extend(
            [
                "Keep consent timestamps or equivalent authorization records.",
                "Limit use to the stated business purpose and honor unsubscribe or deletion requests.",
                "Avoid sharing raw personal data with third parties unless contract terms and notice explicitly allow it.",
            ]
        )
        return PlanAssessment(
            decision="PASS",
            summary=(
                "This plan appears directionally compliant if execution remains limited to authorized first-party workflows."
            ),
            reasons=reasons,
            required_evidence=required_evidence,
            safer_alternatives=safer_alternatives,
            flags=flags,
        )

    reasons.append(
        "The plan does not provide enough information to confirm legality, consent, or data provenance."
    )
    required_evidence.extend(
        [
            "Clarify whether personal data is involved at all.",
            "If personal data is involved, identify source, authorization, purpose, and retention rules.",
        ]
    )
    return PlanAssessment(
        decision="HOLD",
        summary="Gather the missing compliance details before implementation.",
        reasons=reasons,
        required_evidence=required_evidence,
        safer_alternatives=safer_alternatives,
        flags=["insufficient-detail"],
    )


def format_assessment(assessment: PlanAssessment) -> str:
    lines = [
        f"decision: {assessment.decision}",
        f"summary: {assessment.summary}",
        "",
        "reasons:",
    ]
    lines.extend(f"- {reason}" for reason in assessment.reasons)
    lines.extend(
        [
            "",
            "required_evidence:",
        ]
    )
    lines.extend(f"- {item}" for item in assessment.required_evidence)
    lines.extend(
        [
            "",
            "safer_alternatives:",
        ]
    )
    lines.extend(f"- {item}" for item in assessment.safer_alternatives)
    lines.extend(["", "flags:"])
    lines.extend(f"- {flag}" for flag in assessment.flags)
    return "\n".join(lines)
