from __future__ import annotations

from dataclasses import dataclass
from typing import Any


LEVELS = {"low", "medium", "high"}
HARD_FACTORS = ("legality", "consent", "provenance", "platform")
SOFT_FACTORS = (
    "time_to_cash",
    "margin",
    "repeatability",
    "automation",
    "defensibility",
)

REJECT_PATTERNS = {
    "personal_data_resale": (
        "sell email list",
        "sell email lists",
        "email list brokerage",
        "contact list brokerage",
        "broker emails",
        "data broker",
    ),
    "non_consensual_inbox": (
        "gmail",
        "inbox scraping",
        "scrape inbox",
        "mailbox scraping",
        "harvest emails",
        "extract emails from inbox",
    ),
    "spam_or_evasion": (
        "spam",
        "mass unsolicited",
        "bypass captcha",
        "bypass rate limit",
        "evade platform",
    ),
}

HOLD_PATTERNS = {
    "regulated_finance": (
        "trading",
        "securities",
        "investment advice",
        "lending",
        "underwriting",
    ),
}


@dataclass
class FactorResult:
    level: str
    note: str


def normalize_level(value: Any, default: str = "medium") -> str:
    candidate = str(value or default).strip().lower()
    if candidate not in LEVELS:
        return default
    return candidate


def _collect_text(payload: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("idea", "assets", "data_sources", "customer", "outreach_method", "notes"):
        value = payload.get(key, "")
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        else:
            values.append(str(value))
    return " ".join(values).lower()


def _detect_pattern_hits(text: str, patterns: dict[str, tuple[str, ...]]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for label, keywords in patterns.items():
        matches = [keyword for keyword in keywords if keyword in text]
        if matches:
            hits[label] = matches
    return hits


def score_lane(
    legality: Any,
    consent: Any,
    provenance: Any,
    platform: Any,
    time_to_cash: Any,
    margin: Any,
    repeatability: Any,
    automation: Any,
    defensibility: Any,
) -> dict[str, Any]:
    hard = {
        "legality": normalize_level(legality),
        "consent": normalize_level(consent),
        "provenance": normalize_level(provenance),
        "platform": normalize_level(platform),
    }
    soft = {
        "time_to_cash": normalize_level(time_to_cash),
        "margin": normalize_level(margin),
        "repeatability": normalize_level(repeatability),
        "automation": normalize_level(automation),
        "defensibility": normalize_level(defensibility),
    }

    failed_hard = [name for name, level in hard.items() if level == "low"]
    medium_hard = [name for name, level in hard.items() if level == "medium"]
    low_soft = [name for name, level in soft.items() if level == "low"]
    high_soft_count = sum(1 for level in soft.values() if level == "high")

    verdict = "HOLD"
    summary = "Compliant lane needs stronger evidence or economics."

    if failed_hard:
        verdict = "REJECT"
        summary = f"Hard gate failure: {', '.join(failed_hard)}."
    elif medium_hard:
        verdict = "HOLD"
        summary = f"Hard gates not fully cleared: {', '.join(medium_hard)}."
    elif low_soft:
        verdict = "HOLD"
        summary = f"Commercial weakness detected in: {', '.join(low_soft)}."
    elif high_soft_count >= 3:
        verdict = "PASS"
        summary = "All hard gates are clear and commercial quality is strong enough to activate."

    return {
        "verdict": verdict,
        "summary": summary,
        "hard_factors": hard,
        "soft_factors": soft,
        "high_soft_count": high_soft_count,
    }


def evaluate_revenue_plan(payload: dict[str, Any]) -> dict[str, Any]:
    text = _collect_text(payload)
    reject_hits = _detect_pattern_hits(text, REJECT_PATTERNS)
    hold_hits = _detect_pattern_hits(text, HOLD_PATTERNS)

    hard_overrides = {
        "legality": payload.get("legality", "medium"),
        "consent": payload.get("consent", "medium"),
        "provenance": payload.get("provenance", "medium"),
        "platform": payload.get("platform", "medium"),
    }
    soft_overrides = {
        "time_to_cash": payload.get("time_to_cash", "medium"),
        "margin": payload.get("margin", "medium"),
        "repeatability": payload.get("repeatability", "medium"),
        "automation": payload.get("automation", "medium"),
        "defensibility": payload.get("defensibility", "medium"),
    }

    reasons: list[str] = []
    required_changes: list[str] = []
    alternatives: list[str] = [
        "opt-in lead generation funnel with a clear value exchange",
        "client-authorized CRM hygiene or segmentation on first-party exports",
        "research or intelligence products based on public business information",
        "listing, operations, or workflow automation services sold as software or retainers",
    ]

    if reject_hits:
        verdict = "REJECT"
        reasons.append("Plan includes prohibited patterns such as personal-data resale, non-consensual inbox use, or spam/evasion tactics.")
        for factor in HARD_FACTORS:
            if factor in ("legality", "consent", "provenance", "platform"):
                hard_overrides[factor] = "low"
        required_changes.extend(
            [
                "remove any sale or brokerage of personal contact data",
                "replace inbox scraping or Gmail extraction with client-provided first-party exports only",
                "switch from unsolicited list monetization to a consent-based service or product",
            ]
        )
    else:
        verdict = "HOLD"

    if hold_hits and not reject_hits:
        reasons.append("Idea touches a regulated or high-liability domain and should stay on hold until controls are defined.")
        required_changes.append("document legal scope, customer disclosures, and risk controls before activation")

    scoring = score_lane(
        hard_overrides["legality"],
        hard_overrides["consent"],
        hard_overrides["provenance"],
        hard_overrides["platform"],
        soft_overrides["time_to_cash"],
        soft_overrides["margin"],
        soft_overrides["repeatability"],
        soft_overrides["automation"],
        soft_overrides["defensibility"],
    )

    if not reject_hits:
        verdict = scoring["verdict"]

    if not reasons:
        reasons.append(scoring["summary"])

    if verdict == "PASS":
        required_changes.extend(
            [
                "record customer permission, data provenance, and delivery metrics before launch",
                "start with a narrow offer and validate pricing with a real buyer",
            ]
        )
    elif verdict == "HOLD" and not required_changes:
        required_changes.extend(
            [
                "clarify who owns the data and how consent is captured",
                "strengthen the offer on margin, repeatability, or defensibility before activation",
            ]
        )

    return {
        "idea": payload.get("idea", ""),
        "verdict": verdict,
        "summary": reasons[0],
        "reasons": reasons,
        "required_changes": required_changes,
        "compliant_alternatives": alternatives,
        "pattern_hits": {"reject": reject_hits, "hold": hold_hits},
        "scoring": scoring,
    }
