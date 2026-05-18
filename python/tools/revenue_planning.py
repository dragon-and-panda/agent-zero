import json

from python.helpers.tool import Response, Tool

EMAIL_LIST_KEYWORDS = (
    "sell email list",
    "sell email lists",
    "selling email list",
    "selling email lists",
    "broker email list",
    "broker email lists",
    "resell contact list",
    "resell contact lists",
    "email brokerage",
    "contact brokerage",
    "lead list resale",
)

HARVESTING_KEYWORDS = (
    "scrape emails",
    "scrape email",
    "extract emails",
    "extract email addresses",
    "harvest emails",
    "harvest contacts",
    "compile email list",
    "compile email lists",
    "gmail scraping",
    "inbox scraping",
)

SPAM_KEYWORDS = (
    "bulk cold email",
    "cold email blast",
    "mass outreach",
    "email blast",
    "unsolicited outreach",
    "spam campaign",
)

INBOX_KEYWORDS = (
    "gmail",
    "google email",
    "mailbox",
    "inbox",
    "email threads",
    "email data",
)

AUTHORIZED_KEYWORDS = (
    "authorized",
    "authorised",
    "owner",
    "consented",
    "explicit permission",
    "opt-in",
    "opt in",
    "first-party",
    "first party",
)

SAFE_LANE_HINTS = {
    "opt_in_audience": ("newsletter", "community", "waitlist", "subscriber", "opt-in"),
    "productized_service": ("service", "agency", "done-for-you", "automation setup"),
    "software": ("software", "saas", "tool", "workflow", "assistant"),
    "affiliate": ("affiliate", "referral", "sponsorship", "sponsor"),
}


def _normalize(*parts: str) -> str:
    return " ".join(part.strip().lower() for part in parts if part and part.strip())


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _collect_safe_lanes(text: str) -> list[str]:
    lanes: list[str] = []
    for lane, keywords in SAFE_LANE_HINTS.items():
        if _contains_any(text, keywords):
            lanes.append(lane)
    return lanes


class RevenuePlanning(Tool):
    async def execute(
        self,
        venture_summary: str = "",
        data_sources: str = "",
        customer_acquisition: str = "",
        automation_plan: str = "",
        authorization_status: str = "",
        monetization_goal: str = "",
        **kwargs,
    ):
        combined = _normalize(
            venture_summary,
            data_sources,
            customer_acquisition,
            automation_plan,
            authorization_status,
            monetization_goal,
        )
        auth_text = _normalize(authorization_status, data_sources)

        blocking_issues: list[str] = []
        required_controls: list[str] = []
        safe_reframe: list[str] = []
        detected_patterns: list[str] = []

        sells_email_lists = _contains_any(combined, EMAIL_LIST_KEYWORDS)
        harvests_contacts = _contains_any(combined, HARVESTING_KEYWORDS)
        spam_pattern = _contains_any(combined, SPAM_KEYWORDS)
        touches_inbox = _contains_any(combined, INBOX_KEYWORDS)
        has_clear_authorization = _contains_any(auth_text, AUTHORIZED_KEYWORDS)
        safe_lanes = _collect_safe_lanes(combined)

        if sells_email_lists:
            detected_patterns.append("email_list_resale")
            blocking_issues.append(
                "Selling or brokering email lists is not an allowed monetization path."
            )
            safe_reframe.extend(
                [
                    "Build an opt-in newsletter and monetize with sponsorships or affiliates.",
                    "Offer a paid service or software workflow instead of trading contacts.",
                ]
            )

        if harvests_contacts:
            detected_patterns.append("contact_harvesting")
            blocking_issues.append(
                "Contact harvesting from inboxes or files is not allowed without a narrow, authorized operational purpose."
            )
            safe_reframe.extend(
                [
                    "Use first-party forms, waitlists, or explicit partner submissions.",
                    "Use mailbox data only for the owner's internal search, tagging, and reply workflows.",
                ]
            )

        if spam_pattern:
            detected_patterns.append("bulk_unsolicited_outreach")
            blocking_issues.append(
                "Bulk unsolicited outreach creates anti-spam and platform abuse risk."
            )
            safe_reframe.append(
                "Prefer inbound, opt-in, or manually reviewed partnership outreach."
            )

        if touches_inbox and not has_clear_authorization:
            detected_patterns.append("unclear_inbox_authorization")
            required_controls.append(
                "Document explicit mailbox owner authorization and limit scopes before any inbox ingestion."
            )

        if touches_inbox and has_clear_authorization:
            detected_patterns.append("authorized_inbox_workflow")
            required_controls.extend(
                [
                    "Use minimum required Gmail or mailbox scopes.",
                    "Store summaries, tags, and embeddings instead of broad raw exports.",
                    "Do not turn mailbox contacts into resale or blast lists.",
                ]
            )

        if not venture_summary.strip():
            required_controls.append("Provide a concrete venture_summary before execution.")

        if not monetization_goal.strip():
            required_controls.append("Define a clear monetization_goal.")

        if not customer_acquisition.strip():
            required_controls.append("Describe a customer acquisition path and consent model.")

        if blocking_issues:
            decision = "REJECT"
        elif required_controls:
            decision = "HOLD"
        else:
            decision = "PASS"

        if not safe_lanes:
            safe_lanes = [
                "productized_service",
                "opt_in_audience",
                "software",
            ]

        result = {
            "decision": decision,
            "venture_summary": venture_summary,
            "detected_patterns": detected_patterns,
            "blocking_issues": blocking_issues,
            "required_controls": required_controls,
            "recommended_safe_lanes": safe_lanes,
            "safe_reframe": safe_reframe,
        }

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=True),
            break_loop=False,
        )
