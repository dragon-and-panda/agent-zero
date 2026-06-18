from dataclasses import asdict, dataclass


PROHIBITED_PATTERNS = {
    "contact list brokerage": (
        "sell email list",
        "selling email list",
        "resell email list",
        "broker email list",
        "email lists",
        "email address list",
        "contact list for sale",
        "lead list for sale",
        "sell compiled email",
        "sell compiled email lists",
    ),
    "non-consensual inbox extraction": (
        "gmail inbox",
        "google email data",
        "harvest emails",
        "scrape inbox",
        "extract email addresses from emails",
        "compile email address list",
    ),
    "spam or unsolicited outreach": (
        "cold blast",
        "bulk outreach",
        "spam",
        "unsolicited outreach",
        "bypass unsubscribe",
        "skip consent",
    ),
}

PERSONAL_DATA_PATTERNS = (
    "email",
    "emails",
    "contact",
    "contacts",
    "gmail",
    "inbox",
    "personal data",
    "customer data",
    "lead data",
)

CONSENT_POSITIVE_PATTERNS = (
    "opt in",
    "opt-in",
    "double opt in",
    "double opt-in",
    "documented consent",
    "signed dpa",
    "client authorized",
    "first party",
    "first-party",
)

SAFE_MONETIZATION_PATTERNS = (
    "newsletter",
    "subscription",
    "consulting",
    "automation service",
    "workflow service",
    "crm hygiene",
    "lead magnet",
    "course",
    "template",
    "research product",
)


@dataclass
class RevenueAssessment:
    decision: str
    summary: str
    blockers: list[str]
    required_controls: list[str]
    safer_alternatives: list[str]
    matched_signals: list[str]


def _normalize(*parts: str) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def _has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in text for pattern in patterns)


def assess_revenue_plan(
    objective: str = "",
    data_sources: str = "",
    acquisition_method: str = "",
    monetization_plan: str = "",
    notes: str = "",
) -> dict[str, object]:
    text = _normalize(
        objective,
        data_sources,
        acquisition_method,
        monetization_plan,
        notes,
    )
    matched_signals: list[str] = []
    blockers: list[str] = []
    required_controls: list[str] = []
    safer_alternatives: list[str] = [
        (
            "Use inbox or Gmail RAG only for owner-authorized search, "
            "summarization, and workflow automation."
        ),
        (
            "Sell a service, workflow, report, or software product "
            "instead of selling personal contact data."
        ),
        (
            "Build opt-in acquisition loops such as newsletters, lead "
            "magnets, referrals, or client-authorized CRM hygiene."
        ),
    ]

    for label, patterns in PROHIBITED_PATTERNS.items():
        if _has_any(text, patterns):
            matched_signals.append(label)

    touches_personal_data = _has_any(text, PERSONAL_DATA_PATTERNS)
    has_positive_consent = _has_any(text, CONSENT_POSITIVE_PATTERNS)
    has_safe_monetization = _has_any(text, SAFE_MONETIZATION_PATTERNS)

    if matched_signals:
        blockers.extend(
            [
                "Personal email/contact data cannot be harvested, compiled from inboxes, or sold as a brokerage asset.",
                "Unsolicited outreach and list resale create legal, privacy, and platform-enforcement risk.",
            ]
        )
        required_controls.extend(
            [
                "Drop the contact-data resale path entirely.",
                (
                    "Redesign the workflow around first-party consent, "
                    "client authorization, or non-personal-data products."
                ),
            ]
        )
        assessment = RevenueAssessment(
            decision="REJECT",
            summary=(
                "The proposed revenue path relies on prohibited "
                "contact-data extraction, resale, or spam-like behavior."
            ),
            blockers=blockers,
            required_controls=required_controls,
            safer_alternatives=safer_alternatives,
            matched_signals=matched_signals,
        )
        return asdict(assessment)

    if touches_personal_data and not has_positive_consent:
        matched_signals.append("personal-data handling without documented consent")
        blockers.append(
            (
                "Plans that touch inbox, email, or customer-contact data "
                "need explicit authorization, clear provenance, and "
                "documented consent."
            )
        )
        required_controls.extend(
            [
                "Document who owns the data and why you are authorized to process it.",
                (
                    "Prove each contact has opted in or is covered by a "
                    "lawful existing-customer basis before outreach."
                ),
                (
                    "Review jurisdiction-specific privacy and anti-spam "
                    "rules before launching automation."
                ),
            ]
        )
        assessment = RevenueAssessment(
            decision="HOLD",
            summary=(
                "The idea might be salvageable, but it cannot proceed until "
                "consent, provenance, and lawful-use controls are explicit."
            ),
            blockers=blockers,
            required_controls=required_controls,
            safer_alternatives=safer_alternatives,
            matched_signals=matched_signals,
        )
        return asdict(assessment)

    required_controls.extend(
        [
            "Keep an audit trail for data provenance, consent status, and unsubscribe handling.",
            (
                "Review the terms of every platform involved before "
                "automating acquisition or outreach."
            ),
            "Prefer first-party, opt-in, and service-led monetization over data monetization.",
        ]
    )

    if has_safe_monetization or has_positive_consent or not touches_personal_data:
        matched_signals.append("compliance-compatible revenue lane")
        summary = (
            "The idea fits an allowed lane if it stays focused on first-party "
            "consent, service delivery, or non-personal-data products."
        )
    else:
        matched_signals.append("general revenue idea")
        summary = (
            "The idea is directionally acceptable, but it still needs "
            "explicit controls before autonomous execution."
        )

    assessment = RevenueAssessment(
        decision="PASS",
        summary=summary,
        blockers=blockers,
        required_controls=required_controls,
        safer_alternatives=safer_alternatives,
        matched_signals=matched_signals,
    )
    return asdict(assessment)
