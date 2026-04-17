from python.helpers.tool import Tool, Response


REJECT_RULES = {
    "personal-data-resale": [
        "sell email list",
        "sell email lists",
        "email list",
        "email lists",
        "broker email",
        "broker emails",
        "resell contacts",
        "resell email",
        "resale of personal data",
        "contact list",
        "contact lists",
    ],
    "spam-or-unsolicited-outreach": [
        "spam",
        "cold email blast",
        "mass outreach",
        "unsolicited outreach",
    ],
    "credential-or-access-abuse": [
        "scrape inbox",
        "harvest inbox",
        "bypass",
        "credential",
        "phish",
        "impersonat",
    ],
}

CONSENT_SIGNALS = [
    "consent",
    "opt-in",
    "permission",
    "authorized",
    "owner",
    "first-party",
    "client-owned",
]

INBOX_SIGNALS = [
    "gmail",
    "google email",
    "google mail",
    "inbox",
    "mailbox",
    "email data",
]


class RevenuePlanning(Tool):

    async def execute(
        self,
        mission="",
        proposal="",
        data_sources="",
        monetization="",
        customer="",
        constraints="",
        **kwargs,
    ):
        text = self._normalize_text(
            mission,
            proposal,
            data_sources,
            monetization,
            customer,
            constraints,
        )
        constraints_text = self._normalize_text(constraints, proposal, mission)

        rejects: list[str] = []
        holds: list[str] = []
        approved: list[str] = []
        pivots: list[str] = []

        for rule_name, patterns in REJECT_RULES.items():
            if self._contains_any(text, patterns):
                rejects.append(self._reject_message(rule_name))

        uses_inbox_data = self._contains_any(text, INBOX_SIGNALS)
        has_consent = self._contains_any(constraints_text, CONSENT_SIGNALS)

        if uses_inbox_data and not has_consent:
            holds.append(
                "Inbox or email data requires explicit owner or client authorization before use."
            )

        if uses_inbox_data and has_consent:
            approved.append(
                "Mailbox data may be used only for the mailbox owner or an explicitly authorized client."
            )

        if self._contains_any(text, ["rag"]):
            approved.append(
                "RAG is acceptable for first-party retrieval, summarization, and workflow assistance."
            )

        if self._contains_any(text, ["sell", "broker", "resell"]) and uses_inbox_data:
            rejects.append(
                "Private inbox or contact data cannot be monetized through resale, brokerage, or list rental."
            )

        if rejects:
            verdict = "REJECT"
        elif holds:
            verdict = "HOLD"
        else:
            verdict = "PASS"

        pivots.extend(
            [
                "Use inbox RAG only to summarize a consenting owner's inbound demand and write CRM-ready records.",
                "Offer autonomous listing, merchandising, or content operations as a managed service.",
                "Package public or licensed data into a report, dashboard, or subscription product.",
                "Score candidate lanes with instruments/strategy/score.sh before activation.",
            ]
        )

        if verdict == "PASS":
            next_steps = [
                "Document the customer, consent path, and data provenance.",
                "Run instruments/strategy/score.sh and record the result in docs/strategy/incoming.md.",
                "Pilot on synthetic or first-party data before scaling.",
            ]
        elif verdict == "HOLD":
            next_steps = [
                "Resolve consent, provenance, or platform-policy gaps before touching real data.",
                "Rewrite the plan around first-party workflows and rescore it.",
                "Record the remediation plan in docs/strategy/incoming.md.",
            ]
        else:
            next_steps = [
                "Do not execute the current plan.",
                "Replace the personal-data resale component with a consent-based service or product lane.",
                "Use docs/policies/compliance_pack.md and docs/programs/agentic_financial_system/charter.md as the new baseline.",
            ]

        sections = [
            f"verdict: {verdict}",
            "",
            "approved findings:",
            self._render_list(approved or ["No special approvals noted."]),
            "",
            "blocking findings:",
            self._render_list(rejects or holds or ["No blocking findings."]),
            "",
            "recommended pivots:",
            self._render_list(pivots),
            "",
            "next steps:",
            self._render_list(next_steps),
        ]

        return Response(message="\n".join(sections), break_loop=False)

    def _normalize_text(self, *parts: str) -> str:
        return " ".join(part.strip().lower() for part in parts if isinstance(part, str))

    def _contains_any(self, text: str, patterns: list[str]) -> bool:
        return any(pattern in text for pattern in patterns)

    def _render_list(self, items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    def _reject_message(self, rule_name: str) -> str:
        mapping = {
            "personal-data-resale": "Personal contact data brokerage or email-list resale is prohibited.",
            "spam-or-unsolicited-outreach": "Spam or unsolicited bulk outreach is not an acceptable monetization lane.",
            "credential-or-access-abuse": "Access abuse, inbox harvesting, impersonation, or credential misuse is prohibited.",
        }
        return mapping[rule_name]
