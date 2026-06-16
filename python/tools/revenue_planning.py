import json
import re

from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    HARD_FIELDS = ("legality", "consent", "provenance", "tos")
    SOFT_FIELDS = ("time", "margin", "repeatability", "automation", "defensibility")
    HIGH_VALUES = {"high", "yes", "true", "clear", "allowed", "pass", "opt_in", "opt-in"}
    LOW_VALUES = {
        "low",
        "no",
        "false",
        "blocked",
        "reject",
        "scraped",
        "purchased",
        "unsolicited",
        "resale",
        "sell",
    }
    MEDIUM_VALUES = {"medium", "unknown", "unclear", "needs_review", "needs-review", "manual"}

    HARD_REJECT_RULES = (
        (
            "personal-data resale",
            r"(sell|broker|rent|trade).{0,40}(email|contact).{0,20}(list|lists|data)?"
            r"|"
            r"(email|contact).{0,20}(list|lists|data).{0,40}(sell|broker|rent|trade)",
        ),
        (
            "scraped or harvested contact acquisition",
            r"(scrape|harvest|extract|collect).{0,40}(email|gmail|inbox|contact)"
            r"|"
            r"(gmail|inbox).{0,40}(extract|harvest).{0,40}(email|contact)",
        ),
        (
            "unsolicited bulk outreach",
            r"\bspam\b|\bcold spam\b|\bunsolicited\b.{0,20}(outreach|email|messages?)",
        ),
        (
            "bypass or evasion language",
            r"(bypass|evade|work around).{0,30}(consent|oauth|authentication|terms|tos|policy)",
        ),
        (
            "unauthorized account or inbox access",
            r"without (authorization|consent|permission)|unauthorized access|stolen credentials",
        ),
    )

    POSITIVE_SIGNALS = {
        "legality": ("first-party", "customer-owned", "authorized export", "opt-in", "opted-in"),
        "consent": ("opt-in", "opted-in", "consented", "subscriber", "customer approved"),
        "provenance": ("first-party", "customer-owned", "owned crm", "owned inbox", "authorized export"),
        "tos": ("terms-compliant", "api approved", "documented integration", "authorized export"),
    }

    NEGATIVE_SIGNALS = {
        "consent": ("without consent", "no consent", "cold list", "purchased list"),
        "provenance": ("scraped", "harvested", "leaked", "brokered list", "third-party list"),
        "tos": ("bypass terms", "ignore terms", "stealth automation"),
    }

    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        data_sources: str = "",
        acquisition_plan: str = "",
        monetization_plan: str = "",
        delivery_plan: str = "",
        constraints_json: str = "",
        **kwargs,
    ):
        facts = self._parse_constraints(constraints_json)
        text_parts = [
            mission,
            assets,
            data_sources,
            acquisition_plan,
            monetization_plan,
            delivery_plan,
            json.dumps(facts, sort_keys=True) if facts else "",
        ]
        combined_text = " ".join(part for part in text_parts if part).lower()

        hard_failures = self._detect_hard_failures(combined_text, facts)
        scores = self._score_plan(combined_text, facts)
        verdict = self._decide(scores, hard_failures)

        result = {
            "verdict": verdict,
            "summary": self._summary_for(verdict),
            "hard_failures": hard_failures,
            "scores": scores,
            "allowed_next_steps": self._allowed_next_steps(verdict),
            "safe_alternatives": self._safe_alternatives(),
        }

        if verdict == "REJECT":
            result["disallowed_next_steps"] = [
                "Do not scrape, harvest, broker, or sell email/contact lists.",
                "Do not use inbox or account data without clear authorization and consent records.",
                "Do not run unsolicited bulk outreach or policy-evasion workflows.",
            ]

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=False),
            break_loop=False,
        )

    def _parse_constraints(self, constraints_json: str) -> dict:
        if not constraints_json:
            return {}
        try:
            data = json.loads(constraints_json)
        except json.JSONDecodeError as exc:
            return {"parse_error": f"Invalid constraints_json: {exc}"}
        if not isinstance(data, dict):
            return {"parse_error": "constraints_json must be a JSON object."}
        return data

    def _detect_hard_failures(self, text: str, facts: dict) -> list[str]:
        failures: list[str] = []
        for label, pattern in self.HARD_REJECT_RULES:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                failures.append(label)

        explicit_false_flags = {
            "authorized_access": "missing authorized access",
            "personal_data_resale": "personal-data resale enabled",
        }
        for key, label in explicit_false_flags.items():
            rating = self._normalize_rating(facts.get(key))
            if key == "authorized_access" and rating == "low":
                failures.append(label)
            if key == "personal_data_resale" and rating == "high":
                failures.append(label)

        if facts.get("parse_error"):
            failures.append("constraints_json parse error")

        return sorted(set(failures))

    def _score_plan(self, text: str, facts: dict) -> dict[str, str]:
        scores: dict[str, str] = {}

        for field in self.HARD_FIELDS:
            scores[field] = self._score_hard_field(field, text, facts)

        for field in self.SOFT_FIELDS:
            scores[field] = self._score_soft_field(field, text, facts)

        return scores

    def _score_hard_field(self, field: str, text: str, facts: dict) -> str:
        explicit = self._normalize_rating(facts.get(field))
        if explicit:
            return explicit

        if field == "consent":
            consent_status = self._normalize_rating(facts.get("consent_status"))
            if consent_status:
                return consent_status
        if field == "tos":
            tos_flag = self._normalize_rating(facts.get("tos_conflict"))
            if tos_flag == "low":
                return "low"
            if tos_flag == "high":
                return "high"

        for signal in self.NEGATIVE_SIGNALS.get(field, ()):
            if signal in text:
                return "low"

        for signal in self.POSITIVE_SIGNALS.get(field, ()):
            if signal in text:
                return "high"

        if field == "legality" and "sell" in text and ("email" in text or "contact" in text):
            return "low"
        if field == "provenance" and ("gmail" in text or "inbox" in text) and "authorized export" not in text:
            return "medium"
        return "medium"

    def _score_soft_field(self, field: str, text: str, facts: dict) -> str:
        explicit = self._normalize_rating(facts.get(field))
        if explicit:
            return explicit

        positive_map = {
            "time": ("existing customers", "existing inbox", "already have", "current pipeline"),
            "margin": ("software", "subscription", "digital report", "productized service"),
            "repeatability": ("template", "repeatable", "standardized", "batch"),
            "automation": ("automated", "agentic", "workflow", "pipeline"),
            "defensibility": ("proprietary", "first-party", "specialized", "domain expertise"),
        }
        negative_map = {
            "time": ("manual sourcing", "cold start", "no audience"),
            "margin": ("commodity", "low margin", "reseller"),
            "repeatability": ("one-off", "bespoke only"),
            "automation": ("manual only", "human-only"),
            "defensibility": ("easily copied", "undifferentiated"),
        }

        for signal in negative_map.get(field, ()):
            if signal in text:
                return "low"
        for signal in positive_map.get(field, ()):
            if signal in text:
                return "high"
        return "medium"

    def _decide(self, scores: dict[str, str], hard_failures: list[str]) -> str:
        if hard_failures:
            return "REJECT"

        if any(scores[field] == "low" for field in self.HARD_FIELDS):
            return "REJECT"

        if any(scores[field] != "high" for field in self.HARD_FIELDS):
            return "HOLD"

        if any(scores[field] == "low" for field in self.SOFT_FIELDS):
            return "HOLD"

        soft_high_count = sum(1 for field in self.SOFT_FIELDS if scores[field] == "high")
        if soft_high_count >= 3:
            return "PASS"
        return "HOLD"

    def _normalize_rating(self, value) -> str:
        if value is None:
            return ""
        normalized = str(value).strip().lower().replace(" ", "_")
        if normalized in self.HIGH_VALUES:
            return "high"
        if normalized in self.LOW_VALUES:
            return "low"
        if normalized in self.MEDIUM_VALUES:
            return "medium"
        return ""

    def _summary_for(self, verdict: str) -> str:
        if verdict == "REJECT":
            return "The plan crosses legal, privacy, or anti-spam boundaries and should not be executed."
        if verdict == "PASS":
            return "The plan clears hard compliance gates and looks attractive enough to execute."
        return "The plan is not rejected, but it needs clearer consent, provenance, terms validation, or stronger economics."

    def _allowed_next_steps(self, verdict: str) -> list[str]:
        if verdict == "PASS":
            return [
                "Proceed with a first-party, consented workflow.",
                "Document provenance, consent basis, and platform-policy checks.",
                "Build the smallest revenue-generating version and instrument results.",
            ]
        return [
            "Clarify consent, authorization, and data provenance before implementation.",
            "Prefer first-party CRM enrichment, opted-in audiences, or research products.",
            "Run the idea through the scoring instrument again after revising the plan.",
        ]

    def _safe_alternatives(self) -> list[dict[str, str]]:
        return [
            {
                "lane": "consented inbox-to-crm",
                "description": "Normalize customer-owned inbox exports into a first-party CRM using explicit consent records.",
            },
            {
                "lane": "opt-in lead magnet",
                "description": "Publish a useful asset and collect explicit subscriber opt-in before any outreach.",
            },
            {
                "lane": "autonomous listing service",
                "description": "Use the existing listing-service blueprint to productize a lawful operational workflow.",
            },
            {
                "lane": "research subscription",
                "description": "Sell benchmark reports, market maps, or playbooks built from lawful first-party or public data.",
            },
        ]
