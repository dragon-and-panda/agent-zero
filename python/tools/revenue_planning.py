import json

from python.helpers.tool import Response, Tool


HARD_REJECT_KEYWORDS = {
    "email_list_resale": (
        "sell email list",
        "sell email lists",
        "email list resale",
        "broker email lists",
        "contact list resale",
        "lead list resale",
        "rent email list",
        "data broker",
    ),
    "private_inbox_extraction": (
        "scrape gmail",
        "scrape inbox",
        "extract emails from gmail",
        "extract emails from inbox",
        "google email data",
        "gmail data",
        "mailbox scraping",
    ),
    "spam_or_deception": (
        "spam",
        "bulk unsolicited",
        "fake identity",
        "sock puppet",
        "phishing",
        "scam",
    ),
    "illegal_access": (
        "breach",
        "stolen data",
        "leaked data",
        "credential stuffing",
        "bypass access",
        "unauthorized access",
    ),
}

CAUTION_KEYWORDS = {
    "cold_outreach": ("cold email", "cold outreach", "cold dm"),
    "regulated_finance": ("trading bot", "autotrading", "lending", "securities", "wagering"),
}

POSITIVE_SIGNALS = {
    "authorized": (
        "opt in",
        "opt-in",
        "first party",
        "first-party",
        "owner authorized",
        "owner-authorized",
        "customer authorized",
        "customer-authorized",
        "client owned",
        "client-owned",
        "customer provided",
        "customer-provided",
        "consented",
    ),
    "public_or_documented": (
        "public data",
        "public business data",
        "documented provenance",
        "authorized source",
    ),
    "crm_lane": ("crm", "contact cleanup", "follow-up tasks", "mailbox triage", "inbox-to-crm"),
    "listing_lane": ("listing", "directory", "inventory syndication", "listing service"),
    "research_lane": ("research report", "market map", "intelligence brief", "monitoring"),
    "automation_lane": ("automation", "workflow", "agent", "pipeline"),
    "subscription_lane": ("subscription", "retainer", "saas", "template", "report"),
}


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        data_sources: str = "",
        acquisition_method: str = "",
        offer: str = "",
        monetization: str = "",
        customer: str = "",
        fulfillment: str = "",
        notes: str = "",
        **kwargs,
    ):
        fields = {
            "mission": mission,
            "data_sources": data_sources,
            "acquisition_method": acquisition_method,
            "offer": offer,
            "monetization": monetization,
            "customer": customer,
            "fulfillment": fulfillment,
            "notes": notes,
        }
        combined = " ".join(value.lower() for value in fields.values() if value).strip()

        hard_failures = self._detect_matches(combined, HARD_REJECT_KEYWORDS)
        cautions = self._detect_matches(combined, CAUTION_KEYWORDS)
        positives = self._detect_matches(combined, POSITIVE_SIGNALS)

        hard_gates = {
            "legality": "high",
            "consent": "medium",
            "provenance": "medium",
            "tos": "medium",
        }
        soft_scores = {
            "time": "medium",
            "margin": "medium",
            "repeatability": "medium",
            "automation": "medium",
            "defensibility": "medium",
        }

        if positives["authorized"]:
            hard_gates["consent"] = "high"
            hard_gates["provenance"] = "high"
            hard_gates["tos"] = "high"
            soft_scores["defensibility"] = "high"

        if positives["public_or_documented"]:
            hard_gates["consent"] = "high"
            hard_gates["provenance"] = "high"
            hard_gates["tos"] = "high"

        if positives["crm_lane"]:
            soft_scores["time"] = "high"
            soft_scores["automation"] = "high"

        if positives["listing_lane"]:
            soft_scores["time"] = "high"
            soft_scores["repeatability"] = "high"

        if positives["research_lane"]:
            soft_scores["margin"] = "high"
            soft_scores["repeatability"] = "high"

        if positives["automation_lane"]:
            soft_scores["automation"] = "high"

        if positives["subscription_lane"]:
            soft_scores["margin"] = "high"
            soft_scores["repeatability"] = "high"

        if any(hard_failures.values()):
            hard_gates["legality"] = "low"
            hard_gates["consent"] = "low"
            hard_gates["provenance"] = "low"
            hard_gates["tos"] = "low"

        if cautions["cold_outreach"] and hard_gates["consent"] != "high":
            hard_gates["consent"] = "low"
            hard_gates["tos"] = "low"

        if cautions["regulated_finance"]:
            soft_scores["time"] = "low"
            soft_scores["defensibility"] = "medium"

        decision = self._decide(hard_gates, soft_scores)
        recommended_lane = self._recommend_lane(positives)

        safer_alternatives = self._build_alternatives(hard_failures, recommended_lane)
        next_steps = self._build_next_steps(decision, recommended_lane)

        result = {
            "decision": decision,
            "recommended_lane": recommended_lane,
            "hard_gates": hard_gates,
            "soft_scores": soft_scores,
            "hard_failures": self._flatten_matches(hard_failures),
            "cautions": self._flatten_matches(cautions),
            "safe_signals": self._flatten_matches(positives),
            "safer_alternatives": safer_alternatives,
            "next_steps": next_steps,
        }

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=True),
            break_loop=False,
        )

    def _detect_matches(self, text: str, keyword_groups: dict[str, tuple[str, ...]]):
        matches: dict[str, list[str]] = {}
        for label, keywords in keyword_groups.items():
            matched = [keyword for keyword in keywords if keyword in text]
            matches[label] = matched
        return matches

    def _flatten_matches(self, matches: dict[str, list[str]]):
        return {label: values for label, values in matches.items() if values}

    def _decide(self, hard_gates: dict[str, str], soft_scores: dict[str, str]):
        if any(score != "high" for score in hard_gates.values()):
            return "REJECT"

        high_soft = sum(1 for score in soft_scores.values() if score == "high")
        has_low_soft = any(score == "low" for score in soft_scores.values())

        if not has_low_soft and high_soft >= 3:
            return "PASS"

        return "HOLD"

    def _recommend_lane(self, positives: dict[str, list[str]]):
        if positives["crm_lane"]:
            return "Inbox-to-CRM automation"
        if positives["listing_lane"]:
            return "Autonomous listing service"
        if positives["research_lane"]:
            return "Research and intelligence products"
        return "Needs manual scoping"

    def _build_alternatives(self, hard_failures: dict[str, list[str]], recommended_lane: str):
        alternatives = []

        if any(hard_failures.values()):
            alternatives.extend(
                [
                    "Convert private-email extraction into owner-authorized inbox-to-CRM cleanup.",
                    "Sell research, analytics, or workflow automation instead of raw contact data.",
                    "Use opt-in acquisition paths such as newsletters, waitlists, and customer-owned CRM lists.",
                ]
            )

        if recommended_lane == "Autonomous listing service":
            alternatives.append(
                "Package listing creation, enrichment, and monitoring as a repeatable service."
            )
        elif recommended_lane == "Research and intelligence products":
            alternatives.append(
                "Productize monitoring briefs, market maps, and opportunity reports on subscription."
            )
        elif recommended_lane == "Inbox-to-CRM automation":
            alternatives.append(
                "Use mailbox data only for the owner: triage, summaries, follow-up queues, and consent-aware CRM hygiene."
            )

        if not alternatives:
            alternatives.append(
                "Document provenance, consent, and terms before attempting activation."
            )

        return alternatives

    def _build_next_steps(self, decision: str, recommended_lane: str):
        if decision == "PASS":
            return [
                "Log the lane in docs/strategy/incoming.md and the journal.",
                "Run instruments/strategy/score.sh with explicit factor inputs before activation.",
                f"Draft a scoped offer for {recommended_lane.lower()}.",
            ]
        if decision == "HOLD":
            return [
                "Clarify consent, provenance, and platform-terms assumptions.",
                "Strengthen repeatability, automation fit, or margin before activation.",
                "Prefer first-party or client-authorized data sources.",
            ]
        return [
            "Do not execute the requested lane as written.",
            "Replace personal-data resale or private-data extraction with a compliant alternative.",
            "Use the compliance pack and charter to re-scope the mission.",
        ]
