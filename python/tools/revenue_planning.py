import json

from python.helpers.revenue_planning import assess_revenue_plan
from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        data_sources: str = "",
        acquisition_method: str = "",
        monetization_plan: str = "",
        notes: str = "",
        **kwargs,
    ):
        assessment = assess_revenue_plan(
            objective=objective,
            data_sources=data_sources,
            acquisition_method=acquisition_method,
            monetization_plan=monetization_plan,
            notes=notes,
        )
        return Response(
            message=json.dumps(assessment, indent=2),
            break_loop=False,
        )
