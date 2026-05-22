import re

from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    BLOCKED_CHECKS = (
        (
            "personal-data resale",
            (
                r"\b(sell|resell|broker|rent|monetiz(?:e|ing|ation))\b.{0,40}\b(email|contact|mailing)\s+lists?\b",
                r"\b(email|contact|mailing)\s+lists?\b.{0,40}\b(sell|resell|broker|rent|monetiz(?:e|ing|ation))\b",
                r"\bdata broker(?:age)?\b",
            ),
        ),
        (
            "harvested-contact acquisition",
            (
                r"\b(scrap(?:e|ing)|harvest|extract|compile|build)\b.{0,40}\b(email addresses?|contacts?|lead lists?)\b",
                r"\b(email addresses?|contacts?|lead lists?)\b.{0,40}\b(scrap(?:e|ing)|harvest|extract|compile)\b",
            ),
        ),
        (
            "non-consensual account or inbox access",
            (
                r"\bwithout consent\b",
                r"\bwithout permission\b",
                r"\bbypass\b.{0,30}\b(auth|authentication|login|captcha|rate limit|paywall)\b",
            ),
        ),
        (
            "spam-oriented outreach from scraped leads",
            (
                r"\b(cold email|bulk outreach|blast)\b.{0,40}\b(scrap(?:e|ing)|harvest|lead list|email list)\b",
                r"\b(scrap(?:e|ing)|harvest|lead list|email list)\b.{0,40}\b(cold email|bulk outreach|blast)\b",
            ),
        ),
    )

    def _normalize(self, *parts: str) -> str:
        joined = "\n".join(part for part in parts if part)
        return " ".join(joined.lower().split())

    def _contains_any(self, text: str, needles: tuple[str, ...]) -> bool:
        return any(needle in text for needle in needles)

    def _find_blockers(self, text: str) -> list[str]:
        failures: list[str] = []
        for label, patterns in self.BLOCKED_CHECKS:
            if any(re.search(pattern, text) for pattern in patterns):
                failures.append(label)
        return failures

    def _classify_lane(self, text: str) -> str:
        if self._contains_any(
            text,
            (
                "listing",
                "marketplace",
                "ebay",
                "etsy",
                "fb marketplace",
                "facebook marketplace",
            ),
        ):
            return "listing-service"
        if self._contains_any(
            text,
            (
                "newsletter",
                "lead magnet",
                "opt-in",
                "subscribe",
                "audience",
                "community",
            ),
        ):
            return "opt-in-audience"
        if self._contains_any(
            text,
            (
                "report",
                "research",
                "intelligence",
                "watchlist",
                "public data",
                "licensed data",
            ),
        ):
            return "research-product"
        if self._contains_any(
            text,
            (
                "gmail",
                "google email",
                "google workspace",
                "inbox",
                "mailbox",
                "crm",
                "rag",
                "follow-up",
            ),
        ):
            return "inbox-to-crm"
        return "general-service"

    def _has_authorization_signal(self, text: str) -> bool:
        return self._contains_any(
            text,
            (
                "authorized",
                "authorised",
                "consent",
                "first-party",
                "own mailbox",
                "internal",
                "client-authorized",
                "client authorised",
                "owner-authorized",
            ),
        )

    def _decision_for(self, lane: str, text: str, blockers: list[str]) -> tuple[str, list[str]]:
        reasons: list[str] = []
        if blockers:
            reasons.append(
                "The idea triggers blocked patterns: " + ", ".join(blockers) + "."
            )
            reasons.append(
                "This framework does not support monetization that depends on personal-data resale, harvested contacts, or non-consensual inbox access."
            )
            return "REJECT", reasons

        if lane == "listing-service":
            reasons.append(
                "Listing and marketplace automation can be monetized as a service or software layer without trading in personal data."
            )
            return "PASS", reasons

        if lane == "opt-in-audience":
            if self._contains_any(text, ("opt-in", "consent", "newsletter", "subscribe")):
                reasons.append(
                    "Opt-in audience building is a compliant monetization path when consent capture and unsubscribe controls are explicit."
                )
                return "PASS", reasons
            reasons.append(
                "Audience-driven monetization is viable, but the consent capture and delivery model are underspecified."
            )
            return "HOLD", reasons

        if lane == "research-product":
            if self._contains_any(text, ("public data", "licensed data", "licensed", "aggregated", "de-identified")):
                reasons.append(
                    "Research products built from public, licensed, aggregated, or de-identified data are compatible with the compliance pack."
                )
                return "PASS", reasons
            reasons.append(
                "Research can be a strong lane, but the data provenance needs to be made explicit before activation."
            )
            return "HOLD", reasons

        if lane == "inbox-to-crm":
            reasons.append(
                "Inbox and CRM automation is only acceptable as an internal first-party or explicitly client-authorized workflow."
            )
            reasons.append(
                "The monetizable asset should be the automation service, software, or managed workflow, not the underlying contact data."
            )
            if self._has_authorization_signal(text):
                return "PASS", reasons
            reasons.append(
                "Authorization, scope, and retention rules should be made explicit before this lane is activated."
            )
            return "HOLD", reasons

        reasons.append(
            "The idea is not clearly prohibited, but it needs a sharper monetization model, data provenance statement, and delivery path."
        )
        return "HOLD", reasons

    def _safer_alternatives(self, lane: str, blockers: list[str]) -> list[str]:
        if blockers:
            return [
                "Build an authorized inbox-to-CRM assistant for the mailbox owner instead of extracting contacts for resale.",
                "Create an opt-in newsletter or lead-magnet funnel so contacts are earned through consent.",
                "Package public-data or licensed-data research into a paid brief, watchlist, or service.",
            ]
        if lane == "inbox-to-crm":
            return [
                "Scope the workflow to owner-authorized Gmail or Google Workspace accounts only.",
                "Store only the minimum fields needed for CRM updates, reminders, or follow-up drafting.",
                "Use Orange or similar tools only on first-party or de-identified exports.",
            ]
        if lane == "listing-service":
            return [
                "Tie the lane to a defined listing vertical and service package.",
                "Instrument pricing, turnaround time, and conversion metrics from the start.",
            ]
        if lane == "research-product":
            return [
                "Write down the exact data sources and their license or public status.",
                "Package the output as a report, dashboard, subscription, or retained advisory workflow.",
            ]
        return [
            "Narrow the customer, data source, and revenue model.",
            "Run the idea through the score instrument before execution.",
        ]

    async def execute(
        self,
        idea: str = "",
        data_sources: str = "",
        constraints: str = "",
        goal: str = "",
        **kwargs,
    ):
        extras = [f"{key}: {value}" for key, value in kwargs.items() if value]
        normalized = self._normalize(idea, data_sources, constraints, goal, *extras)
        blockers = self._find_blockers(normalized)
        lane = self._classify_lane(normalized)
        decision, reasons = self._decision_for(lane, normalized, blockers)
        alternatives = self._safer_alternatives(lane, blockers)

        lines = [
            "Revenue planning assessment",
            "",
            f"Decision: {decision}",
            f"Primary lane: {lane}",
            "",
            "Why:",
        ]
        lines.extend(f"- {reason}" for reason in reasons)
        lines.extend(
            [
                "",
                "Guardrails:",
                "- Follow docs/policies/compliance_pack.md.",
                "- Do not monetize by selling personal data, scraped contact lists, or non-consensual inbox exports.",
                "- Keep Gmail, inbox, and CRM workflows first-party or explicitly client-authorized.",
            ]
        )

        if "orange" in normalized:
            lines.append(
                "- Orange-style analysis is allowed only on first-party, licensed, aggregated, or de-identified data."
            )

        lines.extend(["", "Safer or next-step paths:"])
        lines.extend(f"- {item}" for item in alternatives)
        lines.extend(
            [
                "",
                "Suggested next action:",
                "- Record the lane in docs/strategy/incoming.md.",
                "- Score it with instruments/strategy/score.sh before execution.",
                "- If the lane passes, continue with productizing the service or workflow instead of monetizing raw contact data.",
            ]
        )

        return Response(message="\n".join(lines), break_loop=False)
