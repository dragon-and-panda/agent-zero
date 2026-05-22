import json
from typing import Iterable

from python.helpers.tool import Tool, Response


VALID_RATINGS = {"low", "medium", "high"}
HARD_GATES = ("legality", "consent", "provenance", "platform_alignment")
SOFT_FACTORS = ("time_to_cash", "margin", "repeatability", "automation", "defensibility")
PROHIBITED_PATTERNS = (
    "sell email list",
    "sell email lists",
    "email list brokerage",
    "contact list brokerage",
    "personal-data resale",
    "personal data resale",
    "gmail scraping",
    "scrape gmail",
    "scrape inbox",
    "inbox scraping",
    "buy contacts",
    "resell contacts",
    "spam blast",
)


def _normalize_rating(value: str, default: str = "medium") -> str:
    normalized = str(value or default).strip().lower()
    return normalized if normalized in VALID_RATINGS else default


def _split_csv(value: str) -> list[str]:
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def _high_count(names: Iterable[str], ratings: dict[str, str]) -> int:
    return sum(1 for name in names if ratings.get(name) == "high")


class RevenuePlanning(Tool):
    async def execute(
        self,
        lane_name: str = "",
        summary: str = "",
        target_customer: str = "",
        delivery_model: str = "",
        data_sources: str = "",
        acquisition_path: str = "",
        value_exchange: str = "",
        consent_basis: str = "",
        platform_dependencies: str = "",
        geography: str = "",
        legality: str = "medium",
        consent: str = "medium",
        provenance: str = "medium",
        platform_alignment: str = "medium",
        time_to_cash: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation: str = "medium",
        defensibility: str = "medium",
        risk_notes: str = "",
        **kwargs,
    ):
        ratings = {
            "legality": _normalize_rating(legality),
            "consent": _normalize_rating(consent),
            "provenance": _normalize_rating(provenance),
            "platform_alignment": _normalize_rating(platform_alignment),
            "time_to_cash": _normalize_rating(time_to_cash),
            "margin": _normalize_rating(margin),
            "repeatability": _normalize_rating(repeatability),
            "automation": _normalize_rating(automation),
            "defensibility": _normalize_rating(defensibility),
        }

        combined_text = " ".join(
            [
                lane_name,
                summary,
                target_customer,
                delivery_model,
                data_sources,
                acquisition_path,
                value_exchange,
                consent_basis,
                platform_dependencies,
                geography,
                risk_notes,
            ]
        ).lower()

        prohibited_hits = [pattern for pattern in PROHIBITED_PATTERNS if pattern in combined_text]
        hard_failures = [name for name in HARD_GATES if ratings[name] == "low"]
        hard_warnings = [name for name in HARD_GATES if ratings[name] == "medium"]
        soft_lows = [name for name in SOFT_FACTORS if ratings[name] == "low"]
        soft_highs = [name for name in SOFT_FACTORS if ratings[name] == "high"]

        if prohibited_hits:
            decision = "REJECT"
            rationale = "Idea contains prohibited privacy-abusive or contact-brokerage patterns."
        elif hard_failures:
            decision = "REJECT"
            rationale = "One or more hard gates failed."
        elif hard_warnings:
            decision = "HOLD"
            rationale = "Hard gates are not yet strong enough for execution."
        elif soft_lows:
            decision = "HOLD"
            rationale = "Compliance gates passed, but the lane is weak on core execution economics."
        elif _high_count(SOFT_FACTORS, ratings) >= 3:
            decision = "PASS"
            rationale = "Hard gates passed and enough soft factors are strong."
        else:
            decision = "HOLD"
            rationale = "Compliant lane, but it needs stronger economics or automation before execution."

        next_actions: list[str]
        if decision == "REJECT":
            next_actions = [
                "Do not execute this lane.",
                "Replace personal-data resale or non-consensual acquisition with a first-party opt-in or client-owned workflow.",
                "Reframe the offer around a lawful service, software product, research product, or consent-based outreach system.",
            ]
        elif decision == "HOLD":
            next_actions = [
                "Clarify weak hard gates or redesign the lane until legality, consent, provenance, and platform alignment are all high.",
                "Improve soft factors with narrower scope, better margins, stronger automation, or a clearer repeatable offer.",
                "Rescore the idea before execution.",
            ]
        else:
            next_actions = [
                "Document the operating procedure and approval checkpoints.",
                "Start with a narrow pilot and track margin, repeatability, and churn.",
                "Capture the lane in strategy docs and keep rescoring it as evidence changes.",
            ]

        result = {
            "lane_name": lane_name or "unnamed-lane",
            "decision": decision,
            "rationale": rationale,
            "ratings": ratings,
            "hard_failures": hard_failures,
            "hard_warnings": hard_warnings,
            "soft_lows": soft_lows,
            "soft_highs": soft_highs,
            "prohibited_hits": prohibited_hits,
            "target_customer": target_customer,
            "delivery_model": delivery_model,
            "data_sources": _split_csv(data_sources),
            "acquisition_path": acquisition_path,
            "value_exchange": value_exchange,
            "consent_basis": consent_basis,
            "platform_dependencies": _split_csv(platform_dependencies),
            "geography": geography,
            "risk_notes": risk_notes,
            "next_actions": next_actions,
        }

        return Response(
            message=json.dumps(result, indent=2, ensure_ascii=False),
            break_loop=False,
        )
