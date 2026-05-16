from python.helpers.tool import Tool, Response


TRUE_VALUES = {"1", "true", "yes", "y", "on"}
LOW_WORDS = {"low", "weak", "unclear", "unknown", "none", "missing"}
HIGH_WORDS = {"high", "strong", "clear", "documented", "opt-in", "opted-in"}

CONTACT_RESALE_TERMS = {
    "sell email list",
    "sell email lists",
    "sell contact list",
    "sell contact lists",
    "broker email",
    "broker emails",
    "broker contact",
    "broker contacts",
    "rent list",
    "rent lists",
    "resell contacts",
    "resale of personal contact data",
    "list brokerage",
}
MAILBOX_TERMS = {"gmail", "google email", "mailbox", "inbox", "email archive"}
HARVEST_TERMS = {"scrape", "harvest", "compile", "extract", "collect", "export"}
OUTREACH_TERMS = {"cold email", "mass email", "bulk email", "blast", "outreach"}


def _flatten(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {_flatten(val)}" for key, val in value.items())
    return str(value)


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in TRUE_VALUES


def _rating_bucket(value: str) -> str:
    text = value.strip().lower()
    if not text:
        return "unknown"
    if text in HIGH_WORDS or "high" in text or "opt-in" in text or "authorized" in text:
        return "high"
    if text in LOW_WORDS or "low" in text or "unknown" in text or "unclear" in text:
        return "low"
    return "medium"


class RevenuePlanning(Tool):
    async def execute(
        self,
        proposal="",
        lane="",
        data_sources="",
        automation_plan="",
        monetization_model="",
        consent_status="",
        provenance="",
        platform_rules="",
        owner_authorized=False,
        notes="",
        **kwargs,
    ):
        combined = " ".join(
            [
                _flatten(proposal),
                _flatten(lane),
                _flatten(data_sources),
                _flatten(automation_plan),
                _flatten(monetization_model),
                _flatten(notes),
                _flatten(kwargs),
            ]
        ).lower()

        consent_bucket = _rating_bucket(_flatten(consent_status))
        provenance_bucket = _rating_bucket(_flatten(provenance))
        platform_bucket = _rating_bucket(_flatten(platform_rules))
        owner_authorized_flag = _as_bool(owner_authorized)

        hard_failures = []
        hard_holds = []
        alternatives = []

        has_contact_resale = any(term in combined for term in CONTACT_RESALE_TERMS)
        touches_mailbox = any(term in combined for term in MAILBOX_TERMS)
        has_harvest_behavior = any(term in combined for term in HARVEST_TERMS)
        has_outreach_behavior = any(term in combined for term in OUTREACH_TERMS)

        if has_contact_resale:
            hard_failures.append(
                "The plan relies on brokering or selling personal contact data."
            )
            alternatives.extend(
                [
                    "Build an opt-in lead funnel instead of selling a contact list.",
                    "Offer client-owned CRM cleanup or inbox-to-CRM automation as a service.",
                    "Sell a research brief or directory built from public business information instead of personal emails.",
                ]
            )

        if touches_mailbox and has_harvest_behavior and not owner_authorized_flag:
            hard_failures.append(
                "Mailbox or Gmail extraction requires explicit owner authorization."
            )
            alternatives.append(
                "Restrict mailbox use to owner-authorized search, summarization, and internal routing."
            )

        if has_outreach_behavior and (has_contact_resale or consent_bucket == "low"):
            hard_failures.append(
                "Mass outreach tied to purchased, scraped, or non-consensual contacts is not allowed."
            )
            alternatives.append(
                "Use first-party opt-in newsletters, waitlists, or lead magnets for outreach."
            )

        if consent_bucket == "low":
            hard_failures.append("Consent quality is low or undefined.")
        elif consent_bucket != "high":
            hard_holds.append("Consent quality is not yet clearly high.")

        if provenance_bucket == "low":
            hard_failures.append("Data provenance is low or undocumented.")
        elif provenance_bucket != "high":
            hard_holds.append("Data provenance is not yet clearly high.")

        if platform_bucket == "low":
            hard_failures.append("Platform rules or terms appear unknown or conflicting.")
        elif platform_bucket != "high":
            hard_holds.append("Platform rules have not been clearly documented.")

        if touches_mailbox and owner_authorized_flag and not has_contact_resale:
            alternatives.append(
                "Keep mailbox RAG limited to internal search, summarization, triage, and CRM sync for the owner."
            )

        if not alternatives:
            alternatives = [
                "Client-owned inbox to CRM automation",
                "Autonomous listing services",
                "Public-data research products",
                "Opt-in demand capture systems",
                "Commissioned workflow automation for paying clients",
            ]

        if hard_failures:
            decision = "REJECT"
            summary = "The plan fails one or more legality, consent, provenance, or privacy gates."
        elif hard_holds:
            decision = "HOLD"
            summary = "The plan may be viable, but key compliance details are still incomplete."
        else:
            decision = "PASS"
            summary = "The plan clears the basic compliance screen and can move to strategy scoring."

        unique_alternatives = []
        for item in alternatives:
            if item not in unique_alternatives:
                unique_alternatives.append(item)

        lines = [
            f"Decision: {decision}",
            f"Summary: {summary}",
        ]

        if hard_failures:
            lines.append("")
            lines.append("Hard failures:")
            for item in hard_failures:
                lines.append(f"- {item}")

        if hard_holds:
            lines.append("")
            lines.append("Hold reasons:")
            for item in hard_holds:
                lines.append(f"- {item}")

        lines.append("")
        lines.append("Recommended compliant lanes:")
        for item in unique_alternatives:
            lines.append(f"- {item}")

        lines.append("")
        lines.append("Next step:")
        if decision == "PASS":
            lines.append(
                "- Score the lane with instruments/strategy/score.sh before activation."
            )
        else:
            lines.append(
                "- Convert the plan to a permissioned lane, then rerun revenue_planning."
            )

        return Response(message="\n".join(lines), break_loop=False)
