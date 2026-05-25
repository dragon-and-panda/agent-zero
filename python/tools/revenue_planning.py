import json
import re

from python.helpers.tool import Response, Tool

DEFAULT_RATING = "medium"
VALID_RATINGS = {"low", "medium", "high"}
HARD_FACTORS = ("legality", "consent", "provenance", "platform_fit")
SOFT_FACTORS = ("time", "margin", "repeatability", "automation", "defensibility")
PROHIBITED_PATTERNS = (
    (
        r"(sell|broker|resell|rent|trade).{0,24}(email\s+lists?|contact\s+lists?)",
        "personal email or contact list brokerage",
    ),
    (
        r"(harvest|scrape|extract|compile).{0,24}(emails?|contacts?).{0,24}(gmail|google\s+mail|inbox|mailbox|files?)",
        "non-consensual contact harvesting from mail or files",
    ),
    (
        r"(spam|cold\s+blast|bulk\s+outreach).{0,24}(emails?|contacts?)",
        "spam or non-compliant bulk outreach",
    ),
    (
        r"(gmail|google\s+mail|inbox|mailbox).{0,24}(sell|resell|broker|list)",
        "monetizing private inbox data",
    ),
)
SAFE_ALTERNATIVES = (
    "consent-based lead magnets and first-party audience growth",
    "client-owned inbox triage and CRM operations",
    "listing optimization and marketplace operations for owner inventory",
    "research products or analytics built from public, licensed, or client-owned data",
)


def normalize_rating(value: str, field_name: str) -> str:
    normalized = (value or DEFAULT_RATING).strip().lower()
    if normalized not in VALID_RATINGS:
        raise ValueError(
            f"{field_name} must be one of: {', '.join(sorted(VALID_RATINGS))}"
        )
    return normalized


def collect_prohibited_matches(opportunity: str) -> list[str]:
    lowered = opportunity.lower()
    matches: list[str] = []
    for pattern, description in PROHIBITED_PATTERNS:
        if re.search(pattern, lowered):
            matches.append(description)
    return matches


def build_next_steps(
    status: str,
    hard_cautions: list[str],
    soft_lows: list[str],
) -> list[str]:
    if status == "PASS":
        return [
            "Define a narrow MVP that only uses user-owned, client-owned, or opt-in data.",
            "Instrument unit economics before scaling automation.",
            "Review platform policies for each launch channel before activation.",
        ]

    if status == "HOLD":
        steps: list[str] = []
        if hard_cautions:
            steps.append(
                "Raise medium hard-gate factors to high before activation: "
                + ", ".join(hard_cautions)
                + "."
            )
        if soft_lows:
            steps.append(
                "Improve weak execution factors before build-out: "
                + ", ".join(soft_lows)
                + "."
            )
        if not steps:
            steps.append(
                "Clarify offer, distribution, and operating leverage before activation."
            )
        steps.append(
            "Prefer first-party, consent-based monetization over any data-resale lane."
        )
        return steps

    return [
        "Stop work on this lane as proposed.",
        "Replace private-data resale or inbox-harvesting behavior with a consent-based service or product.",
        "Consider one of the approved alternatives: " + "; ".join(SAFE_ALTERNATIVES) + ".",
    ]


def score_opportunity(
    opportunity: str,
    legality: str = DEFAULT_RATING,
    consent: str = DEFAULT_RATING,
    provenance: str = DEFAULT_RATING,
    platform_fit: str = DEFAULT_RATING,
    time: str = DEFAULT_RATING,
    margin: str = DEFAULT_RATING,
    repeatability: str = DEFAULT_RATING,
    automation: str = DEFAULT_RATING,
    defensibility: str = DEFAULT_RATING,
) -> dict[str, object]:
    hard_factors = {
        "legality": normalize_rating(legality, "legality"),
        "consent": normalize_rating(consent, "consent"),
        "provenance": normalize_rating(provenance, "provenance"),
        "platform_fit": normalize_rating(platform_fit, "platform_fit"),
    }
    soft_factors = {
        "time": normalize_rating(time, "time"),
        "margin": normalize_rating(margin, "margin"),
        "repeatability": normalize_rating(repeatability, "repeatability"),
        "automation": normalize_rating(automation, "automation"),
        "defensibility": normalize_rating(defensibility, "defensibility"),
    }

    prohibited_matches = collect_prohibited_matches(opportunity)
    hard_failures = [name for name, value in hard_factors.items() if value == "low"]
    hard_cautions = [name for name, value in hard_factors.items() if value == "medium"]
    soft_lows = [name for name, value in soft_factors.items() if value == "low"]
    soft_high_count = sum(1 for value in soft_factors.values() if value == "high")

    status = "HOLD"
    reasons: list[str] = []

    if prohibited_matches:
        status = "REJECT"
        reasons.append(
            "The opportunity description includes blocked patterns: "
            + ", ".join(sorted(set(prohibited_matches)))
            + "."
        )
    elif hard_failures:
        status = "REJECT"
        reasons.append(
            "One or more hard gates failed: " + ", ".join(hard_failures) + "."
        )
    elif hard_cautions:
        status = "HOLD"
        reasons.append(
            "At least one hard gate is only medium: "
            + ", ".join(hard_cautions)
            + "."
        )
    elif soft_lows:
        status = "HOLD"
        reasons.append(
            "The lane is compliant, but weak execution factors remain: "
            + ", ".join(soft_lows)
            + "."
        )
    elif soft_high_count >= 3:
        status = "PASS"
        reasons.append(
            "All hard gates are high and at least three execution factors are high."
        )
    else:
        status = "HOLD"
        reasons.append("The lane is compliant, but not compelling enough to activate yet.")

    return {
        "opportunity": opportunity,
        "status": status,
        "hard_factors": hard_factors,
        "soft_factors": soft_factors,
        "hard_failures": hard_failures,
        "hard_cautions": hard_cautions,
        "soft_lows": soft_lows,
        "soft_high_count": soft_high_count,
        "reasons": reasons,
        "next_steps": build_next_steps(status, hard_cautions, soft_lows),
        "approved_alternatives": list(SAFE_ALTERNATIVES),
    }


class RevenuePlanning(Tool):
    async def execute(
        self,
        opportunity: str = "",
        legality: str = DEFAULT_RATING,
        consent: str = DEFAULT_RATING,
        provenance: str = DEFAULT_RATING,
        platform_fit: str = DEFAULT_RATING,
        time: str = DEFAULT_RATING,
        margin: str = DEFAULT_RATING,
        repeatability: str = DEFAULT_RATING,
        automation: str = DEFAULT_RATING,
        defensibility: str = DEFAULT_RATING,
        **kwargs,
    ):
        if not opportunity.strip():
            return Response(
                message=(
                    "opportunity is required. Describe the revenue lane being evaluated."
                ),
                break_loop=False,
            )

        try:
            result = score_opportunity(
                opportunity=opportunity,
                legality=legality,
                consent=consent,
                provenance=provenance,
                platform_fit=platform_fit,
                time=time,
                margin=margin,
                repeatability=repeatability,
                automation=automation,
                defensibility=defensibility,
            )
        except ValueError as exc:
            return Response(message=str(exc), break_loop=False)

        return Response(
            message=json.dumps(result, indent=2, sort_keys=True),
            break_loop=False,
        )
