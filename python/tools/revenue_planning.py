import json

from python.helpers.revenue_planning import build_revenue_plan
from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        revenue_model: str = "",
        data_source: str = "",
        owner_authorized: bool = False,
        consent_status: str = "unknown",
        data_provenance: str = "unknown",
        platform_risk: str = "medium",
        notes: str = "",
        **kwargs,
    ) -> Response:
        plan = build_revenue_plan(
            objective=objective,
            revenue_model=revenue_model,
            data_source=data_source,
            owner_authorized=owner_authorized,
            consent_status=consent_status,
            data_provenance=data_provenance,
            platform_risk=platform_risk,
            notes=notes,
        )
        return Response(message=json.dumps(plan, indent=2), break_loop=False)
