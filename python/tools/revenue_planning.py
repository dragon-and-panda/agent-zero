from python.helpers.revenue_planning import assess_revenue_plan, format_assessment
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):

    async def execute(self, mission="", assets="", constraints="", **kwargs):
        assessment = assess_revenue_plan(
            mission=mission,
            assets=assets,
            constraints=constraints,
        )
        return Response(message=format_assessment(assessment), break_loop=False)
