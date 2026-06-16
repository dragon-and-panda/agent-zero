import json

from python.helpers.revenue_planning import evaluate_revenue_mission
from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    async def execute(self, mission: str = "", context: str = "", **kwargs):
        if not mission.strip():
            return Response(
                message="Error: mission is required.",
                break_loop=False,
            )

        result = evaluate_revenue_mission(mission=mission, context=context)
        payload = {
            "mission": mission,
            "context": context,
            **result,
        }
        return Response(
            message=json.dumps(payload, indent=2, ensure_ascii=False),
            break_loop=False,
        )
