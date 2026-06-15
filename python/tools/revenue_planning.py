import json

from python.helpers.tool import Response, Tool


REJECT_PHRASES = (
    "sell email list",
    "sell email lists",
    "sell compiled email lists",
    "resell email list",
    "resell email lists",
    "compiled email lists",
    "email list broker",
    "data broker",
    "broker personal data",
    "harvest emails",
    "scrape emails",
    "scraped emails",
    "gmail scraping",
    "extract gmail contacts",
    "compile email address lists",
    "personal data resale",
    "private inbox scraping",
    "list resale",
)

UNAUTHORIZED_PHRASES = (
    "without consent",
    "no consent",
    "non-consensual",
    "unconsented",
    "unauthorized",
    "stolen",
    "leaked",
    "bypass terms",
    "evade terms",
    "ignore tos",
    "spam",
    "bulk unsolicited",
    "purchased list",
    "bought list",
)

SAFE_CONSENT_MARKERS = (
    "authorized",
    "opt-in",
    "opt in",
    "first-party",
    "first party",
    "client-owned",
    "client owned",
    "customer-provided",
    "customer provided",
    "documented consent",
    "written approval",
)

PERSONAL_DATA_MARKERS = (
    "gmail",
    "inbox",
    "email address",
    "email addresses",
    "contact list",
    "contacts",
    "mailbox",
)


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())


def _contains_any(text: str, phrases: tuple[str, ...]) -> list[str]:
    return [phrase for phrase in phrases if phrase in text]


class RevenuePlanning(Tool):
    async def execute(
        self,
        idea: str = "",
        asset: str = "",
        data_sources: str = "",
        consent_status: str = "",
        acquisition_method: str = "",
        customer: str = "",
        notes: str = "",
        **kwargs,
    ):
        fields = {
            "idea": idea,
            "asset": asset,
            "data_sources": data_sources,
            "consent_status": consent_status,
            "acquisition_method": acquisition_method,
            "customer": customer,
            "notes": notes,
        }
        combined = _normalize(" ".join(value for value in fields.values() if value))

        reject_matches = _contains_any(combined, REJECT_PHRASES)
        unauthorized_matches = _contains_any(combined, UNAUTHORIZED_PHRASES)
        personal_data_matches = _contains_any(combined, PERSONAL_DATA_MARKERS)
        has_safe_consent = bool(_contains_any(_normalize(consent_status), SAFE_CONSENT_MARKERS))

        verdict = "PASS"
        reasons: list[str] = []
        next_steps: list[str] = []
        safer_alternatives: list[str] = []

        if reject_matches:
            verdict = "REJECT"
            reasons.append(
                "The plan appears to rely on personal-data extraction or resale, which is outside the allowed operating model."
            )

        if unauthorized_matches:
            verdict = "REJECT"
            reasons.append(
                "The plan references non-consensual, unclear-provenance, or policy-evasive acquisition methods."
            )

        if verdict != "REJECT":
            if personal_data_matches and not has_safe_consent:
                verdict = "HOLD"
                reasons.append(
                    "Email or inbox workflows need documented first-party or client authorization before they can proceed."
                )
            if not customer.strip():
                verdict = "HOLD"
                reasons.append("A specific customer or buyer segment is missing.")
            if not acquisition_method.strip():
                verdict = "HOLD"
                reasons.append("The acquisition and delivery method is not yet defined.")

        if verdict == "REJECT":
            safer_alternatives.extend(
                [
                    "Offer inbox-to-CRM summarization only for client-owned or first-party mailboxes with written authorization.",
                    "Build an opt-in lead magnet, newsletter, or research product instead of selling contact data.",
                    "Use lawful public-business data to build a listing, directory, or market map product.",
                ]
            )
            next_steps.extend(
                [
                    "Remove any dependence on scraped, purchased, or private personal data.",
                    "Rewrite the idea around a first-party, client-authorized, or public-data workflow.",
                ]
            )
        elif verdict == "HOLD":
            next_steps.extend(
                [
                    "Document the target customer and the problem being solved.",
                    "Clarify consent, provenance, and the exact acquisition method before execution.",
                    "Run the lane through instruments/strategy/score.sh after the missing inputs are filled in.",
                ]
            )
        else:
            next_steps.extend(
                [
                    "Score the lane with instruments/strategy/score.sh.",
                    "Document consent/provenance if personal or inbox data is involved.",
                    "Start with a small manual pilot before deeper automation.",
                ]
            )

        result = {
            "verdict": verdict,
            "summary": (
                "Compliant enough to explore."
                if verdict == "PASS"
                else "Needs clarification before execution."
                if verdict == "HOLD"
                else "Not allowed in the current program."
            ),
            "reasons": reasons,
            "matched_risks": {
                "rejected_phrases": reject_matches,
                "unauthorized_phrases": unauthorized_matches,
                "personal_data_markers": personal_data_matches,
            },
            "safer_alternatives": safer_alternatives,
            "next_steps": next_steps,
        }

        return Response(message=json.dumps(result, indent=2), break_loop=False)
