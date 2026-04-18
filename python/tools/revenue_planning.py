from __future__ import annotations

from dataclasses import dataclass

from python.helpers.tool import Tool, Response


@dataclass(frozen=True)
class RevenueAssessment:
    decision: str
    legality: str
    consent: str
    data_provenance: str
    tos_alignment: str
    safety_notes: list[str]
    recommended_lane: str
    rationale: str


class RevenuePlanning(Tool):
    """
    Screen monetization ideas for legality, consent, and platform compatibility.
    """

    REJECT_TERMS = (
        "sell email list",
        "sell email lists",
        "email scraping",
        "scrape emails",
        "harvest emails",
        "gmail scraping",
        "bulk cold email",
        "spam campaign",
        "broker personal data",
        "resell contacts",
        "resale of email data",
    )
    HOLD_TERMS = (
        "trading bot",
        "financial trading",
        "brokerage",
        "loan underwriting",
        "healthcare data",
        "biometric",
        "credit decision",
    )

    async def execute(
        self,
        idea: str = "",
        assets: str = "",
        constraints: str = "",
        **kwargs,
    ) -> Response:
        assessment = self._assess_idea(
            idea=idea.strip(),
            assets=assets.strip(),
            constraints=constraints.strip(),
        )

        lines = [
            f"Decision: {assessment.decision}",
            f"Legality: {assessment.legality}",
            f"Consent: {assessment.consent}",
            f"Data provenance: {assessment.data_provenance}",
            f"Platform terms: {assessment.tos_alignment}",
            f"Recommended lane: {assessment.recommended_lane}",
            "",
            "Rationale:",
            assessment.rationale,
        ]

        if assessment.safety_notes:
            lines.extend(["", "Required guardrails:"])
            lines.extend(f"- {note}" for note in assessment.safety_notes)

        return Response(message="\n".join(lines).strip(), break_loop=False)

    def _assess_idea(
        self, idea: str, assets: str, constraints: str
    ) -> RevenueAssessment:
        normalized = " ".join([idea.lower(), assets.lower(), constraints.lower()])

        if any(term in normalized for term in self.REJECT_TERMS):
            return RevenueAssessment(
                decision="REJECT",
                legality="fails hard gate",
                consent="missing or explicitly violated",
                data_provenance="unclear or third-party personal data",
                tos_alignment="likely prohibited",
                safety_notes=[
                    "Do not scrape inboxes or compile personal contact dossiers.",
                    "Do not sell, rent, or transfer personal email addresses.",
                    "Pivot to opt-in lead capture, first-party CRM enrichment, or research products.",
                ],
                recommended_lane="opt-in lead generation or first-party services",
                rationale=(
                    "The proposal involves personal contact data brokerage or spam-like outreach. "
                    "That is incompatible with the legal, consent, and platform-rule guardrails "
                    "for this project."
                ),
            )

        if any(term in normalized for term in self.HOLD_TERMS):
            return RevenueAssessment(
                decision="HOLD",
                legality="potentially regulated",
                consent="needs tighter workflow design",
                data_provenance="must be documented before activation",
                tos_alignment="depends on provider and jurisdiction review",
                safety_notes=[
                    "Require explicit policy review and sandbox-only validation first.",
                    "Keep humans in the loop until objective risk metrics pass.",
                    "Document data sources, disclosures, and rollback conditions.",
                ],
                recommended_lane="sandboxed R&D or advisory product",
                rationale=(
                    "The idea may be lawful, but it touches a regulated or high-risk domain. "
                    "It should not run autonomously until policy, data provenance, and platform "
                    "constraints are fully documented."
                ),
            )

        recommended_lane = self._recommend_lane(normalized)
        return RevenueAssessment(
            decision="PASS",
            legality="appears compatible with lawful commerce",
            consent="compatible if limited to first-party or opt-in data",
            data_provenance="must remain first-party, consented, or public-domain",
            tos_alignment="requires platform-specific checks before execution",
            safety_notes=[
                "Use only consented, first-party, or public business data.",
                "Respect rate limits, anti-spam rules, and marketplace terms.",
                "Prefer products, services, or opt-in funnels over personal-data arbitrage.",
            ],
            recommended_lane=recommended_lane,
            rationale=(
                "The idea can fit the repo's financial-system objective if it stays within "
                "consent, provenance, and platform-rule boundaries. Treat those checks as "
                "mandatory before activation."
            ),
        )

    def _recommend_lane(self, normalized: str) -> str:
        if any(term in normalized for term in ("listing", "marketplace", "resale", "seller")):
            return "autonomous listing and seller operations"
        if any(term in normalized for term in ("newsletter", "community", "lead magnet", "crm")):
            return "opt-in audience capture and crm workflows"
        if any(term in normalized for term in ("research", "report", "dataset", "intel")):
            return "research products and subscription insights"
        return "productized service automation"
