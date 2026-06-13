import json

from python.helpers.tool import Response, Tool


HARD_REJECT_TERMS = (
    "sell email list",
    "sell email lists",
    "resell email list",
    "resell email lists",
    "broker email list",
    "broker email lists",
    "cold email scraped",
    "scrape gmail",
    "scrape inbox",
    "scrape mailbox",
    "buy contact list",
    "sell contact list",
    "resell contact list",
    "data broker",
    "bypass captcha",
    "bypass rate limit",
)


class RevenuePlanning(Tool):

    async def execute(
        self,
        mission: str = "",
        lane: str = "",
        legality: str = "",
        consent: str = "",
        data_provenance: str = "",
        platform_terms: str = "",
        notes: str = "",
        **kwargs,
    ):
        mission_text = " ".join(
            part.strip()
            for part in [mission, lane, notes]
            if isinstance(part, str) and part.strip()
        ).lower()

        if self._has_hard_reject_term(mission_text):
            return Response(
                message=json.dumps(
                    {
                        "decision": "REJECT",
                        "reason": (
                            "The proposed lane relies on personal-data resale, "
                            "non-consensual extraction, or platform abuse."
                        ),
                        "recommended_reframe": [
                            "first-party inbox to CRM automation",
                            "opt-in lead capture funnels",
                            "client-owned sales operations automation",
                            "lawful marketplace listing services",
                            "research products built from public or licensed data",
                        ],
                    },
                    indent=2,
                ),
                break_loop=False,
            )

        factors = {
            "legality": legality,
            "consent": consent,
            "data_provenance": data_provenance,
            "platform_terms": platform_terms,
        }
        normalized = {key: self._normalize_level(value) for key, value in factors.items()}
        blocked = [key for key, value in normalized.items() if value == "weak"]
        caution = [key for key, value in normalized.items() if value == "unclear"]

        if blocked:
            decision = "REJECT"
            summary = (
                "One or more hard gates failed. Reframe the lane before implementation."
            )
        elif caution:
            decision = "HOLD"
            summary = (
                "The lane may be viable, but missing legal, consent, provenance, or "
                "platform clarity must be resolved before execution."
            )
        else:
            decision = "PASS"
            summary = (
                "The lane clears the initial compliance screen. Continue with small, "
                "reversible, consent-based experiments only."
            )

        response = {
            "decision": decision,
            "summary": summary,
            "lane": lane or mission,
            "gates": normalized,
            "next_steps": self._next_steps(decision),
        }
        if notes.strip():
            response["notes"] = notes.strip()

        return Response(message=json.dumps(response, indent=2), break_loop=False)

    def _has_hard_reject_term(self, text: str) -> bool:
        return any(term in text for term in HARD_REJECT_TERMS)

    def _normalize_level(self, value: str) -> str:
        text = (value or "").strip().lower()
        if text in {"strong", "clear", "yes", "pass", "good"}:
            return "strong"
        if text in {"weak", "no", "fail", "blocked"}:
            return "weak"
        return "unclear"

    def _next_steps(self, decision: str) -> list[str]:
        if decision == "REJECT":
            return [
                "stop implementation on this lane",
                "document why the lane failed legality, consent, provenance, or platform checks",
                "reframe the mission into an opt-in or first-party workflow",
            ]
        if decision == "HOLD":
            return [
                "gather written proof of consent and lawful access",
                "confirm platform terms and data provenance",
                "rerun the screen before any buildout or outreach",
            ]
        return [
            "score the lane for margin, repeatability, automation, and defensibility",
            "start with a reversible pilot using first-party data only",
            "log outcomes in the financial-system journal before scaling",
        ]
