from __future__ import annotations

from typing import Any

REJECT_PATTERNS = (
    "sell email list",
    "sell compiled email",
    "broker email list",
    "resell email list",
    "resell personal data",
    "compile email address lists",
    "compile email lists",
    "harvest emails",
    "gmail data",
    "google email data",
    "scrape inbox",
    "scrape emails",
    "cold spam",
    "mass unsolicited",
    "buy contact list",
    "sell contact list",
)

SENSITIVE_PATTERNS = (
    "gmail",
    "google email",
    "inbox",
    "email",
    "contacts",
    "lead list",
    "mailbox",
    "outreach",
    "newsletter",
    "crm",
)

SAFE_DATA_POLICY = [
    "use first-party or explicitly licensed data only",
    "require documented ownership, provenance, and lawful basis for contact data",
    "do not resell personal data or compile inbox-derived contact lists",
    "keep operational use separate from marketing use",
    "honor unsubscribe, deletion, and retention controls",
]

ALTERNATIVE_LANES = [
    "opt-in newsletter or lead-magnet funnel",
    "first-party CRM hygiene for businesses that control their own data",
    "owner-authorized inbox triage, summarization, or routing assistant",
    "listing optimization and marketplace operations from seller-provided assets",
    "digital products such as reports, templates, prompt packs, or niche software",
]


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _contains_any(text: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if pattern in text]


def _recommend_lanes(text: str) -> list[dict[str, Any]]:
    lanes: list[dict[str, Any]] = []

    if any(keyword in text for keyword in ("inbox", "gmail", "support", "mailbox")):
        lanes.append(
            {
                "lane": "owner-authorized inbox assistant",
                "fit": "Good for search, summarization, routing, and operations on a mailbox the operator controls.",
                "next_steps": [
                    "Confirm mailbox ownership and approved scope.",
                    "Document retention and deletion rules.",
                    "Avoid exporting contacts for resale or unsolicited outreach.",
                ],
            }
        )

    if any(keyword in text for keyword in ("crm", "contacts", "lead", "email")):
        lanes.append(
            {
                "lane": "first-party CRM hygiene service",
                "fit": "Useful when a business already owns its customer or subscriber data.",
                "next_steps": [
                    "Filter for consent-compatible records only.",
                    "Retain provenance and lawful-basis fields.",
                    "Use extracted data for internal operations or approved campaigns only.",
                ],
            }
        )

    if any(keyword in text for keyword in ("listing", "marketplace", "seller", "product")):
        lanes.append(
            {
                "lane": "listing optimization service",
                "fit": "Monetizes seller-provided assets without relying on personal data resale.",
                "next_steps": [
                    "Package photo cleanup, copywriting, and publishing as a service.",
                    "Measure conversion uplift and turnaround time.",
                ],
            }
        )

    if any(keyword in text for keyword in ("research", "newsletter", "content", "rag")):
        lanes.append(
            {
                "lane": "opt-in research product",
                "fit": "Creates recurring revenue from consented subscribers and premium insights.",
                "next_steps": [
                    "Pick a niche and define a lead magnet.",
                    "Collect only opt-in subscriber information.",
                    "Offer premium reports, memberships, or related services.",
                ],
            }
        )

    if not lanes:
        lanes.extend(
            [
                {
                    "lane": "digital product or productized service",
                    "fit": "Broadest compliant default when a mission does not require personal data.",
                    "next_steps": [
                        "Package repeatable expertise into a template, workflow, or service.",
                        "Validate demand with small paid pilots.",
                    ],
                }
            ]
        )

    return lanes


def evaluate_revenue_mission(mission: str, context: str = "") -> dict[str, Any]:
    combined = _normalize(f"{mission} {context}".strip())
    reject_hits = _contains_any(combined, REJECT_PATTERNS)
    sensitive_hits = _contains_any(combined, SENSITIVE_PATTERNS)

    blocked_reasons: list[str] = []
    required_controls: list[str] = []

    if reject_hits:
        blocked_reasons.append(
            "The request includes contact-list resale, inbox scraping, or personal-data brokerage patterns."
        )

    if "sell" in combined and "email" in combined and "list" in combined:
        blocked_reasons.append("Selling email lists is outside the approved compliance posture.")

    if ("gmail" in combined or "inbox" in combined) and any(
        token in combined for token in ("extract", "compile", "sell", "broker", "resell")
    ):
        blocked_reasons.append("Inbox data cannot be repurposed into third-party contact inventory.")

    if sensitive_hits and not blocked_reasons:
        required_controls.extend(
            [
                "Confirm ownership or written authorization for the mailbox or contact dataset.",
                "Document consent or other lawful basis before using contact records.",
                "Restrict usage to internal operations, approved campaigns, or opt-in experiences.",
            ]
        )

    if blocked_reasons:
        status = "REJECT"
        summary = "The mission conflicts with consent, privacy, or anti-spam requirements."
    elif sensitive_hits:
        status = "HOLD"
        summary = "The mission may be workable only with explicit ownership, provenance, and consent controls."
    else:
        status = "PASS"
        summary = "The mission fits a compliant, first-party revenue workflow."

    return {
        "status": status,
        "summary": summary,
        "blocked_reasons": blocked_reasons,
        "required_controls": required_controls,
        "safe_data_policy": SAFE_DATA_POLICY,
        "recommended_alternatives": ALTERNATIVE_LANES,
        "recommended_lanes": _recommend_lanes(combined),
    }
