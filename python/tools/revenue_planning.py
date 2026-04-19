import json
from textwrap import dedent

from python.helpers.tool import Tool, Response


ALLOWED_VALUES = {"low", "medium", "high"}
HARD_FACTORS = ("legality", "consent", "provenance", "platform_fit")
SOFT_FACTORS = (
    "time_to_cash",
    "margin",
    "repeatability",
    "automation_fit",
    "defensibility",
)


class RevenuePlanning(Tool):
    async def execute(
        self,
        lane: str = "",
        summary: str = "",
        legality: str = "",
        consent: str = "",
        provenance: str = "",
        platform_fit: str = "",
        time_to_cash: str = "",
        margin: str = "",
        repeatability: str = "",
        automation_fit: str = "",
        defensibility: str = "",
        notes: str = "",
        **kwargs,
    ):
        lane_name = lane.strip() or "unnamed lane"
        factor_inputs = {
            "legality": legality,
            "consent": consent,
            "provenance": provenance,
            "platform_fit": platform_fit,
            "time_to_cash": time_to_cash,
            "margin": margin,
            "repeatability": repeatability,
            "automation_fit": automation_fit,
            "defensibility": defensibility,
        }

        errors = []
        normalized = {}
        for factor_name, raw_value in factor_inputs.items():
            value = str(raw_value).strip().lower()
            if value not in ALLOWED_VALUES:
                errors.append(
                    f"{factor_name} must be one of low, medium, high; got '{raw_value}'."
                )
            else:
                normalized[factor_name] = value

        if errors:
            return Response(message="\n".join(errors), break_loop=False)

        reject_reasons = [
            factor_name for factor_name in HARD_FACTORS if normalized[factor_name] == "low"
        ]
        hold_reasons = [
            factor_name for factor_name in SOFT_FACTORS if normalized[factor_name] == "low"
        ]
        watch_items = [
            factor_name
            for factor_name, value in normalized.items()
            if value == "medium" and factor_name not in hold_reasons
        ]

        if reject_reasons:
            decision = "REJECT"
            rationale = (
                "The proposal fails one or more non-negotiable compliance gates and should "
                "not be executed until the blocked factors are redesigned."
            )
        elif hold_reasons:
            decision = "HOLD"
            rationale = (
                "The proposal clears the compliance gates but is not yet commercially strong "
                "enough for activation."
            )
        else:
            decision = "APPROVE"
            rationale = (
                "The proposal clears the compliance gates and has no low commercial-readiness "
                "factors."
            )

        guidance = []
        if reject_reasons:
            guidance.append(
                "Replace or remove any workflow elements that rely on unclear legality, "
                "missing consent, unclear provenance, or platform-rule conflicts."
            )
        if hold_reasons:
            guidance.append(
                "Improve the low-readiness factors before activation or keep the lane in a "
                "limited discovery state."
            )
        if watch_items:
            guidance.append(
                "Monitor these medium-confidence factors closely: "
                + ", ".join(sorted(watch_items))
                + "."
            )
        if not guidance:
            guidance.append(
                "Document the data sources, stop conditions, and first activation milestone "
                "before execution."
            )

        payload = {
            "lane": lane_name,
            "decision": decision,
            "summary": summary.strip(),
            "rationale": rationale,
            "hard_gate_failures": reject_reasons,
            "commercial_holds": hold_reasons,
            "watch_items": sorted(watch_items),
            "factors": normalized,
            "notes": notes.strip(),
            "next_actions": guidance,
        }

        message = dedent(
            f"""\
            Revenue lane assessment:
            {json.dumps(payload, indent=2)}
            """
        ).strip()
        return Response(message=message, break_loop=False)
