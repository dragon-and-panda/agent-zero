import json

from python.helpers.tool import Tool, Response


LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2}
HARD_FACTORS = ("legality", "consent", "provenance", "platform_fit")
SOFT_FACTORS = ("time", "margin", "repeatability", "automation", "defensibility")
ALL_FACTORS = HARD_FACTORS + SOFT_FACTORS


def normalize_level(value: str, default: str = "medium") -> str:
    value = (value or "").strip().lower()
    return value if value in LEVEL_ORDER else default


def worse_level(current: str, candidate: str) -> str:
    return candidate if LEVEL_ORDER[candidate] < LEVEL_ORDER[current] else current


def better_level(current: str, candidate: str) -> str:
    return candidate if LEVEL_ORDER[candidate] > LEVEL_ORDER[current] else current


def load_ratings_json(raw: str) -> dict[str, str]:
    if not raw.strip():
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("ratings_json must decode to a JSON object.")
    ratings: dict[str, str] = {}
    for key, value in data.items():
        if key in ALL_FACTORS and isinstance(value, str):
            ratings[key] = normalize_level(value)
    return ratings


def compute_decision(factors: dict[str, str]) -> tuple[str, str]:
    for key in HARD_FACTORS:
        if factors[key] == "low":
            return "REJECT", "At least one hard gate failed."

    for key in HARD_FACTORS:
        if factors[key] == "medium":
            return "HOLD", "A hard gate is still uncertain."

    soft_high_count = 0
    for key in SOFT_FACTORS:
        if factors[key] == "low":
            return "HOLD", "The lane is compliant but weak on at least one execution factor."
        if factors[key] == "high":
            soft_high_count += 1

    if soft_high_count < 3:
        return "HOLD", "The lane is compliant but not yet compelling enough to activate."

    return "PASS", "Hard gates are clear and the lane is attractive enough to activate."


