from typing import Any, Iterable

BLOCKED_PATTERNS = (
    "broker email list",
    "build email list",
    "buy lead list",
    "compile email address lists",
    "contact database resale",
    "extract gmail addresses",
    "gmail lead extraction",
    "inbox scraping",
    "rent email list",
    "resell contacts",
    "sell compiled email lists",
    "sell email list",
    "sell leads",
    "sell the list",
)

SENSITIVE_SOURCES = (
    "gmail",
    "google workspace",
    "inbox",
    "mailbox",
    "outlook",
    "private correspondence",
)

EXTRACTION_TERMS = (
    "compile",
    "extract",
    "harvest",
    "list",
    "scrape",
    "sell",
)

HOLD_PATTERNS = (
    "cold outreach",
    "data enrichment",
    "lead generation",
    "prospecting",
)

SAFE_LANES = [
    "Productized automation services for client-owned workflows",
    "Agent templates, prompt packs, and niche software tools",
    "Paid market-intelligence briefs built from public data and original analysis",
    "Opt-in newsletter or audience products using first-party subscriber data",
    "Owner-authorized inbox or CRM hygiene for internal operations only",
]


def _to_list(raw: str | Iterable[str] | None) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        chunks = raw.replace("\n", ",").split(",")
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    return [str(item).strip() for item in raw if str(item).strip()]


def _contains_any(text: str, patterns: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def _format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- none"


def build_revenue_plan(
    objective: str,
    data_sources: str | Iterable[str] | None = None,
    intended_actions: str | Iterable[str] | None = None,
    constraints: str | Iterable[str] | None = None,
) -> dict[str, Any]:
    source_list = _to_list(data_sources)
    action_list = _to_list(intended_actions)
    constraint_list = _to_list(constraints)

    combined_text = " ".join(
        [objective, " ".join(source_list), " ".join(action_list), " ".join(constraint_list)]
    ).strip()
    lowered = combined_text.lower()

    blocked_reasons: list[str] = []
    hold_reasons: list[str] = []

    if _contains_any(lowered, BLOCKED_PATTERNS):
        blocked_reasons.append(
            "The plan describes contact-data resale, brokerage, or explicit email-list monetization."
        )

    if _contains_any(lowered, SENSITIVE_SOURCES) and _contains_any(lowered, EXTRACTION_TERMS):
        blocked_reasons.append(
            "The plan combines private inbox data with extraction or resale behavior."
        )

    if "gmail" in lowered and "rag" in lowered and (
        "email address" in lowered or "contact list" in lowered or "sell" in lowered
    ):
        blocked_reasons.append(
            "Gmail or Workspace content cannot be repurposed into contact lists for sale or unsolicited exploitation."
        )

    if not blocked_reasons and _contains_any(lowered, HOLD_PATTERNS):
        hold_reasons.append(
            "The plan touches outreach or lead workflows, so consent, owner authorization, and platform rules must be proven before execution."
        )

    if not blocked_reasons and _contains_any(lowered, SENSITIVE_SOURCES):
        hold_reasons.append(
            "Inbox data is sensitive. Limit use to owner-authorized internal operations unless a separate compliant basis is documented."
        )

    if blocked_reasons:
        status = "REJECT"
        summary = "Unsafe monetization path. Redirect to compliant first-party revenue lanes."
        next_steps = [
            "Do not execute the requested extraction or resale workflow.",
            "Replace the idea with a productized service, software, research, or opt-in audience model.",
            "If inbox data is involved, limit it to owner-authorized internal operations such as support triage or CRM hygiene.",
        ]
    elif hold_reasons:
        status = "HOLD"
        summary = "Potentially viable, but authority, consent, provenance, or platform compliance is not yet proven."
        next_steps = [
            "Document the data owner and intended use.",
            "Confirm consent and provenance for all contact records.",
            "Re-score legality, consent, provenance, and platform risk before proceeding.",
        ]
    else:
        status = "PASS"
        summary = "Compliant direction. Proceed with a scoped experiment and explicit success metrics."
        next_steps = [
            "Turn the idea into a small testable offer or product.",
            "Define pricing, acquisition channel, and proof-of-value metrics.",
            "Log outcomes in the strategy intake queue and program journal.",
        ]

    return {
        "status": status,
        "summary": summary,
        "objective": objective.strip(),
        "data_sources": source_list,
        "intended_actions": action_list,
        "constraints": constraint_list,
        "blocked_reasons": blocked_reasons,
        "hold_reasons": hold_reasons,
        "safe_lanes": SAFE_LANES,
        "next_steps": next_steps,
    }


def format_revenue_plan(plan: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Status: {plan['status']}",
            f"Summary: {plan['summary']}",
            "",
            "Objective:",
            plan["objective"] or "unspecified",
            "",
            "Data sources:",
            _format_bullets(plan["data_sources"]),
            "",
            "Intended actions:",
            _format_bullets(plan["intended_actions"]),
            "",
            "Blocked reasons:",
            _format_bullets(plan["blocked_reasons"]),
            "",
            "Hold reasons:",
            _format_bullets(plan["hold_reasons"]),
            "",
            "Recommended safe lanes:",
            _format_bullets(plan["safe_lanes"]),
            "",
            "Next steps:",
            _format_bullets(plan["next_steps"]),
        ]
    ).strip()
