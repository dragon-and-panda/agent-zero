from agent import LoopData
from python.helpers.extension import Extension


class RevenueGuardrails(Extension):

    async def execute(
        self,
        system_prompt: list[str] = [],
        loop_data: LoopData = LoopData(),
        **kwargs,
    ):
        system_prompt.insert(
            0,
            self.agent.read_prompt("agent.system.revenue_guardrails.md"),
        )
