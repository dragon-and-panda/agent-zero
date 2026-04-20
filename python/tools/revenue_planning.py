import json
import re

from python.helpers.tool import Response, Tool


APPROVED_SIGNAL_GROUPS = {
    "client_service": [
        "client-owned",
        "customer support",
        "crm",
        "inbox triage",
        "workflow automation",
        "lead qualification",
    ],
    "marketplace": [
        "listing",
        "marketplace",
        "resale",
        "seller",
        "productized service",
    ],
    "research": [
        "research report",
        "benchmark",
        "dataset",
        "analytics",
        "subscription",
        "advisory",
    ],
}

PROHIBITED_PATTERNS = {
    "personal_data_resale": [
        r"\bsell(?:ing)?\s+(?:an?\s+)?(?:email|contact|lead)\s+list",
        r"\bresell(?:ing)?\s+(?:personal\s+)?data",
        r"\bdata\s+broker(?:age)?\b",
        r"\bcompile\s+(?:an?\s+)?(?:email|contact|lead)\s+list\b",
    ],
    "non_consensual_collection": [
        r"\bharvest(?:ing)?\s+(?:emails|contacts|leads)\b",
        r"\bscrap(?:e|ing)\b.*\b(?:emails|contacts|inbox|gmail)\b",
        r"\bextract\b.*\b(?:emails|contacts)\b",
        r"\bcopy\b.*\b(?:gmail|inbox|contacts)\b",
    ],
    "spam_or_evasion": [
        r"\bcold\s+email\b",
        r"\bspam\b",
        r"\bcaptcha\s+solv(?:e|ing)\b",
        r"\bevad(?:e|ing)\b.*\b(?:tos|rate limit|detection)\b",
    ],
}

HIGH_RISK_DATA_SIGNALS = [
    "gmail",
    "google email",
    "inbox",
    "email",
    "contacts",
    "lead list",
    "contact list",
    "personal data",
]

STRONG_CONSENT_SIGNALS = [
    "opt-in",
    "consented",
    "user-owned",
    "client-owned",
    "first-party",
    "signed contract",
    "customer authorized",
]

SAFE_ALTERNATIVES = [
    "Convert inbox work into a client-owned inbox-to-CRM workflow that classifies messages and drafts responses without exporting third-party contacts.",
    "Package the autonomous listing service as a productized marketplace concierge for sellers with explicit platform-compliance checks.",
    "Build subscription research products from public, licensed, or first-party data instead of brokering personal information.",
    "Offer opt-in lead magnets, newsletters, or referral funnels where contacts consent before any outreach or monetization.",
]


class RevenuePlanning(Tool):
    async def execute(
        self,
        opportunity: str = "",
        customer: str = "",
        offer_type: str = "",
        acquisition_channels: str = "",
        data_sources: str = "",
        consent_basis: str = "",
        platform_constraints: str = "",
        notes: str = "",
        **kwargs,
    ):
        payload = {
            "opportunity": opportunity,
            "customer": customer,
            "offer_type": offer_type,
            "acquisition_channels": acquisition_channels,
            "data_sources": data_sources,
            "consent_basis": consent_basis,
            "platform_constraints": platform_constraints,
            "notes": notes,
        }
        combined = " ".join(value for value in payload.values() if value).lower()

        blocked_reasons = self._detect_blocked_reasons(combined)
        risks = self._detect_risks(combined, consent_basis.lower(), data_sources.lower())
        approved_lanes = self._detect_approved_lanes(combined)

        if blocked_reasons:
            status = "REJECT"
        elif risks:
            status = "HOLD"
        else:
            status = "APPROVE"

        result = {
            "status": status,
            "summary": self._build_summary(status, approved_lanes),
            "blocked_reasons": blocked_reasons,
            "risks": risks,
            "approved_lanes": approved_lanes,
            "required_checks": [
                "Confirm the revenue model is legal in the operating jurisdictions.",
                "Confirm data provenance, user authorization, and consent before using customer data.",
                "Confirm platform terms allow the workflow and no anti-abuse rules are being bypassed.",
            ],
            "safer_alternatives": SAFE_ALTERNATIVES,
            "next_step": self._next_step(status),
        }

        return Response(
            message=json.dumps(result, indent=2, sort_keys=True),
            break_loop=False,
        )

    def _detect_blocked_reasons(self, combined: str) -> list[str]:
        reasons: list[str] = []
        for label, patterns in PROHIBITED_PATTERNS.items():
            if any(re.search(pattern, combined) for pattern in patterns):
                reasons.append(self._blocked_reason_text(label))
        return reasons

    def _detect_risks(
        self, combined: str, consent_basis: str, data_sources: str
    ) -> list[str]:
        risks: list[str] = []

        uses_sensitive_data = any(signal in combined for signal in HIGH_RISK_DATA_SIGNALS)
        has_strong_consent = any(signal in consent_basis for signal in STRONG_CONSENT_SIGNALS)

        if uses_sensitive_data and not has_strong_consent:
            risks.append(
                "Sensitive customer data is referenced without a clear opt-in, client-owned, or otherwise authorized consent basis."
            )

        if any(word in data_sources for word in ["gmail", "inbox", "email"]) and "export" in combined:
            risks.append(
                "Inbox-derived data appears to be leaving the original business context; keep the workflow inside a client-owned CRM or support system."
            )

        if "scrape" in combined and "public" not in combined and "licensed" not in combined:
            risks.append(
                "The plan references scraping without establishing a licensed or platform-permitted data source."
            )

        if "affiliate" in combined and "disclosure" not in combined:
            risks.append(
                "Affiliate or referral revenue is mentioned without disclosure or platform-policy detail."
            )

        return risks

    def _detect_approved_lanes(self, combined: str) -> list[str]:
        lanes: list[str] = []
        for lane, signals in APPROVED_SIGNAL_GROUPS.items():
            if any(signal in combined for signal in signals):
                lanes.append(lane)
        return lanes

    def _blocked_reason_text(self, label: str) -> str:
        mapping = {
            "personal_data_resale": "The plan involves selling, reselling, or brokering personal contact data.",
            "non_consensual_collection": "The plan involves scraping or extracting inbox/contact data without a clear, lawful, user-authorized basis.",
            "spam_or_evasion": "The plan relies on spam, cold outreach without consent, or evasion of platform protections.",
        }
        return mapping[label]

    def _build_summary(self, status: str, approved_lanes: list[str]) -> str:
        if status == "REJECT":
            return "This monetization plan is blocked because it depends on personal-data resale, non-consensual collection, or platform abuse."
        if status == "HOLD":
            return "This idea may be viable, but it needs clearer consent, provenance, or platform-compliance details before execution."
        if approved_lanes:
            lane_list = ", ".join(approved_lanes)
            return f"This looks compatible with compliant autonomous revenue lanes: {lane_list}."
        return "This appears compliant based on the supplied details, but it should still pass legal, consent, and platform checks before launch."

    def _next_step(self, status: str) -> str:
        if status == "REJECT":
            return "Replace the blocked data-harvesting or resale component with an opt-in, client-owned, or public-data revenue model."
        if status == "HOLD":
            return "Clarify consent, provenance, and platform rules, then resubmit the plan for approval."
        return "Score the opportunity with the strategy instrument and turn it into a chartered program with explicit KPIs and guardrails."
