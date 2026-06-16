from python.helpers.revenue_planning import assess_revenue_plan, format_assessment
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        data_sources: str = "",
        monetization: str = "",
        delivery: str = "",
        constraints: str = "",
        **kwargs,
    ):
        assessment = assess_revenue_plan(
            mission=mission,
            data_sources=data_sources,
            monetization=monetization,
            delivery=delivery,
            constraints=constraints,
        )
        return Response(message=format_assessment(assessment), break_loop=False)
