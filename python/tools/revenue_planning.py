import json

from python.helpers.tool import Response, Tool


BLOCKING_PATTERNS = {
    "personal_data_resale": [
        "sell email list",
        "email list sale",
        "broker email list",
        "contact list sale",
        "data brokerage",
        "lead list resale",
        "resell contacts",
    ],
    "non_consensual_collection": [
        "scrape gmail",
        "scrape inbox",
        "harvest emails",
        "extract emails from inbox",
        "scrape contacts",
        "bypass consent",
    ],
    "spam_or_abuse": [
        "spam",
        "mass unsolicited outreach",
        "cold blast",
        "evade anti-spam",
        "avoid detection",
    ],
}


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        target_customer: str = "",
        offer: str = "",
        acquisition_channels: str = "",
        data_sources: str = "",
        consent_basis: str = "",
        platform_dependencies: str = "",
        notes: str = "",
        **kwargs,
    ):
        text_parts = [
            objective,
            target_customer,
            offer,
            acquisition_channels,
            data_sources,
            consent_basis,
            platform_dependencies,
            notes,
        ]
        text_blob = " ".join(part.strip().lower() for part in text_parts if part)

        blocking_issues = self._detect_blocking_issues(text_blob)
        missing_fields = self._missing_fields(
            objective=objective,
            offer=offer,
            acquisition_channels=acquisition_channels,
            data_sources=data_sources,
            consent_basis=consent_basis,
        )

        if blocking_issues:
            status = "reject"
            summary = "Rejected because the plan depends on privacy abuse, non-consensual data use, or spam-like monetization."
        elif missing_fields:
            status = "hold"
            summary = "Held because the plan is missing required legality, consent, or execution details."
        else:
            status = "pass"
            summary = "Plan is suitable for exploration if the stated controls are maintained."

        result = {
            "status": status,
            "summary": summary,
            "blocking_issues": blocking_issues,
            "missing_fields": missing_fields,
            "required_controls": [
                "document lawful data provenance",
                "document explicit consent or other valid authorization",
                "verify platform and API terms before execution",
                "avoid resale of personal data and unsolicited outreach",
                "keep an audit trail for data sources, channels, and permissions",
            ],
            "recommended_lanes": self._recommended_lanes(text_blob),
            "next_steps": self._next_steps(status),
        }

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=True),
            break_loop=False,
        )

    def _detect_blocking_issues(self, text_blob: str) -> list[str]:
        issues: list[str] = []
        for category, patterns in BLOCKING_PATTERNS.items():
            if any(pattern in text_blob for pattern in patterns):
                issues.append(category)
        return issues

    def _missing_fields(self, **fields: str) -> list[str]:
        return [name for name, value in fields.items() if not value.strip()]

    def _recommended_lanes(self, text_blob: str) -> list[dict[str, str]]:
        lanes = [
            {
                "name": "productized automation services",
                "why": "Fastest path to revenue using existing agent capabilities for real customers.",
                "example": "Workflow audits, support automation, reporting, or internal agent setup.",
            },
            {
                "name": "micro-saas tools",
                "why": "Turns repeatable service workflows into subscription revenue.",
                "example": "Proposal generators, internal knowledge assistants, or niche operations dashboards.",
            },
            {
                "name": "public or licensed research products",
                "why": "Monetizes agentic research without relying on private personal data.",
                "example": "Market maps, pricing monitors, or curated competitive intelligence digests.",
            },
        ]

        if "email" in text_blob or "gmail" in text_blob or "inbox" in text_blob:
            lanes.insert(
                0,
                {
                    "name": "authorized inbox intelligence",
                    "why": "Uses owned or authorized email data for internal insight generation instead of resale.",
                    "example": "Summarize inbound demand, extract product feedback, or route support themes.",
                },
            )

        return lanes

    def _next_steps(self, status: str) -> list[str]:
        if status == "reject":
            return [
                "Remove personal-data resale, scraping, or spam-dependent elements.",
                "Replace the plan with a consent-based customer acquisition or product strategy.",
                "Rescore the revised idea with the strategy instrument.",
            ]
        if status == "hold":
            return [
                "Fill in missing fields for offer, channels, data sources, and consent basis.",
                "Verify legality and platform terms for each dependency.",
                "Rescore after clarifying controls.",
            ]
        return [
            "Create an experiment brief with one offer, one customer segment, and one channel.",
            "Define success metrics, stop conditions, and compliance checkpoints.",
            "Log the idea in the strategy intake queue before launch.",
        ]
