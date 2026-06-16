import json
from typing import Dict, List

from python.helpers.tool import Response, Tool


SAFE_AUTHORIZATION_TERMS = [
    "authorized",
    "authorised",
    "opt-in",
    "opt in",
    "consent",
    "consented",
    "first-party",
    "first party",
    "client-owned",
    "client owned",
    "client-authorized",
    "client authorized",
    "operator-owned",
    "operator owned",
    "internal crm",
    "customer-owned",
    "customer owned",
]

PERSONAL_DATA_TERMS = [
    "email list",
    "email lists",
    "email address",
    "email addresses",
    "contact list",
    "contact lists",
    "gmail",
    "google email",
    "mailbox",
    "inbox",
    "lead list",
    "leads database",
]

RESALE_TERMS = [
    "sell",
    "resell",
    "broker",
    "rent",
    "trade",
    "marketplace for leads",
]

UNAUTHORIZED_ACCESS_TERMS = [
    "scrape",
    "harvest",
    "bypass",
    "captcha",
    "rate limit",
    "without permission",
    "without consent",
]


def contains_any(text: str, phrases: List[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def infer_lane(text: str) -> str:
    if contains_any(text, ["crm", "mailbox", "inbox", "gmail", "google workspace"]):
        return "authorized inbox-to-crm"
    if contains_any(text, ["listing", "marketplace", "mercari", "craigslist", "nextdoor"]):
        return "autonomous listing service"
    return "research product or workflow automation"


def infer_soft_scores(lane: str) -> Dict[str, str]:
    if lane == "authorized inbox-to-crm":
        return {
            "time": "high",
            "margin": "medium",
            "repeatability": "high",
            "automation": "high",
            "defensibility": "medium",
        }
    if lane == "autonomous listing service":
        return {
            "time": "medium",
            "margin": "medium",
            "repeatability": "medium",
            "automation": "medium",
            "defensibility": "medium",
        }
    return {
        "time": "medium",
        "margin": "high",
        "repeatability": "high",
        "automation": "high",
        "defensibility": "medium",
    }


def build_report(
    mission: str,
    assets: str = "",
    data_sources: str = "",
    monetization: str = "",
    constraints: str = "",
) -> Dict[str, object]:
    text = " ".join([mission, assets, data_sources, monetization, constraints]).lower()
    hard_failures: Dict[str, str] = {}
    hard_gates = {
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "tos": "high",
    }

    mentions_personal_data = contains_any(text, PERSONAL_DATA_TERMS)
    mentions_resale = contains_any(text, RESALE_TERMS)
    mentions_unsafe_access = contains_any(text, UNAUTHORIZED_ACCESS_TERMS)
    has_authorization_signal = contains_any(text, SAFE_AUTHORIZATION_TERMS)

    if mentions_personal_data and mentions_resale:
        hard_failures["personal_data_resale"] = (
            "Personal email/contact data cannot be packaged for sale or brokerage."
        )
        hard_gates["legality"] = "low"
        hard_gates["consent"] = "low"
        hard_gates["provenance"] = "low"

    if contains_any(text, ["gmail", "google email", "mailbox", "inbox"]) and not has_authorization_signal:
        hard_failures["unauthorized_or_unclear_inbox_access"] = (
            "Inbox processing requires explicit ownership or delegated authority."
        )
        hard_gates["consent"] = "low"
        hard_gates["provenance"] = "low"

    if mentions_personal_data and mentions_unsafe_access:
        hard_failures["nonconsensual_collection"] = (
            "Scraping or harvesting personal contact data is not an acceptable acquisition method."
        )
        hard_gates["legality"] = "low"
        hard_gates["tos"] = "low"

    if contains_any(text, ["bypass tos", "break tos", "ignore tos", "rate limit bypass", "captcha"]):
        hard_failures["terms_of_service_conflict"] = (
            "Plans that depend on bypassing platform controls or terms are rejected."
        )
        hard_gates["tos"] = "low"

    if not hard_failures and mentions_personal_data and not has_authorization_signal:
        hard_gates["consent"] = "medium"
        hard_gates["provenance"] = "medium"

    lane = infer_lane(text)
    soft_scores = infer_soft_scores(lane)
    soft_high = sum(1 for value in soft_scores.values() if value == "high")
    soft_low = sum(1 for value in soft_scores.values() if value == "low")

    verdict = "HOLD"
    verdict_reason = "Compliant direction exists, but the lane needs sharper scope or stronger evidence."
    if hard_failures:
        verdict = "REJECT"
        verdict_reason = "One or more hard compliance gates failed."
    elif all(value == "high" for value in hard_gates.values()) and soft_low == 0 and soft_high >= 3:
        verdict = "PASS"
        verdict_reason = "Compliance gates are strong and the execution profile is attractive."

    compliant_pivots = [
        "authorized inbox-to-crm cleanup for operator-owned or client-authorized data",
        "opt-in newsletter or community operations built on first-party consent",
        "listing, research, or workflow-automation services that do not depend on personal-data resale",
    ]

    next_steps = [
        "Document data ownership, operator authority, and intended use before ingestion.",
        "Score the lane with instruments/strategy/score.sh using explicit legality and consent assumptions.",
        "Prefer subscription, setup-fee, or managed-service monetization over data resale.",
    ]

    if verdict == "REJECT":
        next_steps.insert(
            0,
            "Drop the current monetization path and pivot to a first-party, consent-based revenue lane.",
        )

    return {
        "mission": mission,
        "recommended_lane": lane,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "hard_gates": hard_gates,
        "hard_failures": hard_failures,
        "soft_scores": soft_scores,
        "summary": (
            "Use the framework to build revenue from authorized data operations, productized services, "
            "or internal automation. Do not monetize by selling harvested contact data."
        ),
        "compliant_pivots": compliant_pivots,
        "next_steps": next_steps,
    }


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        data_sources: str = "",
        monetization: str = "",
        constraints: str = "",
        **kwargs,
    ) -> Response:
        if not mission:
            return Response(
                message="Error: provide a mission to evaluate.",
                break_loop=False,
            )

        report = build_report(
            mission=mission,
            assets=assets,
            data_sources=data_sources,
            monetization=monetization,
            constraints=constraints,
        )
        return Response(
            message=json.dumps(report, indent=2, ensure_ascii=False),
            break_loop=False,
        )
