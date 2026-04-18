import json

from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        market: str = "",
        customer: str = "",
        data_sources: str = "",
        acquisition_method: str = "",
        platform_rules: str = "",
        monetization_model: str = "",
        constraints: str = "",
        **kwargs,
    ):
        if not idea.strip():
            return Response(
                message="idea is required. Describe the proposed venture or monetization workflow.",
                break_loop=False,
            )

        normalized = {
            "idea": idea.strip(),
            "market": market.strip() or "unknown",
            "customer": customer.strip() or "unknown",
            "data_sources": data_sources.strip() or "unspecified",
            "acquisition_method": acquisition_method.strip() or "unspecified",
            "platform_rules": platform_rules.strip() or "unspecified",
            "monetization_model": monetization_model.strip() or "unspecified",
            "constraints": constraints.strip() or "unspecified",
        }

        text_blob = " ".join(normalized.values()).lower()

        hard_reject_terms = {
            "sell email list": "personal contact-data resale is prohibited",
            "email list": "personal contact-data resale requires consent and lawful provenance",
            "gmail": "third-party inbox access requires explicit authorization and approved use",
            "google email": "third-party inbox access requires explicit authorization and approved use",
            "scrape emails": "scraping personal contact data is prohibited",
            "harvest emails": "harvesting personal contact data is prohibited",
            "bulk outreach": "bulk outreach requires opt-in consent and platform compliance",
            "spam": "spam and deceptive outreach are prohibited",
            "credential": "credential access or exfiltration is prohibited",
            "broker leads": "lead brokerage without consent and provenance is prohibited",
        }

        reject_hits = []
        for term, reason in hard_reject_terms.items():
            if term in text_blob:
                reject_hits.append({"term": term, "reason": reason})

        legality = self._level(
            reject_hits,
            positive_markers=("first-party", "opt-in", "consent", "client-owned", "owned audience"),
            caution_markers=("unclear", "scrape", "third-party", "cold email", "marketplace automation"),
        )
        consent = self._level(
            reject_hits,
            positive_markers=("opt-in", "double opt-in", "subscriber", "customer requested"),
            caution_markers=("public data", "cold outreach", "scrape", "third-party inbox"),
        )
        provenance = self._level(
            reject_hits,
            positive_markers=("first-party", "crm", "customer provided", "owned content"),
            caution_markers=("public list", "unknown provenance", "broker", "harvest"),
        )
        platform = self._level(
            reject_hits,
            positive_markers=("api", "documented integration", "terms-compliant", "approved channel"),
            caution_markers=("automation", "headless", "relay", "unofficial", "captcha"),
        )

        execution_factors = {
            "time_to_cash": self._soft_level(
                text_blob,
                high_markers=("service", "consulting", "audit", "listing", "template", "retainer"),
                low_markers=("network effect", "marketplace liquidity", "research lab", "exchange"),
            ),
            "margin": self._soft_level(
                text_blob,
                high_markers=("software", "template", "digital", "service", "advisory"),
                low_markers=("resell", "inventory", "brokerage", "paid ads"),
            ),
            "repeatability": self._soft_level(
                text_blob,
                high_markers=("workflow", "playbook", "subscription", "productized service"),
                low_markers=("one-off", "custom only", "manual only"),
            ),
            "automation_fit": self._soft_level(
                text_blob,
                high_markers=("agent", "automation", "async", "queue", "playbook"),
                low_markers=("in-person", "manual only", "physical fulfillment"),
            ),
            "defensibility": self._soft_level(
                text_blob,
                high_markers=("proprietary process", "dataset", "workflow", "niche expertise"),
                low_markers=("commodity", "undifferentiated", "arbitrage only"),
            ),
        }

        blockers = []
        if reject_hits:
            blockers.extend(hit["reason"] for hit in reject_hits)
        if legality == "low":
            blockers.append("legal basis is weak or explicitly prohibited")
        if consent == "low":
            blockers.append("consent model is weak or absent")
        if provenance == "low":
            blockers.append("data provenance is weak or unlawful")
        if platform == "low":
            blockers.append("platform-rule fit is weak or likely disallowed")

        if blockers:
            verdict = "REJECT"
        elif "low" in execution_factors.values():
            verdict = "HOLD"
        else:
            verdict = "PASS"

        recommended_lanes = self._recommended_lanes(text_blob)
        if verdict == "REJECT":
            next_step = (
                "Replace the idea with an opt-in, first-party, or client-authorized workflow "
                "such as a listing service, research product, CRM enrichment for owned contacts, "
                "or a productized compliance-safe service."
            )
        elif verdict == "HOLD":
            next_step = (
                "Clarify consent, provenance, and platform constraints, then strengthen weak execution factors "
                "before activation."
            )
        else:
            next_step = (
                "Proceed with a small pilot, log metrics in the mission journal, and keep compliance checks active "
                "before scaling."
            )

        payload = {
            "verdict": verdict,
            "idea": normalized["idea"],
            "normalized_inputs": normalized,
            "hard_gates": {
                "legality": legality,
                "consent": consent,
                "data_provenance": provenance,
                "platform_fit": platform,
            },
            "execution_factors": execution_factors,
            "blockers": blockers,
            "recommended_lanes": recommended_lanes,
            "next_step": next_step,
        }
        return Response(
            message=json.dumps(payload, ensure_ascii=False, indent=2),
            break_loop=False,
        )

    def _level(
        self,
        reject_hits: list[dict[str, str]],
        positive_markers: tuple[str, ...],
        caution_markers: tuple[str, ...],
    ) -> str:
        if reject_hits:
            return "low"
        text = self.message.lower() + " " + " ".join(self.args.values()).lower()
        if any(marker in text for marker in caution_markers):
            return "medium"
        if any(marker in text for marker in positive_markers):
            return "high"
        return "medium"

    def _soft_level(
        self,
        text_blob: str,
        high_markers: tuple[str, ...],
        low_markers: tuple[str, ...],
    ) -> str:
        if any(marker in text_blob for marker in low_markers):
            return "low"
        if any(marker in text_blob for marker in high_markers):
            return "high"
        return "medium"

    def _recommended_lanes(self, text_blob: str) -> list[str]:
        lanes = []
        if "listing" in text_blob or "marketplace" in text_blob:
            lanes.append("Autonomous listing service for client-owned inventory")
        if "crm" in text_blob or "inbox" in text_blob or "email" in text_blob:
            lanes.append("Inbox-to-CRM enrichment for first-party, client-authorized contacts")
        if "research" in text_blob or "rag" in text_blob:
            lanes.append("Subscription research briefs or data products built from lawful sources")
        if not lanes:
            lanes.extend(
                [
                    "Productized compliance-safe service",
                    "First-party audience growth workflow",
                    "Research-backed niche software or template offering",
                ]
            )
        return lanes
