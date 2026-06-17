from python.helpers import files
from python.helpers.tool import Tool, Response


REJECT_PATTERNS = {
    "email list": "selling or compiling email lists is personal-data brokerage",
    "contact list": "brokering contact lists is not an approved revenue lane",
    "gmail": "private inbox data cannot be repurposed as a lead source",
    "inbox": "private inbox data cannot be repurposed as a lead source",
    "scrape emails": "scraping email addresses for monetization is non-consensual",
    "harvest emails": "harvesting email addresses is non-consensual",
    "sell leads": "selling personal leads requires clear consent and rights",
    "sell data": "selling personal data is disallowed",
    "broker": "data brokerage is outside the approved scope",
    "spam": "spam-based acquisition is disallowed",
}

PIVOT_LANES = [
    "digital products for willing buyers",
    "productized services using first-party or clearly permissioned data",
    "marketplace listings for products or inventory you are allowed to sell",
    "opt-in newsletters, waitlists, and CRM flows with clear consent",
    "affiliate or partnership content with truthful disclosures",
]


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        assets: str = "",
        constraints: str = "",
        data_sources: str = "",
        **kwargs,
    ):
        brief = "\n".join(
            [
                f"Objective: {objective}".strip(),
                f"Assets: {assets}".strip(),
                f"Constraints: {constraints}".strip(),
                f"Data sources: {data_sources}".strip(),
            ]
        ).strip()

        decision, reasons = classify_request(brief)
        compliance_rules = load_policy_excerpt()
        lanes = choose_lanes(brief, decision)
        next_steps = build_next_steps(decision, lanes)

        sections = [
            f"Decision: {decision}",
            "",
            "Why:",
            *[f"- {reason}" for reason in reasons],
            "",
            "Non-negotiable rules:",
            *[f"- {rule}" for rule in compliance_rules],
            "",
            "Recommended lanes:",
            *[f"- {lane}" for lane in lanes],
            "",
            "Next steps:",
            *[f"- {step}" for step in next_steps],
        ]

        return Response(message="\n".join(sections).strip(), break_loop=False)


def classify_request(text: str):
    lowered = text.lower()
    rejection_reasons = [
        reason for pattern, reason in REJECT_PATTERNS.items() if pattern in lowered
    ]
    if rejection_reasons:
        return (
            "REJECT",
            rejection_reasons
            + [
                "pivot to first-party, consent-based, platform-compliant revenue lanes",
            ],
        )

    hold_reasons = []
    if not text.strip():
        hold_reasons.append("objective details are missing")
    if not any(field in lowered for field in ("consent", "opt-in", "first-party")):
        hold_reasons.append("consent and data-rights posture is not explicit")
    if not any(field in lowered for field in ("legal", "lawful", "compliant")):
        hold_reasons.append("legal and platform-rule checks are not explicit")

    if hold_reasons:
        return ("HOLD", hold_reasons)

    return (
        "PASS",
        [
            "the request appears compatible with consent-based monetization",
            "no blocked privacy or spam patterns were detected",
        ],
    )


def choose_lanes(text: str, decision: str):
    lowered = text.lower()
    if decision == "REJECT":
        return PIVOT_LANES

    lanes = []
    if any(word in lowered for word in ("template", "guide", "ebook", "course")):
        lanes.append("digital products")
    if any(word in lowered for word in ("service", "consulting", "ops", "automation")):
        lanes.append("productized services")
    if any(word in lowered for word in ("listing", "marketplace", "shop", "store")):
        lanes.append("marketplace commerce")
    if any(word in lowered for word in ("newsletter", "content", "audience", "community")):
        lanes.append("opt-in audience assets")

    if not lanes:
        lanes = [
            "digital products",
            "productized services",
            "marketplace commerce",
        ]

    return lanes


def build_next_steps(decision: str, lanes: list[str]):
    if decision == "REJECT":
        return [
            "replace the blocked acquisition idea with one approved revenue lane",
            "document first-party or permissioned data sources only",
            "run the strategy score instrument before any implementation work",
            "seek human approval before publishing or contacting anyone",
        ]

    if decision == "HOLD":
        return [
            "clarify the legal basis, consent state, and data rights",
            "document platform constraints for the intended channel",
            "score the idea with instruments/strategy/score.sh",
            f"refine the offer around one lane: {lanes[0]}",
        ]

    return [
        "capture the offer in docs/strategy/incoming.md",
        "score it with instruments/strategy/score.sh",
        f"draft an execution plan around {lanes[0]}",
        "define a human approval gate before launch",
    ]


def load_policy_excerpt():
    path = "docs/policies/compliance_pack.md"
    if not files.exists(path):
        return [
            "refuse unlawful, privacy-invasive, deceptive, or non-consensual work",
            "do not sell personal data or private inbox contents",
            "require clear data rights and platform compliance",
        ]

    content = files.read_file(path).splitlines()
    excerpt = []
    for line in content:
        stripped = line.strip()
        if stripped.startswith("- ") or stripped[:2].isdigit():
            excerpt.append(stripped.lstrip("- ").strip())
        if len(excerpt) == 4:
            break

    return excerpt or [
        "refuse unlawful, privacy-invasive, deceptive, or non-consensual work",
        "do not sell personal data or private inbox contents",
        "require clear data rights and platform compliance",
    ]
