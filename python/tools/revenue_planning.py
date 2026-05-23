from __future__ import annotations

import re
from typing import Iterable

from python.helpers.tool import Tool, Response

VALID_LEVELS = {"low", "medium", "high"}
POSITIVE_HARD_FACTORS = ("legality", "consent", "provenance")
SOFT_FACTORS = (
    "time_to_cash",
    "margin",
    "repeatability",
    "automation",
    "defensibility",
)

RISK_PATTERNS = (
    (
        re.compile(
            r"\b(sell|broker|resell|rent|trade)\b.{0,40}\b(email|contact)\s+lists?\b",
            re.IGNORECASE,
        ),
        "Personal email or contact list brokerage is prohibited.",
    ),
    (
        re.compile(
            r"\b(scrape|harvest|compile|extract)\b.{0,40}\b(email|contact)\b.{0,40}\b(sell|broker|resell|rent|trade)\b",
            re.IGNORECASE,
        ),
        "Harvesting contact data for resale is prohibited.",
    ),
    (
        re.compile(
            r"\b(gmail|google mail|google email|mailbox|inbox)\b.{0,60}\b(sell|broker|resell|list brokerage)\b",
            re.IGNORECASE,
        ),
        "Mailbox access does not permit contact-list resale.",
    ),
    (
        re.compile(
            r"\b(spam|mass cold email|bulk cold outreach|unsolicited blast)\b",
            re.IGNORECASE,
        ),
        "Spam or consent-free outreach is not an acceptable acquisition strategy.",
    ),
    (
        re.compile(
            r"\b(bypass|evade|steal|unauthorized|credential stuffing|session hijack)\b",
            re.IGNORECASE,
        ),
        "Unauthorized access or control-evasion is prohibited.",
    ),
)


def normalize_level(value: str, default: str = "medium") -> str:
    normalized = (value or "").strip().lower()
    if normalized in VALID_LEVELS:
        return normalized
    return default


def collect_text(*values: str) -> str:
    return " ".join(value.strip() for value in values if value and value.strip())


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def detect_policy_violations(text: str) -> list[str]:
    violations: list[str] = []
    for pattern, message in RISK_PATTERNS:
        if pattern.search(text):
            violations.append(message)
    return dedupe(violations)


def factor_block(name: str, value: str) -> str:
    return f"- {name}: {value}"


def build_next_steps(verdict: str, hold_reasons: list[str], hard_failures: list[str]) -> list[str]:
    if verdict == "REJECT":
        return [
            "Do not execute the rejected lane.",
            "Replace it with an opt-in, first-party, or client-authorized workflow.",
            "Record the rejected idea and compliant replacement in docs/strategy/incoming.md.",
        ]

    if verdict == "HOLD":
        steps = [
            "Resolve the hard-factor uncertainty before launching the lane.",
            "Document data ownership, authorization scope, and platform constraints.",
            "Re-score the lane after the open questions are closed.",
        ]
        if hold_reasons:
            steps.append(f"Primary hold issue: {hold_reasons[0]}")
        return steps

    return [
        "Write an offer definition, target customer, and operating checklist.",
        "Launch a small, auditable pilot with explicit authorization and success metrics.",
        "Record results in the program journal before scaling.",
    ]


def build_safe_alternatives(text: str) -> list[str]:
    alternatives = [
        "first-party inbox-to-CRM automation for authorized accounts",
        "opt-in newsletter or lead-magnet funnels",
        "paid research briefs built from lawful public or licensed sources",
        "managed listing, sourcing, or response automation that follows platform rules",
    ]

    if re.search(r"\b(gmail|google mail|google email|mailbox|inbox)\b", text, re.IGNORECASE):
        alternatives.insert(0, "authorized mailbox summarization, task extraction, and CRM drafting without exporting or reselling contacts")

    return dedupe(alternatives)


