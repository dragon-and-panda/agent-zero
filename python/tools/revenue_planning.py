import re

from python.helpers.tool import Tool, Response

RATING_ORDER = {"low": 1, "medium": 2, "high": 3}
HARD_GATES = {
    "legality": "Legality",
    "consent": "Consent",
    "data_provenance": "Data provenance",
    "platform_compliance": "Platform compliance",
}
SOFT_FACTORS = {
    "time_to_cash": "Time to cash",
    "margin": "Margin",
    "repeatability": "Repeatability",
    "automation_fit": "Automation fit",
    "defensibility": "Defensibility",
}
POLICY_PATTERNS = (
    (
        re.compile(
            r"\b(sell|broker|rent|trade|resell).{0,40}\b(email|emails|contact list|mailing list|lead list)\b",
            re.IGNORECASE,
        ),
        "Personal email or contact-list resale is prohibited.",
    ),
    (
        re.compile(
            r"\b(scrape|harvest|extract|pull).{0,50}\b(gmail|inbox|mailbox|email account|contacts?)\b",
            re.IGNORECASE,
        ),
        "Inbox or contact harvesting needs explicit owner authorization and cannot be repurposed into list brokerage.",
    ),
    (
        re.compile(
            r"\b(cold email|bulk outreach|mass outreach|spam)\b",
            re.IGNORECASE,
        ),
        "Spam-oriented or non-consensual outreach is not an acceptable acquisition strategy.",
    ),
)


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission="",
        revenue_model="",
        data_sources="",
        channels="",
        legality="",
        consent="",
        data_provenance="",
        platform_compliance="",
        time_to_cash="",
        margin="",
        repeatability="",
        automation_fit="",
        defensibility="",
        notes="",
        **kwargs,
    ):
        combined_text = " ".join(
            [
                mission,
                revenue_model,
                data_sources,
                channels,
                notes,
            ]
        ).strip()
        policy_hits = self._policy_hits(combined_text)
        ratings = {
            "legality": self._normalize_rating(legality),
            "consent": self._normalize_rating(consent),
            "data_provenance": self._normalize_rating(data_provenance),
            "platform_compliance": self._normalize_rating(platform_compliance),
            "time_to_cash": self._normalize_rating(time_to_cash),
            "margin": self._normalize_rating(margin),
            "repeatability": self._normalize_rating(repeatability),
            "automation_fit": self._normalize_rating(automation_fit),
            "defensibility": self._normalize_rating(defensibility),
        }

        hard_failures = [
            HARD_GATES[key] for key in HARD_GATES if ratings[key] == "low"
        ]
        hard_cautions = [
            HARD_GATES[key] for key in HARD_GATES if ratings[key] == "medium"
        ]
        soft_lows = [
            SOFT_FACTORS[key] for key in SOFT_FACTORS if ratings[key] == "low"
        ]
        soft_high_count = sum(
            1 for key in SOFT_FACTORS if ratings[key] == "high"
        )

        decision = "PASS"
        reasons: list[str] = []
        next_actions: list[str] = []

        if policy_hits:
            decision = "REJECT"
            reasons.extend(policy_hits)
            next_actions.extend(
                [
                    "Replace the idea with a first-party product, opt-in funnel, or client-owned workflow.",
                    "If inbox data is involved, keep the output inside an authorized internal CRM or support process.",
                    "Do not export or sell contact data gathered from private communications.",
                ]
            )
        elif hard_failures:
            decision = "REJECT"
            reasons.append(
                "One or more hard gates are weak: " + ", ".join(hard_failures) + "."
            )
            next_actions.extend(
                [
                    "Redesign the lane until legality, consent, provenance, and platform compliance are strong.",
                    "Use only data with clear ownership and explicit permission.",
                ]
            )
        elif hard_cautions or soft_lows or soft_high_count < 3:
            decision = "HOLD"
            if hard_cautions:
                reasons.append(
                    "Hard gates are not yet strong enough: "
                    + ", ".join(hard_cautions)
                    + "."
                )
            if soft_lows:
                reasons.append(
                    "Execution quality is weak in: " + ", ".join(soft_lows) + "."
                )
            if soft_high_count < 3:
                reasons.append(
                    "Fewer than three soft factors are strong, so the lane is not compelling enough yet."
                )
            next_actions.extend(
                [
                    "Tighten consent, provenance, or platform fit before execution.",
                    "Improve economics or delivery mechanics before investing more automation effort.",
                ]
            )
        else:
            reasons.append(
                "All hard gates are strong and the lane clears the minimum execution-quality threshold."
            )
            next_actions.extend(
                [
                    "Run a narrow pilot with first-party or client-owned data only.",
                    "Log assumptions, customer value, and unit economics before scaling.",
                    "Keep exports minimal and auditable.",
                ]
            )

        message = self._build_message(
            mission=mission,
            revenue_model=revenue_model,
            data_sources=data_sources,
            channels=channels,
            notes=notes,
            ratings=ratings,
            decision=decision,
            reasons=reasons,
            next_actions=next_actions,
        )
        return Response(message=message, break_loop=False)

    def _normalize_rating(self, value: str) -> str:
        rating = str(value).strip().lower()
        if rating in RATING_ORDER:
            return rating
        return "medium"

    def _policy_hits(self, text: str) -> list[str]:
        hits: list[str] = []
        for pattern, explanation in POLICY_PATTERNS:
            if pattern.search(text):
                hits.append(explanation)
        return hits

    def _build_message(
        self,
        *,
        mission: str,
        revenue_model: str,
        data_sources: str,
        channels: str,
        notes: str,
        ratings: dict[str, str],
        decision: str,
        reasons: list[str],
        next_actions: list[str],
    ) -> str:
        lines = [
            "# Revenue planning screen",
            "",
            f"- Decision: {decision}",
            f"- Mission: {mission or 'Not provided'}",
            f"- Revenue model: {revenue_model or 'Not provided'}",
            f"- Data sources: {data_sources or 'Not provided'}",
            f"- Channels: {channels or 'Not provided'}",
        ]

        if notes:
            lines.append(f"- Notes: {notes}")

        lines.extend(
            [
                "",
                "## Hard gates",
            ]
        )
        for key, label in HARD_GATES.items():
            lines.append(f"- {label}: {ratings[key]}")

        lines.extend(
            [
                "",
                "## Soft execution factors",
            ]
        )
        for key, label in SOFT_FACTORS.items():
            lines.append(f"- {label}: {ratings[key]}")

        lines.extend(["", "## Why"])
        for reason in reasons:
            lines.append(f"- {reason}")

        lines.extend(["", "## Next actions"])
        for action in next_actions:
            lines.append(f"- {action}")

        if decision != "PASS":
            lines.extend(
                [
                    "",
                    "## Compliant pivots",
                    "- owner-authorized inbox intelligence for internal CRM or support use",
                    "- opt-in audience building instead of harvested-contact resale",
                    "- seller-authorized listing automation",
                    "- public-data or licensed research products",
                ]
            )

        return "\n".join(lines)
