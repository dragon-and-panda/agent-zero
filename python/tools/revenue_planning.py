import json

from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        data_source: str = "",
        consent_level: str = "",
        customer: str = "",
        delivery_model: str = "",
        notes: str = "",
        **kwargs,
    ):
        idea = idea.strip()
        data_source = data_source.strip()
        consent_level = consent_level.strip().lower()
        customer = customer.strip()
        delivery_model = delivery_model.strip()
        notes = notes.strip()

        if not idea:
            return Response(
                message="idea is required.",
                break_loop=False,
            )

        concerns = []
        alternatives = []
        allowed = True

        risk_terms = [
            "sell email",
            "email list",
            "contact list",
            "gmail scrape",
            "scrape inbox",
            "broker leads",
            "cold email blast",
            "personal data resale",
        ]
        haystack = " ".join(
            part for part in [idea.lower(), data_source.lower(), notes.lower()] if part
        )

        if any(term in haystack for term in risk_terms):
            allowed = False
            concerns.append(
                "The proposal appears to rely on scraping, brokering, or selling personal contact data."
            )
            alternatives.extend(
                [
                    "opt-in lead generation with explicit signup and consent tracking",
                    "inbox-to-CRM enrichment for a consenting mailbox owner",
                    "research products based on public or licensed business data",
                ]
            )

        if consent_level in {"none", "unknown", "unclear", "third-party"}:
            allowed = False
            concerns.append(
                "Consent is missing or unclear. The system only supports first-party or explicitly authorized data use."
            )
            alternatives.extend(
                [
                    "first-party analytics for the account owner",
                    "customer-owned CRM enrichment",
                ]
            )

        if not data_source:
            concerns.append(
                "Data provenance is unspecified. Document lawful origin before launch."
            )

        if not customer:
            concerns.append("Target customer is unspecified.")

        if not delivery_model:
            concerns.append("Delivery model is unspecified.")

        if allowed:
            status = "APPROVED_FOR_SCORING"
            next_steps = [
                "Score the lane with instruments/strategy/score.sh before execution.",
                "Attach policy references from docs/policies/compliance_pack.md.",
                "Record the decision in docs/programs/agentic_financial_system/journal.md.",
            ]
        else:
            status = "REJECTED"
            next_steps = [
                "Do not execute the original proposal.",
                "Replace it with a compliant alternative before planning implementation.",
                "Re-run planning with a first-party or opt-in workflow.",
            ]

        result = {
            "status": status,
            "idea": idea,
            "customer": customer or "unspecified",
            "delivery_model": delivery_model or "unspecified",
            "data_source": data_source or "unspecified",
            "consent_level": consent_level or "unspecified",
            "concerns": concerns,
            "recommended_alternatives": sorted(set(alternatives)),
            "next_steps": next_steps,
        }

        return Response(
            message=json.dumps(result, indent=2),
            break_loop=False,
        )
