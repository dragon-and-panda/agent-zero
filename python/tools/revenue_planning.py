from python.helpers.revenue_planning import assess_revenue_plan, format_assessment
from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        data_sources: str = "",
        consent_basis: str = "",
        monetization_target: str = "",
        notes: str = "",
        **kwargs,
    ):
        assessment = assess_revenue_plan(
            mission=mission,
            data_sources=data_sources,
            consent_basis=consent_basis,
            monetization_target=monetization_target,
            notes=notes,
        )
        return Response(message=format_assessment(assessment), break_loop=False)
