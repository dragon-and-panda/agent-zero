import json

from python.helpers.tool import Response, Tool


RISKY_KEYWORDS = {
    "email list",
    "email lists",
    "gmail",
    "inbox scraping",
    "contact scraping",
    "lead database resale",
    "sell leads",
    "buy leads",
    "personal data",
    "broker data",
    "data broker",
    "cold email blast",
    "scrape emails",
    "harvest emails",
}

SAFE_LANES = [
    {
        "lane": "consent-based lead capture",
        "why_it_fits": "Build landing pages, directories, or tools where users explicitly opt in to updates or quotes.",
    },
    {
        "lane": "client-owned inbox to CRM automation",
        "why_it_fits": "Process only inboxes and contacts the client already controls, with documented authorization.",
    },
    {
        "lane": "productized research",
        "why_it_fits": "Sell market maps, lead scoring, vendor intelligence, or industry monitoring without transferring personal contact data.",
    },
    {
        "lane": "done-for-you outbound infrastructure",
        "why_it_fits": "Create compliant outreach systems, copy, and routing for clients using their own lawful, opt-in data.",
    },
    {
        "lane": "listing and marketplace operations",
        "why_it_fits": "Monetize by creating, optimizing, and managing listings rather than brokering personal data.",
    },
]


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        opportunity: str = "",
        consent_status: str = "",
        data_source: str = "",
        platform: str = "",
        notes: str = "",
        **kwargs,
    ):
        mission_text = " ".join(
            part for part in [mission, opportunity, notes, data_source, platform] if part
        ).lower()

        concerns = [
            keyword for keyword in sorted(RISKY_KEYWORDS) if keyword in mission_text
        ]

        consent = (consent_status or "").strip().lower()
        source = (data_source or "").strip().lower()
        platform_name = (platform or "").strip()

        hard_fail_reasons = []
        if concerns:
            hard_fail_reasons.append(
                "Request appears to involve personal-data harvesting, inbox scraping, or contact-list resale."
            )
        if source and any(
            token in source
            for token in ["gmail", "inbox", "email", "contacts", "scraped", "third-party"]
        ) and consent not in {"opt-in", "client-owned", "documented", "yes"}:
            hard_fail_reasons.append(
                "Data source references email or inbox data without clear documented consent."
            )

        status = "redirect"
        if not hard_fail_reasons and consent in {"opt-in", "client-owned", "documented", "yes"}:
            status = "proceed_with_compliance_checks"

        response = {
            "status": status,
            "mission": mission,
            "opportunity": opportunity,
            "platform": platform_name,
            "hard_fail_reasons": hard_fail_reasons,
            "required_checks": [
                "Verify the revenue path is legal in the target jurisdiction.",
                "Confirm clear consent and lawful provenance for any personal data.",
                "Check platform terms and anti-spam rules before execution.",
                "Prefer first-party acquisition, client-owned data, or non-personal-data products.",
            ],
            "recommended_safe_lanes": SAFE_LANES,
            "next_step": (
                "Rewrite the idea as a compliant lane and score it with /workspace/instruments/strategy/score.sh."
                if hard_fail_reasons
                else "Score the lane with /workspace/instruments/strategy/score.sh and document it in docs/strategy/incoming.md."
            ),
        }

        return Response(
            message=json.dumps(response, indent=2, ensure_ascii=False),
            break_loop=False,
        )
