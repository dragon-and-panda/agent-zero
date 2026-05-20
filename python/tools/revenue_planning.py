from dataclasses import dataclass

from python.helpers.tool import Response, Tool


VALID_LEVELS = {"low", "medium", "high"}


@dataclass
class RevenueDecision:
    outcome: str
    reasons: list[str]
    next_steps: list[str]


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        offer: str = "",
        customer: str = "",
        acquisition: str = "",
        delivery: str = "",
        data_sources: str = "",
        legality: str = "medium",
        consent: str = "medium",
        data_provenance: str = "medium",
        platform_risk: str = "medium",
        time_to_cash: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation_fit: str = "medium",
        defensibility: str = "medium",
        **kwargs,
    ):
        hard_gates = {
            "legality": self._normalize(legality, "legality"),
            "consent": self._normalize(consent, "consent"),
            "data_provenance": self._normalize(
                data_provenance, "data_provenance"
            ),
            "platform_risk": self._normalize(platform_risk, "platform_risk"),
        }
        soft_factors = {
            "time_to_cash": self._normalize(time_to_cash, "time_to_cash"),
            "margin": self._normalize(margin, "margin"),
            "repeatability": self._normalize(repeatability, "repeatability"),
            "automation_fit": self._normalize(automation_fit, "automation_fit"),
            "defensibility": self._normalize(defensibility, "defensibility"),
        }

        decision = self._assess(hard_gates=hard_gates, soft_factors=soft_factors)
        message = self._render(
            mission=mission,
            offer=offer,
            customer=customer,
            acquisition=acquisition,
            delivery=delivery,
            data_sources=data_sources,
            hard_gates=hard_gates,
            soft_factors=soft_factors,
            decision=decision,
        )
        return Response(message=message, break_loop=False)

    def _normalize(self, value: str, name: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in VALID_LEVELS:
            raise ValueError(
                f"{name} must be one of: low, medium, high. Got: {value!r}"
            )
        return normalized

    def _assess(
        self, hard_gates: dict[str, str], soft_factors: dict[str, str]
    ) -> RevenueDecision:
        reject_reasons: list[str] = []
        hold_reasons: list[str] = []

        if hard_gates["legality"] == "low":
            reject_reasons.append("legality is weak or clearly non-compliant")
        if hard_gates["consent"] == "low":
            reject_reasons.append("consent is absent or non-consensual")
        if hard_gates["data_provenance"] == "low":
            reject_reasons.append("data provenance is weak or unauthorized")
        if hard_gates["platform_risk"] == "high":
            reject_reasons.append("platform or terms-of-service risk is high")

        if reject_reasons:
            return RevenueDecision(
                outcome="REJECT",
                reasons=reject_reasons,
                next_steps=[
                    "Replace the lane with a first-party or client-authorized workflow.",
                    "Use public, licensed, or user-owned data only.",
                    "Rework acquisition around opt-in channels, partnerships, or content.",
                ],
            )

        if hard_gates["legality"] == "medium":
            hold_reasons.append("legality is not yet clearly validated")
        if hard_gates["consent"] == "medium":
            hold_reasons.append("consent basis is incomplete")
        if hard_gates["data_provenance"] == "medium":
            hold_reasons.append("data provenance needs clarification")
        if hard_gates["platform_risk"] == "medium":
            hold_reasons.append("platform risk needs mitigation")

        soft_high = 0
        soft_low = 0
        for level in soft_factors.values():
            if level == "high":
                soft_high += 1
            elif level == "low":
                soft_low += 1

        if soft_low > 0:
            hold_reasons.append("at least one execution factor is weak")
        if soft_high < 3:
            hold_reasons.append("fewer than three execution factors are strong")

        if hold_reasons:
            return RevenueDecision(
                outcome="HOLD",
                reasons=hold_reasons,
                next_steps=[
                    "Tighten the offer and document the lawful basis for data use.",
                    "Reduce platform dependency or move to official APIs and approved workflows.",
                    "Improve economics or repeatability before activating the lane.",
                ],
            )

        return RevenueDecision(
            outcome="PASS",
            reasons=[
                "hard gates are clear",
                "no execution factor is weak",
                "at least three execution factors are strong",
            ],
            next_steps=[
                "Start with a narrow pilot and capture unit economics.",
                "Instrument the lane with consent, provenance, and platform-compliance logs.",
                "Promote repeatable steps into tools or instruments after validation.",
            ],
        )

    def _render(
        self,
        mission: str,
        offer: str,
        customer: str,
        acquisition: str,
        delivery: str,
        data_sources: str,
        hard_gates: dict[str, str],
        soft_factors: dict[str, str],
        decision: RevenueDecision,
    ) -> str:
        lines = [
            "Revenue planning screen",
            "",
            f"Decision: {decision.outcome}",
            "",
            "Mission",
            f"- Mission: {mission or 'Not provided'}",
            f"- Offer: {offer or 'Not provided'}",
            f"- Customer: {customer or 'Not provided'}",
            f"- Acquisition: {acquisition or 'Not provided'}",
            f"- Delivery: {delivery or 'Not provided'}",
            f"- Data sources: {data_sources or 'Not provided'}",
            "",
            "Hard gates",
            f"- Legality: {hard_gates['legality']}",
            f"- Consent: {hard_gates['consent']}",
            f"- Data provenance: {hard_gates['data_provenance']}",
            f"- Platform risk: {hard_gates['platform_risk']}",
            "",
            "Execution factors",
            f"- Time to cash: {soft_factors['time_to_cash']}",
            f"- Margin: {soft_factors['margin']}",
            f"- Repeatability: {soft_factors['repeatability']}",
            f"- Automation fit: {soft_factors['automation_fit']}",
            f"- Defensibility: {soft_factors['defensibility']}",
            "",
            "Reasons",
        ]

        for reason in decision.reasons:
            lines.append(f"- {reason}")

        lines.extend(["", "Next steps"])
        for step in decision.next_steps:
            lines.append(f"- {step}")

        return "\n".join(lines)
