import json
import re

from python.helpers.tool import Response, Tool


DISALLOWED_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"\b(sell|broker|rent|trade|monetize)\b.{0,30}\b(email|contact|lead)\s+lists?\b",
            re.IGNORECASE,
        ),
        "Personal email or contact-list brokerage is not allowed.",
    ),
    (
        re.compile(
            r"\b(scrape|harvest|extract|pull|compile)\b.{0,30}\b(email|emails|contacts|gmail|inbox)\b",
            re.IGNORECASE,
        ),
        "Harvesting emails or inbox data is not allowed.",
    ),
    (
        re.compile(r"\b(cold email|spam|mass unsolicited|bulk outreach)\b", re.IGNORECASE),
        "Spam or mass unsolicited outreach is not allowed.",
    ),
    (
        re.compile(r"\b(buy|purchase)\b.{0,20}\b(email|lead|contact)\b", re.IGNORECASE),
        "Buying third-party contact data is not allowed.",
    ),
    (
        re.compile(r"\b(gmail|google email|workspace email)\b", re.IGNORECASE),
        "Access to inbox content requires explicit user authorization and cannot be used for data brokerage.",
    ),
]

GOOD_CONSENT_TERMS = (
    "opt-in",
    "consent",
    "first-party",
    "customer provided",
    "user provided",
    "subscriber",
    "newsletter signup",
    "double opt-in",
    "explicit permission",
)

BAD_CONSENT_TERMS = (
    "scraped",
    "harvested",
    "purchased",
    "third-party list",
    "cold outreach",
    "gmail dump",
    "inbox export",
    "unknown",
    "unclear",
)

LOW_RISK_CHANNELS = (
    "seo",
    "content",
    "referrals",
    "marketplace",
    "newsletter",
    "community",
    "affiliate",
    "partnership",
)

HIGH_RISK_CHANNELS = (
    "cold email",
    "spam",
    "mass dm",
    "scraping",
    "bot outreach",
    "purchased list",
)

LANE_LIBRARY: list[tuple[tuple[str, ...], dict[str, str]]] = [
    (
        ("agent", "automation", "workflow", "service", "consulting"),
        {
            "lane": "productized automation service",
            "why": "Owned automation capability is usually easiest to monetize through a scoped service or retainer.",
            "next_step": "Package one repeatable workflow with a fixed deliverable, price, and case-study style proof.",
        },
    ),
    (
        ("software", "app", "tool", "dashboard", "saas"),
        {
            "lane": "subscription software",
            "why": "Existing software assets can support recurring revenue with low marginal cost.",
            "next_step": "Define a narrow paid use case, onboarding path, and acquisition channel before adding growth automation.",
        },
    ),
    (
        ("content", "research", "report", "guide", "newsletter", "audience"),
        {
            "lane": "audience monetization",
            "why": "Owned content and trust-based distribution are compatible with affiliate, sponsorship, and premium content models.",
            "next_step": "Create an opt-in lead magnet, publish one authority asset, and route signups into a compliant newsletter or CRM.",
        },
    ),
    (
        ("template", "dataset", "playbook", "course", "ebook"),
        {
            "lane": "digital products",
            "why": "Reusable digital assets can be sold repeatedly without relying on personal-data exploitation.",
            "next_step": "Turn one proven internal workflow into a paid template, checklist, or micro-course.",
        },
    ),
]

FALLBACK_LANES = [
    {
        "lane": "opt-in newsletter plus lead magnet",
        "why": "Build first-party demand before any automated sales workflow.",
        "next_step": "Offer a free useful asset and collect explicit consent before any follow-up communication.",
    },
    {
        "lane": "service marketplace listing",
        "why": "Marketplace demand reduces the need for risky outbound tactics.",
        "next_step": "Create a narrow offer and publish it on a platform with built-in buyer intent.",
    },
]


def _joined_text(*parts: str) -> str:
    return " ".join(part.strip() for part in parts if part and part.strip())


