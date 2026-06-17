from python.helpers.tool import Tool, Response


LOW = "low"
MEDIUM = "medium"
HIGH = "high"
VALID_LEVELS = {LOW, MEDIUM, HIGH}


def normalize_level(value: str, default: str = MEDIUM) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in VALID_LEVELS else default


class RevenuePlanning(Tool):
    async def execute(
        self,
        objective: str = "",
        offer_type: str = "",
        customer: str = "",
        acquisition_channel: str = "",
        fulfillment_mode: str = "",
        data_source: str = "",
        consent_model: str = "",
        legality: str = MEDIUM,
        platform_risk: str = MEDIUM,
        brand_risk: str = MEDIUM,
        setup_effort: str = MEDIUM,
        time_to_cash: str = MEDIUM,
        margin: str = MEDIUM,
        repeatability: str = MEDIUM,
        automation_fit: str = MEDIUM,
        defensibility: str = MEDIUM,
        notes: str = "",
        **kwargs,
    ):
        legality = normalize_level(legality)
        platform_risk = normalize_level(platform_risk)
        brand_risk = normalize_level(brand_risk)
        setup_effort = normalize_level(setup_effort)
        time_to_cash = normalize_level(time_to_cash)
        margin = normalize_level(margin)
        repeatability = normalize_level(repeatability)
        automation_fit = normalize_level(automation_fit)
        defensibility = normalize_level(defensibility)

        objective_text = (objective or "Unspecified objective").strip()
        offer_type_text = (offer_type or "Unspecified offer").strip()
        customer_text = (customer or "Unspecified customer").strip()
        acquisition_channel_text = (acquisition_channel or "Unspecified channel").strip()
        fulfillment_mode_text = (fulfillment_mode or "Unspecified fulfillment").strip()
        data_source_text = (data_source or "Unspecified data source").strip()
        consent_model_text = (consent_model or "Unspecified consent model").strip()
        notes_text = (notes or "").strip()

        rejection_reasons: list[str] = []
        hold_reasons: list[str] = []
        strengths: list[str] = []
        next_steps: list[str] = []

        if legality == LOW:
            rejection_reasons.append("Legality confidence is low.")
        elif legality == HIGH:
            strengths.append("Legality confidence is high.")

        consent_lower = consent_model_text.lower()
        if any(
            phrase in consent_lower
            for phrase in [
                "no consent",
                "without consent",
                "implied only",
                "scraped",
                "purchased list",
                "bought list",
                "brokered list",
            ]
        ):
            rejection_reasons.append("Consent model is non-consensual or depends on purchased/scraped contacts.")
        elif "opt-in" in consent_lower or "customer-owned" in consent_lower or "first-party" in consent_lower:
            strengths.append("Consent model appears first-party or opt-in.")
        else:
            hold_reasons.append("Consent model needs explicit confirmation that contact rights are first-party and opt-in.")

        data_source_lower = data_source_text.lower()
        if any(
            phrase in data_source_lower
            for phrase in [
                "gmail inboxes",
                "google email data",
                "scraped contacts",
                "email list",
                "third-party list",
                "brokered contacts",
                "resold contacts",
            ]
        ):
            rejection_reasons.append("Data source relies on personal inbox data or third-party contact resale.")
        elif any(phrase in data_source_lower for phrase in ["crm", "customer list", "first-party", "newsletter signups", "opt-in leads"]):
            strengths.append("Data source appears first-party and reusable.")
        else:
            hold_reasons.append("Data provenance is not yet clear enough for activation.")

        if platform_risk == HIGH:
            rejection_reasons.append("Platform risk is high.")
        elif platform_risk == MEDIUM:
            hold_reasons.append("Platform risk is moderate and needs a tighter operating procedure.")
        else:
            strengths.append("Platform risk is low.")

        if brand_risk == HIGH:
            hold_reasons.append("Brand risk is high enough to require manual review before launch.")

        if rejection_reasons:
            decision = "REJECT"
        else:
            low_soft_factors = []
            for label, value in [
                ("time_to_cash", time_to_cash),
                ("margin", margin),
                ("repeatability", repeatability),
                ("automation_fit", automation_fit),
                ("defensibility", defensibility),
            ]:
                if value == LOW:
                    low_soft_factors.append(label)

            if setup_effort == HIGH:
                hold_reasons.append("Setup effort is high.")
            if low_soft_factors:
                hold_reasons.append(
                    "Execution factors need improvement: " + ", ".join(low_soft_factors) + "."
                )

            decision = "PASS" if not hold_reasons else "HOLD"

        if decision == "REJECT":
            next_steps.extend(
                [
                    "Replace the model with a first-party, opt-in customer acquisition loop.",
                    "Remove any dependence on purchased, scraped, or brokered personal contact data.",
                    "Route the idea through docs/policies/compliance_pack.md before reconsideration.",
                ]
            )
        elif decision == "HOLD":
            next_steps.extend(
                [
                    "Clarify legality, consent, and data provenance in writing.",
                    "Tighten the offer so time-to-cash, margin, and repeatability are at least medium.",
                    "Pilot with a small, consented workflow before scaling automation.",
                ]
            )
        else:
            next_steps.extend(
                [
                    "Create a focused SOP and KPI dashboard for the lane.",
                    "Run a small pilot with budget, quality, and compliance checkpoints.",
                    "Save the winning workflow to memory and convert repeatable steps into instruments.",
                ]
            )

        lines = [
            f"Decision: {decision}",
            f"Objective: {objective_text}",
            f"Offer type: {offer_type_text}",
            f"Customer: {customer_text}",
            f"Acquisition channel: {acquisition_channel_text}",
            f"Fulfillment mode: {fulfillment_mode_text}",
            f"Data source: {data_source_text}",
            f"Consent model: {consent_model_text}",
            "",
            "Factor summary:",
            f"- legality: {legality}",
            f"- platform_risk: {platform_risk}",
            f"- brand_risk: {brand_risk}",
            f"- setup_effort: {setup_effort}",
            f"- time_to_cash: {time_to_cash}",
            f"- margin: {margin}",
            f"- repeatability: {repeatability}",
            f"- automation_fit: {automation_fit}",
            f"- defensibility: {defensibility}",
        ]

        if strengths:
            lines.extend(["", "Strengths:"])
            lines.extend(f"- {item}" for item in strengths)

        if rejection_reasons:
            lines.extend(["", "Rejection reasons:"])
            lines.extend(f"- {item}" for item in rejection_reasons)

        if hold_reasons:
            lines.extend(["", "Open risks:"])
            lines.extend(f"- {item}" for item in hold_reasons)

        lines.extend(["", "Recommended next steps:"])
        lines.extend(f"- {item}" for item in next_steps)

        if notes_text:
            lines.extend(["", "Notes:", notes_text])

        return Response(message="\n".join(lines), break_loop=False)
