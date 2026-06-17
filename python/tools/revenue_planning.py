from python.helpers.tool import Tool, Response


HARD_REJECT_PATTERNS = [
    "sell email",
    "sell emails",
    "email list",
    "contact list",
    "lead list",
    "scrape inbox",
    "scrape gmail",
    "gmail data",
    "broker data",
    "buy contacts",
    "resell contacts",
    "mass unsolicited",
    "spam",
]


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        lane: str = "",
        constraints: str = "",
        assets: str = "",
        **kwargs,
    ):
        mission_text = _normalize(mission)
        lane_text = _normalize(lane)
        constraint_text = _normalize(constraints)
        assets_text = _normalize(assets)
        combined = " ".join(
            part for part in [mission_text, lane_text, constraint_text, assets_text] if part
        )

        if any(pattern in combined for pattern in HARD_REJECT_PATTERNS):
            text = self.agent.read_prompt(
                "tool.revenue_planning.rejected.md",
                mission=mission or "(not provided)",
                lane=lane or "(not provided)",
                constraints=constraints or "(not provided)",
                assets=assets or "(not provided)",
            )
            return Response(message=text, break_loop=False)

        text = self.agent.read_prompt(
            "tool.revenue_planning.response.md",
            mission=mission or "(not provided)",
            lane=lane or "(not provided)",
            constraints=constraints or "(not provided)",
            assets=assets or "(not provided)",
        )
        await self.agent.handle_intervention(text)
        return Response(message=text, break_loop=False)
