import json
from dataclasses import dataclass

from python.helpers.tool import Tool, Response


REJECT_KEYWORDS = {
    "contact_list_sale": [
        "sell email list",
        "selling email list",
        "broker email list",
        "buy email list",
        "sell contact list",
        "broker contact list",
        "lead list for sale",
        "resell contacts",
        "resale of contacts",
    ],
    "non_consensual_harvesting": [
        "scrape emails",
        "harvest emails",
        "extract email addresses",
        "compile email addresses",
        "gmail scraping",
        "scrape inbox",
        "scrape mailbox",
        "data scraping from email",
    ],
    "spam_or_unsolicited_outreach": [
        "spam",
        "cold blast",
        "bulk unsolicited",
        "mass unsolicited email",
        "send unsolicited",
    ],
}

HIGH_RISK_KEYWORDS = {
    "regulated_finance": ["trading", "forex", "securities", "investment advice"],
    "mailbox_data": ["gmail", "google email", "mailbox", "inbox", "email data"],
    "personal_data": ["email addresses", "contacts", "personal data", "pii"],
}

SAFE_PIVOTS = [
    "Build an inbox-to-CRM assistant for the mailbox owner or a consenting client.",
    "Offer compliant first-party lead capture with opt-in forms, CRM hygiene, and deliverability tooling.",
    "Productize a listing optimization or marketplace automation service using seller-provided assets.",
    "Sell research products built from public, licensed, or client-owned datasets instead of personal contact data.",
]


@dataclass
class ScreeningResult:
    verdict: str
    summary: str
    hard_failures: list[str]
    warnings: list[str]
    required_controls: list[str]
    safer_alternatives: list[str]
    next_steps: list[str]


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        monetization_model: str = "",
        data_sources: str = "",
        consent_basis: str = "",
        acquisition_methods: str = "",
        platform_constraints: str = "",
        target_customer: str = "",
        notes: str = "",
        **kwargs,
    ):
        combined = "\n".join(
            [
                mission,
                monetization_model,
                data_sources,
                consent_basis,
                acquisition_methods,
                platform_constraints,
                target_customer,
                notes,
            ]
        ).lower()

        hard_failures = self._find_hard_failures(combined)
        warnings = self._find_warnings(
            combined=combined,
            mission=mission,
            monetization_model=monetization_model,
            data_sources=data_sources,
            consent_basis=consent_basis,
            platform_constraints=platform_constraints,
            target_customer=target_customer,
        )
        required_controls = self._required_controls(combined)
        safer_alternatives = self._safer_alternatives(combined)
        next_steps = self._next_steps(hard_failures, warnings, required_controls)

        if hard_failures:
            verdict = "REJECT"
            summary = (
                "This revenue idea conflicts with privacy, consent, or platform-compliance requirements."
            )
        elif warnings:
            verdict = "HOLD"
            summary = (
                "This idea may be viable, but key legality, consent, provenance, or go-to-market details are incomplete."
            )
        else:
            verdict = "PASS"
            summary = "This idea clears the initial screening with the documented controls."

        result = ScreeningResult(
            verdict=verdict,
            summary=summary,
            hard_failures=hard_failures,
            warnings=warnings,
            required_controls=required_controls,
            safer_alternatives=safer_alternatives,
            next_steps=next_steps,
        )

        return Response(
            message=json.dumps(result.__dict__, indent=2, ensure_ascii=True),
            break_loop=False,
        )

    def _find_hard_failures(self, combined: str) -> list[str]:
        failures: list[str] = []

        for category, keywords in REJECT_KEYWORDS.items():
            if any(keyword in combined for keyword in keywords):
                failures.append(category.replace("_", " "))

        if "sell" in combined and ("email" in combined or "contact" in combined or "list" in combined):
            failures.append("personal data resale")

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["mailbox_data"]) and not self._has_authorized_mailbox_language(combined):
            failures.append("mailbox access without explicit owner authorization")

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["personal_data"]) and "opt-in" not in combined and "consent" not in combined:
            failures.append("personal data usage without clear consent basis")

        return sorted(set(failures))

    def _find_warnings(
        self,
        *,
        combined: str,
        mission: str,
        monetization_model: str,
        data_sources: str,
        consent_basis: str,
        platform_constraints: str,
        target_customer: str,
    ) -> list[str]:
        warnings: list[str] = []

        if not mission.strip():
            warnings.append("mission is missing")
        if not monetization_model.strip():
            warnings.append("monetization model is missing")
        if not data_sources.strip():
            warnings.append("data sources are missing")
        if not consent_basis.strip():
            warnings.append("consent basis is missing")
        if not platform_constraints.strip():
            warnings.append("platform or legal constraints are missing")
        if not target_customer.strip():
            warnings.append("target customer is missing")

        if "public" not in combined and "licensed" not in combined and "client-owned" not in combined and "first-party" not in combined:
            warnings.append("data provenance is not clearly first-party, client-owned, public, or licensed")

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["regulated_finance"]):
            warnings.append("regulated finance work should stay simulation-first until risk controls are documented")

        return warnings

    def _required_controls(self, combined: str) -> list[str]:
        controls = [
            "Document the customer, offer, and success metric before execution.",
            "Record data provenance and retention limits for every dataset used.",
            "Check platform terms, local privacy law, and channel-specific outreach rules before launch.",
        ]

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["mailbox_data"]):
            controls.extend(
                [
                    "Use mailbox-owner OAuth or equivalent explicit authorization.",
                    "Limit mailbox processing to classification, summarization, CRM sync, or drafting for the authorized account.",
                    "Do not export, broker, or resell inbox contents or contact data.",
                ]
            )

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["regulated_finance"]):
            controls.extend(
                [
                    "Run the strategy in simulation first and require objective risk thresholds before live capital exposure.",
                    "Set reserve limits, logging, and manual halt conditions for any finance-adjacent automation.",
                ]
            )

        return controls

    def _safer_alternatives(self, combined: str) -> list[str]:
        alternatives = list(SAFE_PIVOTS)

        if any(keyword in combined for keyword in HIGH_RISK_KEYWORDS["mailbox_data"]):
            alternatives.insert(
                0,
                "Convert mailbox extraction ideas into an owner-authorized inbox operations product: search, summarize, triage, CRM sync, and follow-up drafting.",
            )

        return alternatives

    def _next_steps(
        self, hard_failures: list[str], warnings: list[str], required_controls: list[str]
    ) -> list[str]:
        if hard_failures:
            return [
                "Stop the current plan.",
                "Choose a compliant pivot from safer_alternatives.",
                "Rescreen the revised idea with explicit consent, provenance, and platform constraints.",
            ]

        if warnings:
            return [
                "Fill in the missing consent, provenance, and monetization details.",
                "Run the strategy scoring instrument after the hard-gate details are documented.",
                "Launch only after the required_controls are satisfied.",
            ]

        return [
            "Score the lane with instruments/strategy/score.sh before prioritizing it.",
            "Create a mission journal entry and define the first measurable experiment.",
            "Keep the required_controls attached to any execution plan.",
        ]

    def _has_authorized_mailbox_language(self, combined: str) -> bool:
        return any(
            phrase in combined
            for phrase in [
                "owner authorization",
                "mailbox owner authorization",
                "user-authorized",
                "user authorized",
                "consenting client",
                "oauth",
                "first-party",
            ]
        )
