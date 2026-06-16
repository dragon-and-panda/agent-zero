from dataclasses import dataclass
import re

from python.helpers.tool import Response, Tool


SAFE_ALTERNATIVES = [
    "Build a first-party, opt-in lead magnet and newsletter.",
    "Offer an automation or listing-optimization service instead of selling data.",
    "Package owned expertise into a digital product, template, or research pack.",
    "Use inbox data only for the account owner's internal organization and follow-up workflows.",
]

REJECT_RULES = [
    (
        "personal email list brokerage",
        [
            r"\bsell(?:ing)?\b.*\bemail list",
            r"\bbroker(?:ing)?\b.*\bemail",
            r"\brent(?:ing)?\b.*\bemail list",
            r"\bcompiled email list",
        ],
        "Personal email list resale is prohibited.",
    ),
    (
        "gmail contact extraction for resale",
        [
            r"\bgmail\b.*\bextract",
            r"\bextract\b.*\bgmail\b",
            r"\bgmail\b.*\bemail list",
            r"\binbox\b.*\bemail list",
        ],
        "Inbox-derived contact extraction is only acceptable for owner-authorized internal use, not resale or spam.",
    ),
    (
        "spam or cold-bulk outreach",
        [
            r"\bspam\b",
            r"\bcold email\b",
            r"\bbulk outreach\b",
            r"\bunsolicited\b.*\bemail",
        ],
        "Spam and unsolicited bulk outreach are not acceptable acquisition strategies.",
    ),
]

HOLD_RULES = [
    (
        "regulated or sensitive domain",
        [
            r"\bhealth\b",
            r"\bmedical\b",
            r"\binsurance\b",
            r"\bloan\b",
            r"\bsecurities\b",
            r"\bminor\b",
        ],
        "The idea touches a regulated or sensitive domain and needs extra review.",
    ),
]


@dataclass
class PlanAssessment:
    decision: str
    reasons: list[str]
    safer_alternatives: list[str]
    next_steps: list[str]


def _normalize(*parts: str) -> str:
    return "\n".join(part.strip() for part in parts if part).lower()


def _matches(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def evaluate_plan(
    mission: str = "",
    assets: str = "",
    audience: str = "",
    data_sources: str = "",
    outreach: str = "",
    notes: str = "",
) -> PlanAssessment:
    text = _normalize(mission, assets, audience, data_sources, outreach, notes)
    reasons: list[str] = []
    safer_alternatives: list[str] = []
    next_steps: list[str] = []
    decision = "PASS"

    if not text:
        return PlanAssessment(
            decision="HOLD",
            reasons=["No plan details were provided."],
            safer_alternatives=SAFE_ALTERNATIVES[:2],
            next_steps=[
                "Describe the customer problem, revenue model, data sources, and outreach method.",
                "Run the strategy score instrument before execution.",
            ],
        )

    for _name, patterns, reason in REJECT_RULES:
        if _matches(text, patterns):
            decision = "REJECT"
            reasons.append(reason)

    if decision != "REJECT":
        for _name, patterns, reason in HOLD_RULES:
            if _matches(text, patterns):
                decision = "HOLD"
                reasons.append(reason)

    if "gmail" in text or "inbox" in text:
        next_steps.append(
            "If inbox data is involved, keep usage limited to owner-authorized internal organization or CRM hygiene."
        )

    if "email list" in text or "contact list" in text:
        safer_alternatives.extend(SAFE_ALTERNATIVES[:3])

    if decision == "PASS":
        reasons.append("No obvious consent, provenance, or platform-policy red flags were detected.")
        next_steps.extend(
            [
                "Verify legality, consent quality, and platform rules with the compliance pack.",
                "Score the opportunity with instruments/strategy/score.sh.",
                "Prefer first-party distribution, owned assets, and repeatable delivery.",
            ]
        )
    elif decision == "HOLD":
        safer_alternatives.extend(
            [
                "Narrow the data scope to first-party or owner-authorized sources.",
                "Document consent and platform dependencies before execution.",
            ]
        )
        next_steps.extend(
            [
                "Resolve the flagged review items before launching.",
                "Do not automate outreach until consent and platform assumptions are explicit.",
            ]
        )
    else:
        safer_alternatives.extend(SAFE_ALTERNATIVES)
        next_steps.extend(
            [
                "Do not execute the rejected plan.",
                "Replace personal-data monetization with a service, software, or opt-in audience model.",
            ]
        )

    return PlanAssessment(
        decision=decision,
        reasons=_dedupe(reasons),
        safer_alternatives=_dedupe(safer_alternatives),
        next_steps=_dedupe(next_steps),
    )


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            output.append(item)
    return output


def format_assessment(assessment: PlanAssessment) -> str:
    lines = [f"decision: {assessment.decision}", "", "reasons:"]
    lines.extend(f"- {reason}" for reason in assessment.reasons)
    if assessment.safer_alternatives:
        lines.extend(["", "safer_alternatives:"])
        lines.extend(f"- {item}" for item in assessment.safer_alternatives)
    if assessment.next_steps:
        lines.extend(["", "next_steps:"])
        lines.extend(f"- {item}" for item in assessment.next_steps)
    return "\n".join(lines)


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        audience: str = "",
        data_sources: str = "",
        outreach: str = "",
        notes: str = "",
        **kwargs,
    ):
        assessment = evaluate_plan(
            mission=mission,
            assets=assets,
            audience=audience,
            data_sources=data_sources,
            outreach=outreach,
            notes=notes,
        )
        return Response(message=format_assessment(assessment), break_loop=False)
