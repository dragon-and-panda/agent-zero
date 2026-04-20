import json

from python.helpers.tool import Tool, Response


HARD_REJECT_REASONS = {
    "illegality": "fails legality requirements",
    "no_consent": "uses personal data without consent or ownership authorization",
    "unclear_provenance": "has unclear data provenance or auditability",
    "tos_conflict": "conflicts with platform terms or anti-abuse controls",
    "personal_data_resale": "depends on selling or brokering personal contact data",
}

SOFT_FIELDS = [
    "time_to_cash",
    "margin",
    "repeatability",
    "automation_fit",
    "defensibility",
]

HIGH_VALUE = {"high", "strong"}
LOW_VALUE = {"low", "weak"}


def _normalize(value: str) -> str:
    return str(value or "").strip().lower()


def _parse_json(raw: str) -> dict:
    if not raw:
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("plan_json must decode to a JSON object")
    return data


def _collect_rejects(plan: dict) -> list[str]:
    reasons = []
    for key, message in HARD_REJECT_REASONS.items():
        if plan.get(key) is True:
            reasons.append(message)
    return reasons


def _score_soft_factors(plan: dict) -> tuple[int, int]:
    highs = 0
    lows = 0
    for field in SOFT_FIELDS:
        value = _normalize(plan.get(field, ""))
        if value in HIGH_VALUE:
            highs += 1
        elif value in LOW_VALUE:
            lows += 1
    return highs, lows


def evaluate_plan(plan: dict) -> dict:
    name = str(plan.get("name") or "unnamed lane").strip()
    summary = str(plan.get("summary") or "").strip()
    reject_reasons = _collect_rejects(plan)
    highs, lows = _score_soft_factors(plan)

    must_pass = {
        "legality": _normalize(plan.get("legality")),
        "consent": _normalize(plan.get("consent")),
        "provenance": _normalize(plan.get("provenance")),
        "terms_of_service": _normalize(plan.get("terms_of_service")),
    }

    gate_failures = [
        key for key, value in must_pass.items() if value not in {"pass", "clear", "strong"}
    ]

    status = "PASS"
    rationale = []

    if reject_reasons:
        status = "REJECT"
        rationale.extend(reject_reasons)

    if gate_failures:
        status = "REJECT"
        rationale.append(
            "failed required gates: " + ", ".join(gate_failures)
        )

    if status != "REJECT":
        if lows > 0:
            status = "HOLD"
            rationale.append("one or more execution factors are low")
        elif highs < 3:
            status = "HOLD"
            rationale.append("fewer than three execution factors are high")
        else:
            rationale.append("all hard gates clear and execution profile is attractive")

    preferred_lane = str(plan.get("preferred_lane") or "").strip()
    if preferred_lane:
        rationale.append(f"preferred compliant lane: {preferred_lane}")

    result = {
        "name": name,
        "summary": summary,
        "status": status,
        "required_gates": must_pass,
        "soft_factors": {field: _normalize(plan.get(field, "")) for field in SOFT_FIELDS},
        "high_soft_factor_count": highs,
        "low_soft_factor_count": lows,
        "rationale": rationale,
        "next_step": _next_step_for(status),
    }
    return result


def _next_step_for(status: str) -> str:
    if status == "PASS":
        return "draft a concrete offer, target customer, acquisition plan, and first experiment"
    if status == "HOLD":
        return "improve weak factors or tighten the lane before activation"
    return "replace the idea with a compliant, consent-based revenue lane"


class RevenuePlanning(Tool):
    async def execute(self, plan_json: str = "", **kwargs):
        if not plan_json:
            return Response(
                message="plan_json is required and must be a JSON object.",
                break_loop=False,
            )

        try:
            plan = _parse_json(plan_json)
            result = evaluate_plan(plan)
        except Exception as exc:
            return Response(
                message=f"Invalid plan_json: {exc}",
                break_loop=False,
            )

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=True),
            break_loop=False,
        )
