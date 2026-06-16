from python.helpers.revenue_planning import (
    evaluate_revenue_plan,
    format_assessment_markdown,
)
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):

    async def execute(
        self,
        mission: str = "",
        revenue_model: str = "",
        data_sources: str = "",
        operating_constraints: str = "",
        **kwargs,
    ):
        assessment = evaluate_revenue_plan(
            mission=mission,
            revenue_model=revenue_model,
            data_sources=data_sources,
            operating_constraints=operating_constraints,
        )
        return Response(
            message=format_assessment_markdown(assessment),
            break_loop=False,
        )
