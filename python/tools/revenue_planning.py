from python.helpers.tool import Tool, Response


class RevenuePlanning(Tool):
    PROHIBITED_TERMS = (
        "sell email list",
        "sell email lists",
        "email list resale",
        "resell email",
        "resale contact",
        "broker email",
        "broker contacts",
        "harvest email",
        "harvest contacts",
        "compile email list",
        "scrape emails",
        "scrape email addresses",
        "buy email list",
        "buy contact list",
        "gmail dump",
    )

    PLATFORM_EVASION_TERMS = (
        "bypass captcha",
        "evade captcha",
        "evade detection",
        "bypass rate limit",
        "anti-bot",
        "stealth scrape",
    )

    AUTHORIZATION_TERMS = (
        "authorized",
        "authorised",
        "permission",
        "consent",
        "opt-in",
        "owned mailbox",
        "client-approved",
        "customer-approved",
        "first-party",
        "internal use",
    )

    def _contains_any(self, text: str, terms: tuple[str, ...]) -> bool:
        return any(term in text for term in terms)

    async def execute(
        self,
        mission: str = "",
        assets: str = "",
        constraints: str = "",
        audience: str = "",
        monetization: str = "",
        data_sources: str = "",
        **kwargs,
    ):
        combined = " ".join(
            [
                mission,
                assets,
                constraints,
                audience,
                monetization,
                data_sources,
            ]
        ).lower()

        hard_failures: list[str] = []
        warnings: list[str] = []
        lanes: list[str] = []

        if self._contains_any(combined, self.PROHIBITED_TERMS):
            hard_failures.append(
                "personal email harvesting, brokering, or list resale is prohibited"
            )

        if self._contains_any(combined, self.PLATFORM_EVASION_TERMS):
            hard_failures.append(
                "platform-evasion tactics are prohibited and make the lane non-viable"
            )

        touches_inbox = any(
            word in combined for word in ("gmail", "email", "inbox", "mailbox", "crm")
        )
        if touches_inbox:
            if self._contains_any(combined, self.AUTHORIZATION_TERMS):
                lanes.append("authorized inbox-to-crm assistant")
            else:
                warnings.append(
                    "email and inbox workflows require explicit authorization, internal-only use, and clear provenance"
                )

        if any(word in combined for word in ("listing", "marketplace", "seller", "listing service")):
            lanes.append("autonomous listing service")

        if any(word in combined for word in ("research", "report", "analysis", "intelligence")):
            lanes.append("research and intelligence products")

        if any(word in combined for word in ("newsletter", "opt-in", "lead magnet", "audience")):
            lanes.append("first-party opt-in audience system")

        if "orange" in combined:
            warnings.append(
                "orange-based analysis is acceptable only on permissioned or anonymized datasets"
            )

        if not lanes and not hard_failures:
            lanes.extend(
                [
                    "authorized client operations automation",
                    "research and intelligence products",
                ]
            )

        decision = "PASS"
        if hard_failures:
            decision = "REJECT"
        elif warnings:
            decision = "HOLD"

        safe_next_steps = [
            "record the lane in /a0/docs/strategy/incoming.md",
            "score the lane with /a0/instruments/strategy/score.sh",
            "follow /a0/docs/policies/compliance_pack.md before using inbox, contact, or marketplace data",
        ]

        if decision == "REJECT":
            safe_next_steps.extend(
                [
                    "replace contact-list resale with a first-party opt-in funnel or an authorized inbox-to-crm workflow",
                    "sell the software or service outcome, not the contact data",
                ]
            )
        elif decision == "HOLD":
            safe_next_steps.extend(
                [
                    "document who owns the data and what consent basis applies",
                    "limit outputs to internal crm, support, or opt-in audience operations",
                ]
            )
        else:
            safe_next_steps.extend(
                [
                    "define the narrowest sellable workflow and customer profile",
                    "instrument margin, repeatability, and automation coverage from the first iteration",
                ]
            )

        unique_lanes: list[str] = []
        for lane in lanes:
            if lane not in unique_lanes:
                unique_lanes.append(lane)

        lines = [
            f"decision: {decision}",
            "",
            "recommended lanes:",
        ]
        lines.extend(f"- {lane}" for lane in unique_lanes)

        if hard_failures:
            lines.append("")
            lines.append("hard failures:")
            lines.extend(f"- {item}" for item in hard_failures)

        if warnings:
            lines.append("")
            lines.append("warnings:")
            lines.extend(f"- {item}" for item in warnings)

        lines.append("")
        lines.append("next steps:")
        lines.extend(f"- {item}" for item in safe_next_steps)

        return Response(message="\n".join(lines), break_loop=False)
