import json
import re
from typing import Any

from python.helpers.tool import Response, Tool

FAIL = "fail"
PASS = "pass"
UNCLEAR = "unclear"

UNSAFE_PATTERNS = {
    "contact_resale": [
        r"\bemail lists?\b",
        r"\bcontact lists?\b",
        r"\bsell(?:ing)? compiled emails?\b",
        r"\bbroker(?:ing)? leads?\b",
        r"\brent(?:ing)? leads?\b",
    ],
    "unauthorized_mail_access": [
        r"\bscrap(?:e|ing)\b.*\b(gmail|inbox|email)\b",
        r"\bharvest(?:ing)?\b.*\b(emails?|contacts?)\b",
        r"\bgoogle email data\b",
        r"\bextract\b.*\bemail addresses\b",
    ],
    "spam_or_deception": [
        r"\bspam\b",
        r"\bmass cold email\b",
        r"\bundisclosed bulk messaging\b",
        r"\bimpersonat(?:e|ion)\b",
    ],
    "platform_evasion": [
        r"\bbypass\b.*\b(tos|terms|robots|rate limits?)\b",
        r"\bundetected\b.*\bscrap",
        r"\bcaptcha bypass\b",
    ],
}

PERSONAL_DATA_MARKERS = [
    "email",
    "gmail",
    "inbox",
    "contact",
    "lead list",
    "crm",
    "mailbox",
]

AUTHORIZED_CONSENT_MARKERS = [
    "opt-in",
    "opt in",
    "authorized",
    "user-owned",
    "user owned",
    "first-party",
    "first party",
    "customer-owned",
    "customer owned",
    "client-authorized",
    "client authorized",
    "existing customer",
]

UNCLEAR_PROVENANCE_MARKERS = [
    "unknown source",
    "unclear source",
    "scraped",
    "purchased list",
    "brokered data",
    "third-party list",
    "third party list",
]


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _collect_text(payload: dict[str, Any]) -> str:
    parts = []
    for key, value in payload.items():
        parts.append(f"{key}: {_normalize_text(value)}")
    return "\n".join(parts).lower()


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _has_personal_data(text: str) -> bool:
    return any(marker in text for marker in PERSONAL_DATA_MARKERS)


def _has_authorized_basis(text: str) -> bool:
    return any(marker in text for marker in AUTHORIZED_CONSENT_MARKERS)


def _lane_family(text: str) -> str:
    if "mailbox" in text or "inbox" in text or "crm" in text:
        return "inbox-to-crm"
    if "directory" in text or "listing" in text or "marketplace" in text:
        return "listing-operations"
    if "research" in text or "benchmark" in text or "report" in text:
        return "research-product"
    if "newsletter" in text or "waitlist" in text or "lead magnet" in text:
        return "opt-in-demand-gen"
    return "general-service"


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        lane_json: str = "",
        **kwargs: Any,
    ) -> Response:
        lane: dict[str, Any] = {}
        if lane_json:
            try:
                loaded = json.loads(lane_json)
            except json.JSONDecodeError as exc:
                return Response(
                    message=f"Invalid lane_json: {exc}",
                    break_loop=False,
                )
            if not isinstance(loaded, dict):
                return Response(
                    message="lane_json must decode to a JSON object.",
                    break_loop=False,
                )
            lane.update(loaded)

        if mission:
            lane.setdefault("mission", mission)
        lane.update({key: value for key, value in kwargs.items() if value not in (None, "")})

        if not lane:
            return Response(
                message="Provide mission text and/or lane_json describing the revenue idea.",
                break_loop=False,
            )

        text = _collect_text(lane)
        reasons: list[str] = []
        alternatives: list[str] = []

        legality = PASS
        consent = PASS
        provenance = PASS
        platform_fit = PASS

        for label, patterns in UNSAFE_PATTERNS.items():
            if _contains_any(text, patterns):
                legality = FAIL
                reasons.append(f"unsafe pattern detected: {label}")

        if any(marker in text for marker in UNCLEAR_PROVENANCE_MARKERS):
            provenance = FAIL
            reasons.append("data provenance is unclear or depends on scraped or brokered data")

        if _has_personal_data(text) and not _has_authorized_basis(text):
            consent = UNCLEAR
            reasons.append("personal-data use lacks an explicit authorized or opt-in basis")

        if "bypass" in text or "rate limit" in text or "robots" in text or "terms of service" in text:
            platform_fit = FAIL
            reasons.append("workflow conflicts with platform access or terms-of-service constraints")

        if legality == FAIL:
            alternatives.extend(
                [
                    "build an inbox-to-crm assistant for a user-owned or client-authorized mailbox",
                    "build public-source research products with provenance notes",
                    "build an opt-in funnel and CRM workflow instead of list brokerage",
                ]
            )

        hard_gates = {
            "legality": legality,
            "consent": consent,
            "provenance": provenance,
            "platform_fit": platform_fit,
        }

        if FAIL in hard_gates.values():
            outcome = "REJECT"
        elif UNCLEAR in hard_gates.values():
            outcome = "HOLD"
        else:
            outcome = "PASS"

        lane_family = _lane_family(text)
        if not alternatives and lane_family == "inbox-to-crm":
            alternatives.append("keep scope to authorized mailbox summarization, triage, and CRM sync")
        if not alternatives and lane_family == "research-product":
            alternatives.append("sell public-source benchmark packs or curated niche directories")
        if not alternatives and lane_family == "listing-operations":
            alternatives.append("focus on client-owned listing operations and directory maintenance")

        next_actions = [
            "document the buyer, offer, delivery, and data provenance in the mission brief",
            "score the lane with instruments/strategy/score.sh before activation",
            "write progress and stop conditions to docs/programs/agentic_financial_system/journal.md",
        ]
        if outcome != "REJECT":
            next_actions.insert(
                0,
                "confirm legality, consent, provenance, and platform fit before any automation touching personal data",
            )

        payload = {
            "outcome": outcome,
            "lane_family": lane_family,
            "hard_gates": hard_gates,
            "reasons": reasons,
            "recommended_alternatives": alternatives,
            "next_actions": next_actions,
        }
        return Response(message=json.dumps(payload, indent=2, ensure_ascii=True), break_loop=False)
