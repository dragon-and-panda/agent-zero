import json

from python.helpers.tool import Tool, Response


SYSTEM_PROMPT = """You are a compliance-first revenue planning analyst.

Your job is to classify a proposed monetization lane and return strict JSON.

Hard rules:
- Reject any idea that depends on scraping, brokering, buying, selling, or sharing personal email addresses, inbox contents, or contact lists without explicit opt-in and ownership rights.
- Reject ideas that violate privacy law, anti-spam law, platform terms, data broker restrictions, or consent requirements.
- Reject regulated financial activity that is framed as autonomous live trading, wagering, laundering, or anything deceptive.
- Prefer lawful, ethical alternatives such as opt-in lead generation, first-party CRM enrichment, agency services, listing optimization, research products, analytics, or workflow automation for consenting clients.
- Keep recommendations practical and specific.

Return JSON only with this schema:
{
  "decision": "PASS" | "HOLD" | "REJECT",
  "summary": "short paragraph",
  "compliance": {
    "legal": "clear|mixed|blocked",
    "privacy": "clear|mixed|blocked",
    "consent": "clear|mixed|blocked",
    "tos": "clear|mixed|blocked"
  },
  "risks": ["..."],
  "approved_lane": "name of compliant lane or empty string",
  "next_steps": ["..."],
  "safer_alternatives": ["..."]
}
"""


class RevenuePlanning(Tool):

    async def execute(self, objective: str = "", context: str = "", **kwargs):
        if not objective.strip():
            return Response(
                message="objective is required.",
                break_loop=False,
            )

        message = (
            "Evaluate this monetization objective for a self-sustaining agentic system.\n\n"
            f"OBJECTIVE:\n{objective.strip()}\n\n"
            f"CONTEXT:\n{context.strip() or 'None provided.'}\n"
        )

        raw = await self.agent.call_utility_model(
            system=SYSTEM_PROMPT,
            message=message,
            background=False,
        )

        try:
            parsed = json.loads(raw)
            formatted = json.dumps(parsed, indent=2)
        except Exception:
            formatted = raw

        return Response(message=formatted, break_loop=False)
