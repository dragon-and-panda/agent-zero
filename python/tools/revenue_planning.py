import json
from textwrap import dedent

from python.helpers.tool import Tool, Response


BLOCKED_SIGNALS = (
    "sell email list",
    "email list",
    "contact list",
    "gmail data",
    "google email data",
    "inbox scraping",
    "scrape emails",
    "bulk cold outreach",
    "spam",
    "data broker",
)


COMPLIANT_ALTERNATIVES = [
    "first-party CRM workflow automation",
    "opt-in lead magnet and newsletter funnel",
    "public-data market research product",
    "listing and merchandising automation service",
    "internal tool or managed workflow sold to businesses",
]


class RevenuePlanning(Tool):

    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        constraints: str = "",
        **kwargs,
    ):
        mission_text = mission.strip()
        assets_text = assets.strip()
        constraints_text = constraints.strip()

        if not mission_text:
            return Response(
                message="mission is required.",
                break_loop=False,
            )

        if self._is_blocked(mission_text, assets_text, constraints_text):
            return Response(
                message=self._blocked_response(mission_text),
                break_loop=False,
            )

        scorecard = self._score(mission_text, assets_text, constraints_text)
        return Response(
            message=json.dumps(scorecard, indent=2),
            break_loop=False,
        )

    def _is_blocked(self, *texts: str) -> bool:
        haystack = " ".join(texts).lower()
        return any(signal in haystack for signal in BLOCKED_SIGNALS)

    def _score(self, mission: str, assets: str, constraints: str) -> dict[str, object]:
        mission_lower = mission.lower()
        assets_lower = assets.lower()
        constraints_lower = constraints.lower()

        legality = 5
        consent = 5
        tos_fit = 4
        speed = 3
        margin = 3
        repeatability = 3
        automation = 3
        defensibility = 2
        reputation = 4

        if any(token in mission_lower for token in ("opt-in", "newsletter", "subscriber", "crm", "first-party", "listing", "workflow", "research")):
            legality = 5
            consent = 5
            tos_fit = 5

        if any(token in mission_lower for token in ("service", "agency", "managed", "automation")):
            speed += 1
            margin += 1
            automation += 1

        if any(token in mission_lower for token in ("software", "tool", "saas", "productized")):
            repeatability += 1
            defensibility += 1

        if any(token in assets_lower for token in ("existing audience", "customer list", "website traffic", "inventory", "product catalog", "crm")):
            speed += 1
            repeatability += 1

        if any(token in constraints_lower for token in ("no budget", "low budget", "manual")):
            speed -= 1
            automation -= 1

        metrics = {
            "legality": self._clamp(legality),
            "consent": self._clamp(consent),
            "tos_fit": self._clamp(tos_fit),
            "time_to_cash": self._clamp(speed),
            "margin": self._clamp(margin),
            "repeatability": self._clamp(repeatability),
            "automation": self._clamp(automation),
            "defensibility": self._clamp(defensibility),
            "reputation_risk": self._clamp(reputation),
        }

        soft_values = [
            metrics["time_to_cash"],
            metrics["margin"],
            metrics["repeatability"],
            metrics["automation"],
            metrics["defensibility"],
        ]

        if min(metrics["legality"], metrics["consent"], metrics["tos_fit"]) <= 2:
            decision = "REJECT"
        elif min(soft_values) <= 2:
            decision = "HOLD"
        else:
            decision = "PASS"

        next_steps = [
            "Document provenance, consent, and operator authority before execution.",
            "Start with first-party or opt-in data only.",
            "Pilot the lane with one narrow offer and measure conversion, fulfillment time, and gross margin.",
            "Record the result in docs/programs/agentic_financial_system/journal.md.",
        ]

        return {
            "decision": decision,
            "mission": mission,
            "assets": assets,
            "constraints": constraints,
            "metrics": metrics,
            "recommended_lanes": self._recommended_lanes(mission.lower()),
            "next_steps": next_steps,
        }

    def _blocked_response(self, mission: str) -> str:
        payload = {
            "decision": "REJECT",
            "mission": mission,
            "reason": "The requested lane involves personal-data extraction, contact-list brokerage, spam enablement, or another prohibited monetization pattern.",
            "allowed_alternatives": COMPLIANT_ALTERNATIVES,
            "policy_summary": dedent(
                """
                Reject any workflow involving inbox scraping, resale of personal contact lists,
                unauthorized enrichment, or non-consensual outreach. Reframe toward first-party,
                opt-in, public-data, or workflow-automation revenue lanes.
                """
            ).strip(),
        }
        return json.dumps(payload, indent=2)

    def _recommended_lanes(self, mission_lower: str) -> list[str]:
        lanes = []
        if "listing" in mission_lower or "marketplace" in mission_lower:
            lanes.append("Autonomous listing and merchandising service")
        if "research" in mission_lower or "data" in mission_lower:
            lanes.append("Public-data research briefs and competitive intelligence")
        if "workflow" in mission_lower or "automation" in mission_lower:
            lanes.append("Managed workflow automation for first-party operators")
        if "audience" in mission_lower or "newsletter" in mission_lower:
            lanes.append("Opt-in content funnel with newsletter and paid upsell")
        if not lanes:
            lanes.extend(
                [
                    "Managed workflow automation for first-party operators",
                    "Opt-in content funnel with newsletter and paid upsell",
                    "Public-data research briefs and competitive intelligence",
                ]
            )
        return lanes

    def _clamp(self, value: int) -> int:
        return max(1, min(5, value))
