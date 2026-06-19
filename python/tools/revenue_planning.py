from python.helpers.revenue_planning import build_revenue_plan, format_revenue_plan
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):

    async def execute(
        self,
        objective="",
        data_sources="",
        intended_actions="",
        constraints="",
        **kwargs,
    ):
        plan = build_revenue_plan(
            objective=objective,
            data_sources=data_sources,
            intended_actions=intended_actions,
            constraints=constraints,
        )
        return Response(message=format_revenue_plan(plan), break_loop=False)
