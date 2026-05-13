import json
import re
from typing import Any

from python.helpers.tool import Response, Tool

VALID_SCORES = {"low", "medium", "high", "unknown"}
HARD_GATES = ("legality", "consent", "provenance", "platform_risk")
SOFT_FACTORS = ("time", "margin", "repeatability", "automation", "defensibility")

BLOCKED_PATTERNS = (
    (
        "personal-data resale",
        re.compile(
            r"\b(sell|broker|resell|monetize|trade)\b.{0,40}\b(email|contact)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "Do not build systems that sell, broker, or monetize personal contact data.",
    ),
    (
        "email-list brokerage",
        re.compile(r"\b(email|contact)\s+list(s)?\b", re.IGNORECASE),
        "Email and contact lists are not an approved inventory class.",
    ),
    (
        "inbox scraping",
        re.compile(
            r"\b(extract|scrape|harvest|compile|pull)\b.{0,60}\b(gmail|google email|inbox|mailbox|email address)",
            re.IGNORECASE | re.DOTALL,
        ),
        "Private inbox data can support first-party operations, but not list extraction or resale.",
    ),
    (
        "spam or bulk cold outreach",
        re.compile(
            r"\b(spam|blast|bulk cold outreach|cold email|mass outreach)\b",
            re.IGNORECASE,
        ),
        "Outreach must be consent-based or grounded in a lawful existing relationship.",
    ),
)

SAFE_EMAIL_USES = [
    "Summarize and retrieve context from a user-owned inbox for support, operations, or relationship management.",
    "Draft replies, next steps, or CRM updates for existing contacts or explicit opt-ins.",
    "Analyze aggregate trends from first-party mailboxes without exporting personal contact data for resale.",
]

BLOCKED_EMAIL_USES = [
    "Compiling email-address inventories from Gmail, local files, or exports for resale.",
    "Building bulk outreach targets from private inboxes or non-consensual datasets.",
    "Treating personal contact data as an asset class to be sold to third parties.",
]

DEFAULT_LANES = [
    {
        "lane": "first-party inbox-to-crm assistant",
        "why": "Turns existing customer and prospect conversations into internal workflow gains without reselling personal data.",
        "first_step": "Map one mailbox-to-CRM flow for summarization, tagging, and follow-up drafting.",
    },
    {
        "lane": "autonomous listing operations",
        "why": "Creates service revenue through listing quality, merchandising, and operational automation.",
        "first_step": "Choose one listing channel and define measurable optimization experiments.",
    },
    {
        "lane": "research briefs and lead magnets",
        "why": "Monetizes insight directly while growing a permission-based audience.",
        "first_step": "Publish one narrowly scoped report with an opt-in download flow.",
    },
    {
        "lane": "workflow automation retainers",
        "why": "Sells operational outcomes instead of data access.",
        "first_step": "Package one repeatable automation offer for a specific business niche.",
    },
]


def normalize_score(value: str) -> str:
    score = (value or "").strip().lower()
    if not score:
        return "unknown"
    if score not in VALID_SCORES:
        return "unknown"
    return score


def detect_policy_issues(mission: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for name, pattern, guidance in BLOCKED_PATTERNS:
        if pattern.search(mission):
            issues.append({"issue": name, "guidance": guidance})
    return issues


def choose_lanes(mission: str) -> list[dict[str, str]]:
    mission_lower = mission.lower()
    lanes = list(DEFAULT_LANES)
    if "gmail" in mission_lower or "email" in mission_lower or "inbox" in mission_lower:
        return lanes
    return lanes[1:]


def summarize_reasons(
    hard_scores: dict[str, str], soft_scores: dict[str, str], policy_issues: list[dict[str, str]]
) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if policy_issues:
        reasons.extend(issue["guidance"] for issue in policy_issues)
        return "REJECT", reasons

    if any(hard_scores[name] == "low" for name in HARD_GATES):
        low_fields = [name for name in HARD_GATES if hard_scores[name] == "low"]
        reasons.append(
            "Rejected because at least one hard gate failed: " + ", ".join(low_fields) + "."
        )
        return "REJECT", reasons

    unknown_hard = [name for name in HARD_GATES if hard_scores[name] == "unknown"]
    if unknown_hard:
        reasons.append(
            "Hold until all hard gates are evidenced: " + ", ".join(unknown_hard) + "."
        )
        return "HOLD", reasons

    unknown_soft = [name for name in SOFT_FACTORS if soft_scores[name] == "unknown"]
    low_soft = [name for name in SOFT_FACTORS if soft_scores[name] == "low"]
    high_soft = [name for name in SOFT_FACTORS if soft_scores[name] == "high"]

    if not unknown_soft and not low_soft and len(high_soft) >= 3:
        reasons.append("Passes hard gates and has attractive execution characteristics.")
        return "PASS", reasons

    if low_soft:
        reasons.append(
            "Compliant but execution needs work because these factors are low: "
            + ", ".join(low_soft)
            + "."
        )
    if unknown_soft:
        reasons.append(
            "Compliant but incomplete because these soft factors are unevidenced: "
            + ", ".join(unknown_soft)
            + "."
        )
    if len(high_soft) < 3:
        reasons.append("Compliant but not yet strong enough on repeatable economics or automation.")

    return "HOLD", reasons


def plan_revenue_mission(mission: str = "", **scores: str) -> dict[str, Any]:
    mission_text = (mission or "").strip()
    mission_for_rules = mission_text.lower()

    hard_scores = {name: normalize_score(scores.get(name, "")) for name in HARD_GATES}
    soft_scores = {name: normalize_score(scores.get(name, "")) for name in SOFT_FACTORS}
    policy_issues = detect_policy_issues(mission_for_rules)
    verdict, reasons = summarize_reasons(hard_scores, soft_scores, policy_issues)

    next_actions = [
        "Score the chosen lane with explicit legality, consent, provenance, and platform evidence.",
        "Keep Gmail or inbox usage limited to first-party retrieval, summarization, and CRM support.",
        "Choose one revenue lane and define a smallest revenue-bearing workflow with measurable unit economics.",
    ]
    if verdict == "REJECT":
        next_actions = [
            "Drop the blocked workflow from the queue.",
            "Replace it with an opt-in, first-party, or service-based lane.",
            "Only resume planning after the redesign clears legality, consent, provenance, and platform checks.",
        ]

    return {
        "mission": mission_text,
        "verdict": verdict,
        "reasons": reasons,
        "hard_gates": hard_scores,
        "soft_factors": soft_scores,
        "policy_issues": policy_issues,
        "approved_email_data_uses": SAFE_EMAIL_USES,
        "blocked_email_data_uses": BLOCKED_EMAIL_USES,
        "recommended_lanes": choose_lanes(mission_text),
        "next_actions": next_actions,
    }


class RevenuePlanning(Tool):
    async def execute(self, mission: str = "", **kwargs):
        plan = plan_revenue_mission(mission=mission, **kwargs)
        return Response(message=json.dumps(plan, indent=2), break_loop=False)
