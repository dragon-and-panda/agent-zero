#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "consent_strength",
    "legality_safety",
    "automation_fit",
    "time_to_revenue",
    "margin_potential",
    "repeatability",
    "strategic_fit",
    "startup_cost",
}

WEIGHTS = {
    "consent_strength": 0.22,
    "legality_safety": 0.22,
    "automation_fit": 0.15,
    "time_to_revenue": 0.10,
    "margin_potential": 0.12,
    "repeatability": 0.08,
    "strategic_fit": 0.06,
    "startup_cost": 0.05,
}

EXAMPLE = [
    {
        "name": "Inbox-to-offer audit",
        "consent_strength": 5,
        "legality_safety": 5,
        "automation_fit": 4,
        "time_to_revenue": 4,
        "margin_potential": 4,
        "repeatability": 4,
        "strategic_fit": 5,
        "startup_cost": 2,
        "notes": "Turns owned inbox and document exports into an audit and action plan.",
    },
    {
        "name": "Sell scraped contact lists",
        "consent_strength": 0,
        "legality_safety": 0,
        "automation_fit": 3,
        "time_to_revenue": 3,
        "margin_potential": 2,
        "repeatability": 1,
        "strategic_fit": 1,
        "startup_cost": 1,
        "notes": "Included as a negative example; should be rejected.",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score revenue opportunities with consent and legality guardrails."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Path to a JSON file containing one opportunity object or a list of objects.",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Print an example JSON payload and exit.",
    )
    return parser.parse_args()


def load_payload(path: str) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("Input JSON must be an object or an array of objects.")


def validate_opportunity(opportunity: dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - opportunity.keys()
    if missing:
        raise ValueError(
            f"{opportunity.get('name', 'Unnamed opportunity')} is missing fields: "
            + ", ".join(sorted(missing))
        )

    for field in REQUIRED_FIELDS:
        value = opportunity[field]
        if not isinstance(value, (int, float)):
            raise ValueError(f"{opportunity.get('name', 'Unnamed opportunity')}: {field} must be numeric.")
        if value < 0 or value > 5:
            raise ValueError(
                f"{opportunity.get('name', 'Unnamed opportunity')}: {field} must be between 0 and 5."
            )


def normalized_value(field: str, value: float) -> float:
    if field == "startup_cost":
        return (5 - value) / 5
    return value / 5


def classify(opportunity: dict[str, Any], score: float) -> tuple[str, str]:
    consent = opportunity["consent_strength"]
    legality = opportunity["legality_safety"]

    if consent < 3 or legality < 3:
        return "REJECT", "Consent or legality is too weak."
    if score >= 80:
        return "PRIORITIZE", "Strong consent, safety, and economic shape."
    if score >= 65:
        return "PILOT", "Promising, but validate economics with a narrow test."
    return "DEFER", "Safe enough, but lower leverage than better-ranked options."


def score_opportunity(opportunity: dict[str, Any]) -> dict[str, Any]:
    validate_opportunity(opportunity)

    weighted_sum = 0.0
    for field, weight in WEIGHTS.items():
        weighted_sum += normalized_value(field, float(opportunity[field])) * weight

    score = round(weighted_sum * 100, 1)
    decision, rationale = classify(opportunity, score)

    return {
        "name": opportunity.get("name", "Unnamed opportunity"),
        "score": score,
        "decision": decision,
        "rationale": rationale,
        "notes": opportunity.get("notes", ""),
    }


def format_row(result: dict[str, Any]) -> str:
    name = result["name"][:32]
    return f"{name:<32} {result['score']:>6}  {result['decision']:<10}  {result['rationale']}"


def main() -> int:
    args = parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0

    if not args.input_file:
        raise SystemExit("Provide an input JSON file or use --example.")

    opportunities = load_payload(args.input_file)
    results = [score_opportunity(item) for item in opportunities]
    results.sort(key=lambda item: item["score"], reverse=True)

    print("Opportunity scoring results")
    print("=" * 96)
    print(f"{'Name':<32} {'Score':>6}  {'Decision':<10}  Rationale")
    print("-" * 96)
    for result in results:
        print(format_row(result))
    print("=" * 96)
    print("Rejected opportunities should not be pursued, regardless of apparent speed or margin.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
