import json

from python.helpers.tool import Response, Tool


ALLOWED_LEVELS = {"low", "medium", "high"}
HARD_GATES = ("legality", "consent", "provenance", "tos")
SOFT_FACTORS = (
    "margin",
    "repeatability",
    "automation",
    "defensibility",
    "time_to_cash",
)


def validate_level(name: str, value: str) -> str:
    normalized = (value or "").strip().lower()
    if normalized not in ALLOWED_LEVELS:
        raise ValueError(f"{name} must be one of: low, medium, high")
    return normalized


def score_level(value: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}[value]


class RevenuePlanning(Tool):
    async def execute(
        self,
        opportunity: str = "",
        legality: str = "",
        consent: str = "",
        provenance: str = "",
        tos: str = "",
        margin: str = "",
        repeatability: str = "",
        automation: str = "",
        defensibility: str = "",
        time_to_cash: str = "",
        setup_complexity: str = "",
        notes: str = "",
        **kwargs,
    ):
        try:
            hard_gates = {
                "legality": validate_level("legality", legality),
                "consent": validate_level("consent", consent),
                "provenance": validate_level("provenance", provenance),
                "tos": validate_level("tos", tos),
            }
            soft_factors = {
                "margin": validate_level("margin", margin),
                "repeatability": validate_level("repeatability", repeatability),
                "automation": validate_level("automation", automation),
                "defensibility": validate_level("defensibility", defensibility),
                "time_to_cash": validate_level("time_to_cash", time_to_cash),
            }
            setup_complexity = validate_level("setup_complexity", setup_complexity)
        except ValueError as exc:
            return Response(
                message=json.dumps({"error": str(exc)}, indent=2),
                break_loop=False,
            )

        reasons: list[str] = []
        next_step = "Reject the lane and select a different opportunity."

        for name in HARD_GATES:
            if hard_gates[name] == "low":
                result = {
                    "opportunity": opportunity,
                    "verdict": "REJECT",
                    "reasons": [f"Hard gate '{name}' is low."],
                    "next_step": next_step,
                    "hard_gates": hard_gates,
                    "soft_factors": soft_factors,
                    "setup_complexity": setup_complexity,
                    "notes": notes,
                }
                return Response(message=json.dumps(result, indent=2), break_loop=False)

        for name in HARD_GATES:
            if hard_gates[name] == "medium":
                reasons.append(f"Hard gate '{name}' needs stronger evidence.")

        high_soft = 0
        soft_total = 0
        for name in SOFT_FACTORS:
            value = soft_factors[name]
            soft_total += score_level(value)
            if value == "high":
                high_soft += 1
            if value == "low":
                reasons.append(f"Soft factor '{name}' is low.")

        if setup_complexity == "low":
            soft_total += 3
        elif setup_complexity == "medium":
            soft_total += 2
            reasons.append("Setup complexity is medium.")
        else:
            soft_total += 1
            reasons.append("Setup complexity is high.")

        if not reasons and high_soft >= 4 and soft_total >= 15:
            verdict = "PASS"
            next_step = "Proceed to a focused execution plan and keep the compliance pack attached."
        else:
            verdict = "HOLD"
            next_step = "Gather evidence, improve the economics, or narrow the lane before execution."

        result = {
            "opportunity": opportunity,
            "verdict": verdict,
            "reasons": reasons or ["Economics are not strong enough to prioritize yet."],
            "next_step": next_step,
            "hard_gates": hard_gates,
            "soft_factors": soft_factors,
            "setup_complexity": setup_complexity,
            "notes": notes,
        }
        return Response(message=json.dumps(result, indent=2), break_loop=False)
