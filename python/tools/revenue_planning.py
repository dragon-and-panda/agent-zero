import json

from python.helpers.tool import Tool, Response

SOFT_KEYS = ("time", "margin", "repeatability", "automation", "defensibility")
RISKY_TERMS = (
    "email list",
    "sell emails",
    "gmail scrape",
    "scrape inbox",
    "cold email blast",
    "broker contacts",
    "buy leads",
    "resell contacts",
    "non-consensual",
    "spam",
)


def _normalize_score(value: str, default: str = "medium") -> str:
    text = str(value or default).strip().lower()
    if text in {"low", "medium", "high"}:
        return text
    return default


def _score_to_points(value: str) -> int:
    if value == "high":
        return 2
    if value == "medium":
        return 1
    return 0


def _detect_red_flags(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in RISKY_TERMS if term in lowered]


def evaluate_lane(
    lane_name: str,
    summary: str,
    legality: str,
    consent: str,
    provenance: str,
    platform_risk: str,
    time: str,
    margin: str,
    repeatability: str,
    automation: str,
    defensibility: str,
) -> dict[str, object]:
    normalized = {
        "legality": _normalize_score(legality),
        "consent": _normalize_score(consent),
        "provenance": _normalize_score(provenance),
        "platform_risk": _normalize_score(platform_risk),
        "time": _normalize_score(time),
        "margin": _normalize_score(margin),
        "repeatability": _normalize_score(repeatability),
        "automation": _normalize_score(automation),
        "defensibility": _normalize_score(defensibility),
    }

    red_flags = _detect_red_flags(f"{lane_name}\n{summary}")
    reasons: list[str] = []

    if normalized["legality"] == "low":
        reasons.append("reject: legality is low")
    if normalized["consent"] == "low":
        reasons.append("reject: consent is low")
    if normalized["provenance"] == "low":
        reasons.append("reject: data provenance is low")
    if normalized["platform_risk"] == "high":
        reasons.append("reject: platform risk is high")
    if red_flags:
        reasons.append(
            "reject: request contains prohibited monetization terms "
            + ", ".join(red_flags)
        )

    soft_values = [normalized[key] for key in SOFT_KEYS]
    soft_points = sum(_score_to_points(value) for value in soft_values)
    low_soft = [key for key in SOFT_KEYS if normalized[key] == "low"]
    high_soft = [key for key in SOFT_KEYS if normalized[key] == "high"]

    if reasons:
        decision = "REJECT"
    elif low_soft:
        decision = "HOLD"
        reasons.append("hold: at least one execution factor is low")
    elif len(high_soft) < 3:
        decision = "HOLD"
        reasons.append("hold: fewer than three execution factors are high")
    elif soft_points < 8:
        decision = "HOLD"
        reasons.append("hold: execution quality is not yet strong enough")
    else:
        decision = "PASS"
        reasons.append("pass: compliance gates cleared and execution profile is strong")

    if decision != "REJECT":
        if normalized["platform_risk"] == "medium":
            reasons.append("watch: platform risk is medium")
        if normalized["legality"] != "high":
            reasons.append("watch: legality should be verified before launch")
        if normalized["consent"] != "high":
            reasons.append("watch: consent posture should be strengthened")

    return {
        "lane_name": lane_name,
        "decision": decision,
        "scores": normalized,
        "soft_points": soft_points,
        "high_soft_factors": high_soft,
        "reasons": reasons,
        "recommended_next_step": _recommended_next_step(decision),
    }


def _recommended_next_step(decision: str) -> str:
    if decision == "PASS":
        return "Run a narrow pilot, instrument outcomes, and log progress in the mission journal."
    if decision == "HOLD":
        return "Tighten consent, improve unit economics, or reduce platform risk before activation."
    return "Redirect to a compliant alternative such as opt-in lead capture, client-owned CRM work, or first-party listing services."


class RevenuePlanning(Tool):
    async def execute(
        self,
        lane_name: str = "",
        summary: str = "",
        legality: str = "medium",
        consent: str = "medium",
        provenance: str = "medium",
        platform_risk: str = "medium",
        time: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation: str = "medium",
        defensibility: str = "medium",
        **kwargs,
    ):
        result = evaluate_lane(
            lane_name=lane_name,
            summary=summary,
            legality=legality,
            consent=consent,
            provenance=provenance,
            platform_risk=platform_risk,
            time=time,
            margin=margin,
            repeatability=repeatability,
            automation=automation,
            defensibility=defensibility,
        )
        return Response(message=json.dumps(result, indent=2), break_loop=False)
