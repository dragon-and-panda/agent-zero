import json
import re

from python.helpers.tool import Tool, Response


PROHIBITED_RULES = {
    "personal_data_brokerage": [
        r"\b(email|contact|lead)\s+list(s)?\b",
        r"\b(sell|broker|rent|trade|resell)\b.{0,40}\b(email|contact|lead)(s)?\b",
        r"\bdata brokerage\b",
    ],
    "unauthorized_inbox_extraction": [
        r"\b(gmail|google workspace|inbox|mailbox|email archive)\b.{0,50}\b(extract|harvest|dump|compile|export|scrape)\b",
        r"\b(extract|harvest|dump|compile|export|scrape)\b.{0,50}\b(gmail|google workspace|inbox|mailbox|email archive)\b",
    ],
    "spam_or_unsolicited_outreach": [
        r"\bspam\b",
        r"\bcold email blast\b",
        r"\bunsolicited bulk outreach\b",
        r"\bpurchased list\b",
    ],
}

REVIEW_RULES = {
    "email_data_requires_authority": [
        r"\b(gmail|google workspace|inbox|mailbox|email)\b",
    ],
    "outbound_channels_need_policy_review": [
        r"\boutreach\b",
        r"\blead generation\b",
    ],
}

DEFAULT_ALTERNATIVES = [
    "Build opt-in lead capture flows such as demos, newsletters, waitlists, or lead magnets.",
    "Use first-party inbox analysis only for support, billing, FAQ extraction, and warm inbound opportunity triage.",
    "Package a productized service that can be sold from owned channels with clear customer consent.",
    "Monetize owned or authorized inventory through compliant marketplace listings.",
    "Create digital products or research assets from original work instead of reselling contact data.",
]


def _parse_list_arg(value: str) -> list[str]:
    if not value:
        return []

    stripped = value.strip()
    if not stripped:
        return []

    if stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass

    parts = re.split(r"[\n,;]+", stripped)
    return [part.strip() for part in parts if part.strip()]


def _collect_matches(text: str, rules: dict[str, list[str]]) -> list[str]:
    matches: list[str] = []
    for label, patterns in rules.items():
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                matches.append(label)
                break
    return matches


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        data_sources: str = "",
        monetization_paths: str = "",
        constraints: str = "",
        **kwargs,
    ):
        parsed_assets = _parse_list_arg(assets)
        parsed_data_sources = _parse_list_arg(data_sources)
        parsed_monetization_paths = _parse_list_arg(monetization_paths)
        parsed_constraints = _parse_list_arg(constraints)

        combined_text = "\n".join(
            [
                mission,
                "\n".join(parsed_assets),
                "\n".join(parsed_data_sources),
                "\n".join(parsed_monetization_paths),
                "\n".join(parsed_constraints),
            ]
        )

        blocked = _collect_matches(combined_text, PROHIBITED_RULES)
        warnings = _collect_matches(combined_text, REVIEW_RULES)

        if blocked:
            decision = "REJECT"
        elif warnings:
            decision = "HOLD"
        else:
            decision = "PASS"

        next_steps = [
            "Document legal basis, permissions, and platform constraints before execution.",
            "Prefer first-party or clearly authorized data sources over third-party contact data.",
            "Track the opportunity in /workspace/docs/strategy/incoming.md with a PASS/HOLD/REJECT decision.",
        ]

        if decision == "REJECT":
            summary = (
                "The proposed revenue plan depends on prohibited behavior such as personal-data brokerage, "
                "unauthorized inbox extraction, or spam-like outreach."
            )
            next_steps = [
                "Remove any plan to extract, package, sell, rent, or broker personal contact data.",
                "Rewrite the workflow around first-party, opt-in, or clearly authorized business data.",
                "Choose one of the safe alternatives and rescore the opportunity.",
            ]
        elif decision == "HOLD":
            summary = (
                "The plan may be viable, but it touches sensitive channels or monetization paths that require "
                "clear authority, data minimization, and policy review."
            )
            next_steps = [
                "Confirm authority over every inbox, file set, or platform account involved.",
                "Define retention, field-level minimization, and approved uses for any email-derived data.",
                "Rescope toward opt-in demand capture, inbound triage, or owned-channel monetization if needed.",
            ]
        else:
            summary = (
                "The plan is compatible with a compliance-first revenue system based on original value creation "
                "and authorized data use."
            )
            next_steps = [
                "Prioritize the opportunity with the strategy scoring instrument.",
                "Define success metrics for revenue, margin, automation coverage, and compliance health.",
                "Ship the smallest compliant experiment that can validate demand.",
            ]

        email_specific_alternatives: list[str] = []
        if re.search(r"\b(gmail|google workspace|inbox|mailbox|email)\b", combined_text, flags=re.IGNORECASE):
            email_specific_alternatives = [
                "Analyze an authorized business inbox for invoices, renewals, support themes, or warm inbound requests.",
                "Use inbox retrieval to build internal FAQs, response templates, and CRM follow-up queues instead of lists for sale.",
            ]

        response = {
            "mission": mission or "unspecified mission",
            "decision": decision,
            "summary": summary,
            "blocked_reasons": blocked,
            "review_flags": warnings,
            "assets": parsed_assets,
            "data_sources": parsed_data_sources,
            "monetization_paths": parsed_monetization_paths,
            "constraints": parsed_constraints,
            "safe_alternatives": _dedupe(email_specific_alternatives + DEFAULT_ALTERNATIVES),
            "next_steps": next_steps,
            "references": [
                "/workspace/docs/policies/compliance_pack.md",
                "/workspace/docs/programs/agentic_financial_system/charter.md",
                "/workspace/docs/strategy/incoming.md",
                "/workspace/instruments/strategy/score.sh",
            ],
        }

        return Response(message=json.dumps(response, indent=2), break_loop=False)
