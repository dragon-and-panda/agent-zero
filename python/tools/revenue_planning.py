import json

from python.helpers.revenue_guardrails import evaluate_revenue_plan
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    """
    Screen monetization ideas for legality, consent, provenance, and commercial quality.
    """

    async def execute(
        self,
        idea: str = "",
        assets: str = "",
        data_sources: str = "",
        customer: str = "",
        outreach_method: str = "",
        notes: str = "",
        legality: str = "medium",
        consent: str = "medium",
        provenance: str = "medium",
        platform: str = "medium",
        time_to_cash: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation: str = "medium",
        defensibility: str = "medium",
        **kwargs,
    ) -> Response:
        payload = {
            "idea": idea,
            "assets": assets,
            "data_sources": data_sources,
            "customer": customer,
            "outreach_method": outreach_method,
            "notes": notes,
            "legality": legality,
            "consent": consent,
            "provenance": provenance,
            "platform": platform,
            "time_to_cash": time_to_cash,
            "margin": margin,
            "repeatability": repeatability,
            "automation": automation,
            "defensibility": defensibility,
        }
        result = evaluate_revenue_plan(payload)
        return Response(message=json.dumps(result, indent=2), break_loop=False)
