import json

from python.helpers.tool import Tool, Response


VALID_LEVELS = {"low", "medium", "high"}


class RevenuePlanning(Tool):
    async def execute(
        self,
        opportunity_name: str = "",
        legality: str = "",
        consent: str = "",
        data_provenance: str = "",
        tos_alignment: str = "",
        time_to_cash: str = "",
        expected_margin: str = "",
        repeatability: str = "",
        automation_fit: str = "",
        defensibility: str = "",
        notes: str = "",
        **kwargs,
    ):
        factors = {
            "legality": legality,
            "consent": consent,
            "data_provenance": data_provenance,
            "tos_alignment": tos_alignment,
            "time_to_cash": time_to_cash,
            "expected_margin": expected_margin,
            "repeatability": repeatability,
            "automation_fit": automation_fit,
            "defensibility": defensibility,
        }

        invalid = sorted(
            factor_name
            for factor_name, value in factors.items()
            if value.lower() not in VALID_LEVELS
        )
        if invalid:
            return Response(
                message=(
                    "All factor values must be one of: low, medium, high. "
                    f"Invalid fields: {', '.join(invalid)}"
                ),
                break_loop=False,
            )

        normalized = {name: value.lower() for name, value in factors.items()}
        hard_fail_fields = [
            name
            for name in ("legality", "consent", "data_provenance", "tos_alignment")
            if normalized[name] == "low"
        ]
        hard_hold_fields = [
            name
            for name in ("legality", "consent", "data_provenance", "tos_alignment")
            if normalized[name] == "medium"
        ]
        soft_hold_fields = [
            name
            for name in (
                "time_to_cash",
                "expected_margin",
                "repeatability",
                "automation_fit",
                "defensibility",
            )
            if normalized[name] == "low"
        ]

        if hard_fail_fields:
            verdict = "REJECT"
            rationale = (
                "Hard gate failed on legality, consent, provenance, or platform rules."
            )
        elif hard_hold_fields:
            verdict = "HOLD"
            rationale = (
                "Compliance review is incomplete because at least one hard gate is only "
                "medium confidence."
            )
        elif soft_hold_fields:
            verdict = "HOLD"
            rationale = (
                "Compliance gates passed, but at least one commercial execution factor "
                "is too weak for autonomous activation."
            )
        else:
            verdict = "PASS"
            rationale = (
                "Compliance gates passed and no commercial execution factor is low."
            )

        payload = {
            "opportunity_name": opportunity_name or "Unnamed opportunity",
            "verdict": verdict,
            "rationale": rationale,
            "hard_fail_fields": hard_fail_fields,
            "hard_hold_fields": hard_hold_fields,
            "soft_hold_fields": soft_hold_fields,
            "factors": normalized,
            "notes": notes,
        }
        return Response(
            message=json.dumps(payload, indent=2, sort_keys=True),
            break_loop=False,
        )