def safer_alternatives(text: str) -> list[str]:
    text = text.lower()
    alternatives = []

    if any(phrase in text for phrase in ("email list", "contact list", "lead list", "gmail", "inbox")):
        alternatives.extend(
            [
                "Use authorized inbox-to-CRM extraction for the mailbox owner's internal operations.",
                "Build opt-in lead magnets or newsletter funnels instead of brokering contacts.",
                "Sell productized research, workflows, or listings services rather than raw personal data.",
            ]
        )

    if any(phrase in text for phrase in ("scrape", "harvest", "spam", "cold email")):
        alternatives.append(
            "Switch to first-party, opt-in, or client-provided data sources with documented consent."
        )

    if any(phrase in text for phrase in ("trade", "trading", "crypto", "forex", "stocks", "securities")):
        alternatives.append(
            "Keep finance-adjacent ideas in simulation until compliance, reserve thresholds, and licensing needs are clear."
        )

    if not alternatives:
        alternatives.extend(
            [
                "Favor opt-in, first-party, or client-authorized workflows.",
                "Prefer productized services, subscriptions, or software over raw data resale.",
            ]
        )

    return alternatives


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        target_customer: str = "",
        assets: str = "",
        data_sources: str = "",
        acquisition_method: str = "",
        monetization_model: str = "",
        execution_notes: str = "",
        ratings_json: str = "",
        **kwargs,
    ):
        if not idea.strip():
            return Response(message="idea is required.", break_loop=False)

        try:
            provided_ratings = load_ratings_json(ratings_json)
        except ValueError as exc:
            return Response(message=str(exc), break_loop=False)
        except json.JSONDecodeError as exc:
            return Response(message=f"Invalid ratings_json: {exc}", break_loop=False)

        factors = {factor: "medium" for factor in ALL_FACTORS}
        reasons: list[str] = []

        for key, value in provided_ratings.items():
            factors[key] = value
        if provided_ratings:
            reasons.append("Applied caller-provided factor ratings from ratings_json.")

        combined = " ".join(
            [
                idea,
                target_customer,
                assets,
                data_sources,
                acquisition_method,
                monetization_model,
                execution_notes,
            ]
        ).lower()

        def downgrade(key: str, level: str, reason: str):
            previous = factors[key]
            factors[key] = worse_level(previous, level)
            if factors[key] != previous and reason not in reasons:
                reasons.append(reason)

        def upgrade(key: str, level: str, reason: str):
            previous = factors[key]
            factors[key] = better_level(previous, level)
            if factors[key] != previous and reason not in reasons:
                reasons.append(reason)

        if any(
            phrase in combined
            for phrase in (
                "sell email list",
                "sell contact list",
                "sell lead list",
                "broker email list",
                "rent email list",
                "trade email list",
                "email list brokerage",
                "contact list brokerage",
                "resell contacts",
            )
        ):
            for key in HARD_FACTORS:
                downgrade(key, "low", "Raw personal-contact resale is prohibited.")

        if (
            any(phrase in combined for phrase in ("gmail", "inbox", "mailbox", "contacts", "address book"))
            and any(phrase in combined for phrase in ("scrape", "harvest", "extract all", "dump", "broker", "resell", "sell"))
        ):
            for key in HARD_FACTORS:
                downgrade(
                    key,
                    "low",
                    "Inbox- or account-derived harvesting for resale or mass outreach is not allowed.",
                )

        if any(
            phrase in combined
            for phrase in (
                "without consent",
                "without permission",
                "unauthorized",
                "evade tos",
                "bypass captcha",
                "stealth automation",
                "exfiltrate",
                "breach",
                "leaked data",
            )
        ):
            for key in HARD_FACTORS:
                downgrade(key, "low", "Unauthorized or evasive workflows fail the hard gates.")

        if any(phrase in combined for phrase in ("spam", "cold blast", "mass cold email", "unsolicited outreach")):
            downgrade("consent", "low", "Spam or unsolicited outreach fails the consent gate.")
            downgrade("platform_fit", "low", "Spam-like tactics create platform-compliance risk.")

        if any(phrase in combined for phrase in ("opt-in", "inbound", "newsletter", "waitlist", "customer-provided")):
            upgrade("consent", "high", "The idea uses opt-in or customer-provided acquisition.")
            upgrade("provenance", "high", "The data provenance appears explainable and permissioned.")

        if any(phrase in combined for phrase in ("first-party", "authorized inbox", "authorized mailbox", "own inbox", "own mailbox")):
            upgrade("legality", "high", "The workflow appears to use authorized first-party data.")
            upgrade("consent", "high", "The workflow appears to stay within first-party consent boundaries.")
            upgrade("provenance", "high", "The data source is user-owned or explicitly authorized.")
            upgrade("platform_fit", "high", "Internal productivity use is more compatible with platform rules.")

        if "crm" in combined and any(phrase in combined for phrase in ("authorized", "first-party", "own inbox", "own mailbox", "customer-provided", "opt-in")):
            upgrade("repeatability", "high", "Inbox-to-CRM operations are repeatable once scoped to authorized data.")
            upgrade("automation", "high", "Structured extraction into CRM is automation-friendly.")
            upgrade("time", "high", "First-party workflow automation can validate quickly.")

        if any(phrase in combined for phrase in ("research", "report", "market map", "competitive intelligence", "pricing brief", "newsletter")):
            upgrade("legality", "high", "Productized knowledge work is usually compliant when sources are lawful.")
            upgrade("platform_fit", "high", "Research products are typically platform-compatible.")
            upgrade("margin", "medium", "Research products can support moderate to strong margins.")
            upgrade("defensibility", "medium", "Repeated synthesis can become defensible with process and archives.")

        if any(phrase in combined for phrase in ("listing", "inventory", "marketplace", "resale service", "seller")):
            upgrade("consent", "high", "Seller-provided inventory workflows are consent-aligned.")
            upgrade("provenance", "high", "Client-provided listing data has clear provenance.")
            upgrade("automation", "medium", "Listing operations can be partially automated.")
            upgrade("repeatability", "medium", "Listing workflows are reusable across sellers and channels.")

        if any(phrase in combined for phrase in ("public data", "licensed data", "client-provided", "customer-owned")):
            upgrade("provenance", "high", "The data source appears public, licensed, or client-provided.")

        if any(phrase in combined for phrase in ("scraped data", "bought list", "brokered data", "unknown source")):
            downgrade("provenance", "low", "The data source lacks clear provenance.")

        if any(phrase in combined for phrase in ("trade", "trading", "crypto", "forex", "stocks", "securities", "hedge fund")):
            upgrade("margin", "medium", "Finance-adjacent ideas can be lucrative if compliant.")
            downgrade("legality", "medium", "Finance-adjacent automation needs explicit compliance review.")
            downgrade("platform_fit", "medium", "Execution risk is higher in regulated or TOS-sensitive environments.")
            downgrade("time", "low", "A safe rollout should stay in simulation first.")
            if not any(phrase in combined for phrase in ("simulation", "simulated", "paper trade", "paper trading")):
                reasons.append("Keep finance-adjacent lanes in simulation until compliance and risk controls are defined.")

        if any(phrase in combined for phrase in ("subscription", "retainer", "software", "saas", "service")):
            upgrade("repeatability", "high", "Recurring revenue models improve repeatability.")

        if any(phrase in combined for phrase in ("agent", "automation", "workflow", "autonomous")):
            upgrade("automation", "high", "The idea benefits directly from automation leverage.")

        decision, summary = compute_decision(factors)

        next_actions = {
            "REJECT": [
                "Do not implement the requested lane in its current form.",
                "Replace the unsafe data or acquisition step with opt-in, first-party, or client-authorized inputs.",
                "Rescore the revised lane before activation.",
            ],
            "HOLD": [
                "Clarify the uncertain hard gates or weak execution factors.",
                "Narrow the scope to a pilot with strong provenance and clear consent.",
                "Rescore after tightening the plan.",
            ],
            "PASS": [
                "Document the lane in the strategy queue and journal.",
                "Build the smallest lawful pilot and track margin, cycle time, and repeatability.",
                "Keep monitoring legality, consent, provenance, and platform fit as the lane scales.",
            ],
        }[decision]

        response = {
            "decision": decision,
            "summary": summary,
            "idea": idea,
            "hard_factors": {key: factors[key] for key in HARD_FACTORS},
            "soft_factors": {key: factors[key] for key in SOFT_FACTORS},
            "reasons": reasons,
            "safer_alternatives": safer_alternatives(combined),
            "next_actions": next_actions,
        }

        return Response(message=json.dumps(response, indent=2), break_loop=False)
