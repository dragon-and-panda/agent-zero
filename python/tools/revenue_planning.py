from typing import Iterable

from python.helpers.tool import Response, Tool


BLOCKED_PATTERNS = (
    "sell email list",
    "sell email lists",
    "sell contact list",
    "sell contact lists",
    "compiled email list",
    "compiled email lists",
    "broker email list",
    "broker contact list",
    "harvest email",
    "scrape inbox",
    "gmail scraping",
    "sell inbox data",
    "resell personal data",
    "data brokerage",
)

PROHIBITED_HINTS = (
    "email list",
    "contact list",
    "gmail",
    "inbox",
    "mailbox",
    "sell",
    "broker",
    "resale",
    "extract",
    "harvest",
    "compile",
)

SAFE_ALTERNATIVES = (
    "Build a consent-based newsletter or research digest using opted-in subscribers.",
    "Build an owner-authorized inbox-to-CRM or support-triage workflow for existing opted-in relationships.",
    "Create a marketplace automation workflow for owned or client-authorized inventory.",
    "Sell premium reports based on public or licensed market data.",
    "Offer B2B automation services on client-authorized CRM, support, or operations data.",
    "Package recurring internal workflows as a micro-SaaS or paid template bundle.",
)

LEVEL_POINTS = {"low": 1, "medium": 2, "high": 3}
YES_VALUES = {"yes", "true", "y", "opt_in", "opted_in", "contractual"}
NO_VALUES = {"no", "false", "n", "none"}
UNCLEAR_VALUES = {"", "unknown", "unclear", "maybe"}
ALLOWED_PROVENANCE = {"first_party", "licensed", "public"}
REJECTED_PROVENANCE = {"private", "restricted", "stolen"}


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def normalize_level(value: str, default: str = "medium") -> str:
    value = normalize_text(value).replace(" ", "_")
    return value if value in LEVEL_POINTS else default


def normalize_boolean_like(value: str) -> str:
    value = normalize_text(value).replace(" ", "_")
    if value in YES_VALUES:
        return "yes"
    if value in NO_VALUES:
        return "no"
    if value in UNCLEAR_VALUES:
        return "unclear"
    return "unclear"


def normalize_provenance(value: str) -> str:
    value = normalize_text(value).replace(" ", "_")
    if value in ALLOWED_PROVENANCE | REJECTED_PROVENANCE | {"unclear"}:
        return value
    return "unclear"


def contains_blocked_pattern(text: str) -> bool:
    return any(pattern in text for pattern in BLOCKED_PATTERNS)


def mentions_private_contact_resale(text: str) -> bool:
    hits = sum(1 for hint in PROHIBITED_HINTS if hint in text)
    return hits >= 4


def join_nonempty(values: Iterable[str]) -> str:
    return " ".join(value for value in values if value).strip()


class RevenuePlanning(Tool):

    async def execute(
        self,
        venture_idea: str = "",
        monetization_model: str = "",
        data_provenance: str = "unclear",
        consent_status: str = "unclear",
        legal_basis: str = "unclear",
        platform_dependency: str = "medium",
        automation_level: str = "medium",
        margin_profile: str = "medium",
        recurring_revenue: str = "unclear",
        notes: str = "",
        **kwargs,
    ):
        combined_text = normalize_text(
            join_nonempty([venture_idea, monetization_model, notes])
        )
        consent_status = normalize_boolean_like(consent_status)
        legal_basis = normalize_boolean_like(legal_basis)
        recurring_revenue = normalize_boolean_like(recurring_revenue)
        data_provenance = normalize_provenance(data_provenance)
        platform_dependency = normalize_level(platform_dependency)
        automation_level = normalize_level(automation_level)
        margin_profile = normalize_level(margin_profile)

        reasons: list[str] = []
        next_steps: list[str] = []
        status = "PASS"

        if contains_blocked_pattern(combined_text) or mentions_private_contact_resale(
            combined_text
        ):
            status = "REJECT"
            reasons.append(
                "the idea involves private contact harvesting, inbox extraction, or personal-data resale"
            )
            next_steps.extend(SAFE_ALTERNATIVES[:3])

        if legal_basis == "no":
            status = "REJECT"
            reasons.append("there is no legal basis for the proposed workflow")

        if consent_status == "no":
            status = "REJECT"
            reasons.append("the workflow lacks required consent")

        if data_provenance in REJECTED_PROVENANCE:
            status = "REJECT"
            reasons.append("the data source is private, restricted, or otherwise not approved")

        if status != "REJECT":
            if legal_basis == "unclear":
                status = "HOLD"
                reasons.append("legal basis needs review before implementation")

            if consent_status == "unclear":
                status = "HOLD"
                reasons.append("consent status is unclear")

            if data_provenance == "unclear":
                status = "HOLD"
                reasons.append("data provenance is unclear")

            if platform_dependency == "high":
                status = "HOLD"
                reasons.append("platform dependency is high and needs safeguards")

            score = LEVEL_POINTS[automation_level] + LEVEL_POINTS[margin_profile]
            if recurring_revenue == "yes":
                score += 1
            if score <= 3:
                status = "HOLD"
                reasons.append("repeatability or margin profile is too weak for autonomous focus")

        if not reasons:
            reasons.append(
                "the idea appears compliant, automation-friendly, and based on acceptable data sources"
            )

        if status == "PASS":
            next_steps.extend(
                [
                    "Score the idea with /workspace/instruments/strategy/score.sh and log it in docs/strategy/incoming.md.",
                    "Draft a narrow MVP tied to first-party, public, or licensed data only.",
                    "Define revenue, margin, and platform concentration metrics before automation expands.",
                ]
            )
        elif status == "HOLD":
            next_steps.extend(
                [
                    "Clarify the legal basis, consent path, and exact provenance of every dataset.",
                    "Reduce single-platform risk or add a fallback distribution channel.",
                    "Prefer an opt-in audience, public research, or client-authorized operations workflow if uncertainty remains.",
                ]
            )
        else:
            if "gmail" in combined_text or "inbox" in combined_text or "mailbox" in combined_text:
                next_steps.append(
                    "If mailbox access is needed, limit it to owner-authorized summarization, invoicing, support triage, or follow-up drafting for existing opted-in relationships."
                )
            next_steps.extend(SAFE_ALTERNATIVES[3:])

        message_lines = [
            "Revenue planning assessment",
            f"Status: {status}",
            "",
            "Reasons:",
            *[f"- {reason}" for reason in reasons],
            "",
            "Recommended next steps:",
            *[f"- {step}" for step in next_steps],
        ]

        return Response(message="\n".join(message_lines), break_loop=False)