def assess_revenue_plan(
    idea: str = "",
    customer: str = "",
    offer: str = "",
    acquisition: str = "",
    data_handling: str = "",
    legality: str = "",
    consent: str = "",
    provenance: str = "",
    platform_risk: str = "",
    time_to_cash: str = "",
    margin: str = "",
    repeatability: str = "",
    automation: str = "",
    defensibility: str = "",
    notes: str = "",
) -> str:
    combined_text = collect_text(
        idea,
        customer,
        offer,
        acquisition,
        data_handling,
        notes,
    )

    levels = {
        "legality": normalize_level(legality),
        "consent": normalize_level(consent),
        "provenance": normalize_level(provenance),
        "platform_risk": normalize_level(platform_risk),
        "time_to_cash": normalize_level(time_to_cash),
        "margin": normalize_level(margin),
        "repeatability": normalize_level(repeatability),
        "automation": normalize_level(automation),
        "defensibility": normalize_level(defensibility),
    }

    hard_failures = detect_policy_violations(combined_text)
    hold_reasons: list[str] = []

    for factor in POSITIVE_HARD_FACTORS:
        if levels[factor] == "low":
            hard_failures.append(f"{factor} is low.")
        elif levels[factor] != "high":
            hold_reasons.append(f"{factor} is not fully cleared.")

    if levels["platform_risk"] == "high":
        hard_failures.append("platform risk is high.")
    elif levels["platform_risk"] != "low":
        hold_reasons.append("platform risk is not low.")

    soft_high_count = 0
    for factor in SOFT_FACTORS:
        if levels[factor] == "low":
            hold_reasons.append(f"{factor} is low.")
        if levels[factor] == "high":
            soft_high_count += 1

    if hard_failures:
        verdict = "REJECT"
    elif hold_reasons:
        verdict = "HOLD"
    elif soft_high_count < 3:
        verdict = "HOLD"
        hold_reasons.append("fewer than three soft factors are high.")
    else:
        verdict = "PASS"

    hard_failures = dedupe(hard_failures)
    hold_reasons = dedupe(hold_reasons)

    next_steps = build_next_steps(verdict, hold_reasons, hard_failures)
    safe_alternatives = build_safe_alternatives(combined_text)

    lines = [
        f"VERDICT: {verdict}",
        "",
        "SUMMARY:",
        f"- idea: {idea or 'not provided'}",
        f"- customer: {customer or 'not provided'}",
        f"- offer: {offer or 'not provided'}",
        f"- acquisition: {acquisition or 'not provided'}",
        f"- data_handling: {data_handling or 'not provided'}",
        "",
        "HARD_FACTORS:",
        factor_block("legality", levels["legality"]),
        factor_block("consent", levels["consent"]),
        factor_block("provenance", levels["provenance"]),
        factor_block("platform_risk", levels["platform_risk"]),
        "",
        "SOFT_FACTORS:",
        factor_block("time_to_cash", levels["time_to_cash"]),
        factor_block("margin", levels["margin"]),
        factor_block("repeatability", levels["repeatability"]),
        factor_block("automation", levels["automation"]),
        factor_block("defensibility", levels["defensibility"]),
        "",
        "REASONS:",
    ]

    if verdict == "REJECT":
        lines.extend(f"- {reason}" for reason in hard_failures)
    elif verdict == "HOLD":
        lines.extend(f"- {reason}" for reason in hold_reasons)
    else:
        lines.extend(
            [
                "- hard gates are fully clear",
                "- no soft factor is low",
                "- at least three soft factors are high",
            ]
        )

    lines.extend(["", "NEXT_STEPS:"])
    lines.extend(f"- {step}" for step in next_steps)

    lines.extend(["", "SAFE_ALTERNATIVES:"])
    lines.extend(f"- {alternative}" for alternative in safe_alternatives)

    if notes:
        lines.extend(["", "NOTES:", f"- {notes}"])

    return "\n".join(lines)


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        customer: str = "",
        offer: str = "",
        acquisition: str = "",
        data_handling: str = "",
        legality: str = "",
        consent: str = "",
        provenance: str = "",
        platform_risk: str = "",
        time_to_cash: str = "",
        margin: str = "",
        repeatability: str = "",
        automation: str = "",
        defensibility: str = "",
        notes: str = "",
        **kwargs,
    ):
        result = assess_revenue_plan(
            idea=idea,
            customer=customer,
            offer=offer,
            acquisition=acquisition,
            data_handling=data_handling,
            legality=legality,
            consent=consent,
            provenance=provenance,
            platform_risk=platform_risk,
            time_to_cash=time_to_cash,
            margin=margin,
            repeatability=repeatability,
            automation=automation,
            defensibility=defensibility,
            notes=notes,
        )
        return Response(message=result, break_loop=False)
