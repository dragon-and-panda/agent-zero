import json
from typing import Dict, List

from python.helpers.tool import Response, Tool

VALID_LEVELS = {"low", "medium", "high"}
BLOCKED_KEYWORDS = (
    "sell email list",
    "selling email list",
    "broker email list",
    "email list for sale",
    "contact list for sale",
    "compile email list",
    "scrape gmail",
    "scrape inbox",
    "gmail rag",
    "gmail leads",
    "resell contacts",
    "resale of contacts",
    "spam campaign",
)

SAFE_ALTERNATIVES = (
    "first-party inbox-to-CRM cleanup for the account owner or an authorized client",
    "productized research from public or licensed sources",
    "autonomous listing operations using customer-owned inventory",
    "opt-in newsletter or content product growth",
    "automation services delivered under explicit client authorization",
)


def normalize_level(value: str, default: str = "medium") -> str:
    normalized = (value or "").strip().lower()
    if normalized not in VALID_LEVELS:
        return default
    return normalized


def build_text_blob(payload: Dict[str, str]) -> str:
    return " ".join(str(payload.get(key, "")) for key in payload).lower()


def evaluate_revenue_plan(payload: Dict[str, str]) -> Dict[str, object]:
    text_blob = build_text_blob(payload)
    hard_failures: List[str] = []
    hard_holds: List[str] = []
    soft_issues: List[str] = []

    scores = {
        "legality": normalize_level(payload.get("legality", "medium")),
        "consent": normalize_level(payload.get("consent", "medium")),
        "data_provenance": normalize_level(payload.get("data_provenance", "medium")),
        "platform_risk": normalize_level(payload.get("platform_risk", "medium")),
        "time_to_revenue": normalize_level(payload.get("time_to_revenue", "medium")),
        "margin": normalize_level(payload.get("margin", "medium")),
        "repeatability": normalize_level(payload.get("repeatability", "medium")),
        "automation": normalize_level(payload.get("automation", "medium")),
        "defensibility": normalize_level(payload.get("defensibility", "medium")),
    }

    blocked_hits = [keyword for keyword in BLOCKED_KEYWORDS if keyword in text_blob]
    if blocked_hits:
        hard_failures.append(
            "plan matches blocked privacy-abuse or contact-resale patterns"
        )

    if scores["legality"] == "low":
        hard_failures.append("legality confidence is low")
    elif scores["legality"] == "medium":
        hard_holds.append("legality confidence needs to be raised to high")

    if scores["consent"] == "low":
        hard_failures.append("consent is weak or absent")
    elif scores["consent"] == "medium":
        hard_holds.append("consent needs clearer authorization")

    if scores["data_provenance"] == "low":
        hard_failures.append("data provenance is weak or unclear")
    elif scores["data_provenance"] == "medium":
        hard_holds.append("data provenance needs clearer validation")

    if scores["platform_risk"] == "high":
        hard_failures.append("platform risk is high")
    elif scores["platform_risk"] == "medium":
        hard_holds.append("platform risk is not yet low")

    soft_fields = (
        "time_to_revenue",
        "margin",
        "repeatability",
        "automation",
        "defensibility",
    )
    soft_high_count = 0
    for field in soft_fields:
        value = scores[field]
        if value == "high":
            soft_high_count += 1
        elif value == "low":
            soft_issues.append(f"{field} is weak")

    if hard_failures:
        decision = "REJECT"
        summary = (
            "Reject this revenue lane. It fails one or more hard compliance gates "
            "or resembles prohibited privacy-abuse patterns."
        )
    elif hard_holds or soft_issues or soft_high_count < 3:
        decision = "HOLD"
        summary = (
            "Do not automate or launch this lane yet. Clear the remaining "
            "compliance and economic gaps first."
        )
    else:
        decision = "PASS"
        summary = (
            "This lane clears the hard gates and has enough attractive economics "
            "for a controlled pilot."
        )

    next_actions: List[str] = []
    if decision == "REJECT":
        next_actions.extend(
            [
                "drop the blocked lane instead of trying to optimize it",
                "rewrite the plan around first-party or licensed inputs",
                "choose a safe alternative that does not rely on personal-data resale",
            ]
        )
    elif decision == "HOLD":
        next_actions.extend(
            [
                "raise legality, consent, provenance, and platform confidence to high or low-risk as appropriate",
                "improve the weakest soft factors before pilot launch",
                "re-score the lane after the inputs are clarified",
            ]
        )
    else:
        next_actions.extend(
            [
                "run a small pilot with explicit customer authorization",
                "measure revenue, margin, repeatability, and compliance incidents",
                "record results in docs/programs/agentic_financial_system/journal.md",
            ]
        )

    return {
        "decision": decision,
        "summary": summary,
        "scores": scores,
        "hard_failures": hard_failures,
        "hard_holds": hard_holds,
        "soft_issues": soft_issues,
        "soft_high_count": soft_high_count,
        "blocked_keyword_hits": blocked_hits,
        "recommended_safe_alternatives": list(SAFE_ALTERNATIVES),
        "next_actions": next_actions,
    }


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        offer: str = "",
        customer: str = "",
        acquisition: str = "",
        legality: str = "medium",
        consent: str = "medium",
        data_provenance: str = "medium",
        platform_risk: str = "medium",
        time_to_revenue: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation: str = "medium",
        defensibility: str = "medium",
        notes: str = "",
        **kwargs,
    ):
        report = evaluate_revenue_plan(
            {
                "idea": idea,
                "offer": offer,
                "customer": customer,
                "acquisition": acquisition,
                "legality": legality,
                "consent": consent,
                "data_provenance": data_provenance,
                "platform_risk": platform_risk,
                "time_to_revenue": time_to_revenue,
                "margin": margin,
                "repeatability": repeatability,
                "automation": automation,
                "defensibility": defensibility,
                "notes": notes,
            }
        )
        return Response(message=json.dumps(report, indent=2), break_loop=False)