def _find_disallowed_reasons(text: str) -> list[str]:
    reasons: list[str] = []
    for pattern, message in DISALLOWED_PATTERNS:
        if pattern.search(text) and message not in reasons:
            reasons.append(message)
    return reasons


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _consent_state(consent_status: str) -> str:
    lowered = consent_status.lower()
    if _contains_any(lowered, BAD_CONSENT_TERMS):
        return "insufficient"
    if _contains_any(lowered, GOOD_CONSENT_TERMS):
        return "sufficient"
    return "unknown"


def _channel_state(channels: str) -> str:
    lowered = channels.lower()
    if _contains_any(lowered, HIGH_RISK_CHANNELS):
        return "high_risk"
    if _contains_any(lowered, LOW_RISK_CHANNELS):
        return "low_risk"
    return "unknown"


def _recommended_lanes(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    lanes: list[dict[str, str]] = []
    for keywords, lane in LANE_LIBRARY:
        if any(keyword in lowered for keyword in keywords):
            lanes.append(lane)
    if not lanes:
        lanes.extend(FALLBACK_LANES)
    return lanes[:3]


class RevenuePlanning(Tool):
    async def execute(
        self,
        proposal: str = "",
        assets: str = "",
        consent_status: str = "",
        channels: str = "",
        notes: str = "",
        **kwargs,
    ) -> Response:
        combined = _joined_text(proposal, assets, consent_status, channels, notes)
        lowered = combined.lower()
        reject_reasons = _find_disallowed_reasons(lowered)

        if reject_reasons:
            result = {
                "decision": "reject",
                "summary": "Rejected because the plan depends on privacy-invasive, non-consensual, or non-compliant monetization tactics.",
                "reasons": reject_reasons,
                "allowed_alternatives": [
                    "Build an opt-in newsletter or CRM from user-provided signups.",
                    "Sell a digital product, software tool, or productized service.",
                    "Monetize first-party content via affiliate offers, sponsorships, or premium reports.",
                ],
                "required_guardrails": [
                    "Use only first-party or explicitly licensed data.",
                    "Collect explicit consent before retaining or contacting individuals.",
                    "Avoid inbox scraping, contact-list resale, and unsolicited bulk outreach.",
                ],
            }
            return Response(message=json.dumps(result, indent=2), break_loop=False)

        consent_state = _consent_state(consent_status)
        channel_state = _channel_state(channels)
        lanes = _recommended_lanes(_joined_text(proposal, assets, channels))

        decision = "pass"
        blockers: list[str] = []

        if not proposal.strip():
            decision = "hold"
            blockers.append("Define a concrete offer before building automation around it.")
        if consent_state != "sufficient":
            decision = "hold"
            blockers.append(
                "Clarify that every contact or dataset is first-party, opt-in, or otherwise explicitly licensed."
            )
        if channel_state == "high_risk":
            decision = "hold"
            blockers.append("Replace risky outreach channels with platform-compliant acquisition channels.")

        score = 60
        if consent_state == "sufficient":
            score += 20
        if channel_state == "low_risk":
            score += 10
        if proposal.strip() and lanes:
            score += 10
        if decision == "hold":
            score -= 25

        result = {
            "decision": decision,
            "score": max(0, min(score, 100)),
            "summary": (
                "Viable as a compliance-first revenue workflow."
                if decision == "pass"
                else "Promising, but missing consent, channel, or offer clarity required for a compliant launch."
            ),
            "recommended_lanes": lanes,
            "blockers": blockers,
            "required_guardrails": [
                "Use first-party or explicitly licensed data only.",
                "Keep audit trails for consent, source provenance, and outbound messaging rules.",
                "Favor inbound demand, marketplaces, SEO, referrals, and opt-in lifecycle messaging over cold outreach.",
            ],
            "next_actions": [
                "Choose one lane and define a concrete paid offer.",
                "Document approved data sources and consent status before ingestion or outreach.",
                "Build automation only after the acquisition channel and compliance checks are explicit.",
            ],
        }
        return Response(message=json.dumps(result, indent=2), break_loop=False)
