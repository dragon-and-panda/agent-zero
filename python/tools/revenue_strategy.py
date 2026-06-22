import json

from python.helpers.tool import Tool, Response

BLOCKED_SIGNALS = (
    "sell email list",
    "sell email lists",
    "email list resale",
    "resell email",
    "resell emails",
    "scrape emails",
    "harvest emails",
    "gmail data",
    "google email data",
    "private inbox",
    "data broker",
    "cold spam",
    "bulk unsolicited",
)

BLOCKED_TACTICS = [
    "Scraping or harvesting personal email addresses without clear consent",
    "Buying, selling, or reselling personal contact data",
    "Mining private inboxes or account data for commercialization",
    "Bulk unsolicited outreach or spam-driven growth loops",
    "Deceptive collection, impersonation, or privacy-invasive targeting",
]

SAFE_LEAD_SOURCES = [
    "Opt-in newsletter signups and lead magnets",
    "Inbound content funnels tied to a clear privacy notice",
    "Partnerships, referrals, and affiliate programs",
    "Public business contacts where outreach is relevant, limited, and compliant",
    "Customer interviews, communities, and waitlists with explicit consent",
]

SAFE_REVENUE_MODELS = [
    "Productized services",
    "Micro-SaaS or internal tooling sold as a subscription",
    "Affiliate content around tools with genuine fit",
    "Premium research or niche information products built from licensed or first-party data",
    "Lead generation based on opt-in forms, not resold contact lists",
]


class RevenueStrategy(Tool):
    async def execute(
        self,
        venture: str = "",
        market: str = "",
        goal: str = "",
        assets_json: str = "",
        constraints_json: str = "",
        **kwargs,
    ):
        assets, assets_error = _parse_json_object("assets_json", assets_json)
        if assets_error:
            return Response(message=assets_error, break_loop=False)

        constraints, constraints_error = _parse_json_object(
            "constraints_json", constraints_json
        )
        if constraints_error:
            return Response(message=constraints_error, break_loop=False)

        request_blob = " ".join(
            [
                venture,
                market,
                goal,
                json.dumps(assets, ensure_ascii=False),
                json.dumps(constraints, ensure_ascii=False),
            ]
        ).lower()

        if any(signal in request_blob for signal in BLOCKED_SIGNALS):
            return Response(
                message=json.dumps(
                    {
                        "verdict": "blocked",
                        "reason": (
                            "This request depends on personal-data harvesting, "
                            "private inbox access, or spam-prone list resale."
                        ),
                        "blocked_tactics": BLOCKED_TACTICS,
                        "safe_alternatives": SAFE_LEAD_SOURCES,
                        "suggested_revenue_models": SAFE_REVENUE_MODELS,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                break_loop=False,
            )

        system = (
            "You design legal, ethical internet business strategies for an autonomous agent.\n"
            "Output ONLY valid JSON.\n"
            "Return an object with keys:\n"
            "- verdict: string\n"
            "- opportunity_summary: string\n"
            "- revenue_models: array of objects with keys name, why_fit, first_offer\n"
            "- lead_sources: array of objects with keys source, acquisition_method, compliance_notes\n"
            "- automation_workflows: array of objects with keys workflow, stack, human_approval_gate\n"
            "- first_actions: array of short strings\n"
            "- metrics: array of short strings\n"
            "- compliance_checks: array of short strings\n"
            "- blocked_tactics: array of short strings\n"
            "Rules:\n"
            "- Do not propose buying, scraping, trading, or reselling personal data.\n"
            "- Do not propose spam, deception, impersonation, or privacy violations.\n"
            "- Prefer first-party audiences, opt-in capture, licensed/public business data with usage rights, content, affiliate, SaaS, and productized services.\n"
            "- Keep the plan realistic for minimal human supervision and include explicit approval gates for risky actions.\n"
            "- Tailor recommendations to the provided assets and constraints.\n"
        )
        message = (
            f"venture: {venture or 'unspecified'}\n"
            f"market: {market or 'unspecified'}\n"
            f"goal: {goal or 'unspecified'}\n"
            f"assets_json: {json.dumps(assets, ensure_ascii=False)}\n"
            f"constraints_json: {json.dumps(constraints, ensure_ascii=False)}\n"
            f"default_blocked_tactics: {json.dumps(BLOCKED_TACTICS, ensure_ascii=False)}\n"
        )

        try:
            out = await self.agent.call_utility_model(
                system=system, message=message, background=False
            )
            data = json.loads(out)
        except Exception as e:
            return Response(
                message=f"Failed to generate revenue strategy: {e}", break_loop=False
            )

        if not isinstance(data, dict):
            return Response(
                message="Revenue strategy model output was not a JSON object.",
                break_loop=False,
            )

        data.setdefault("verdict", "approved")
        data.setdefault("blocked_tactics", BLOCKED_TACTICS)
        return Response(
            message=json.dumps(data, ensure_ascii=False, indent=2), break_loop=False
        )


def _parse_json_object(field_name: str, raw: str) -> tuple[dict, str | None]:
    if not raw:
        return {}, None

    try:
        data = json.loads(raw)
    except Exception as e:
        return {}, f"Invalid {field_name}: {e}"

    if not isinstance(data, dict):
        return {}, f"{field_name} must be a JSON object."

    return data, None
