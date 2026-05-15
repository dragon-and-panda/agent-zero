#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


POSITIVE_WEIGHTS = {
    "demand": 1.3,
    "margin": 1.2,
    "automation": 1.3,
    "speed_to_revenue": 1.0,
    "recurring_revenue": 1.2,
    "defensibility": 1.0,
}

NEGATIVE_WEIGHTS = {
    "setup_complexity": 0.7,
    "compliance_risk": 1.5,
    "data_sensitivity": 1.4,
    "platform_dependency": 0.8,
}

DEFAULT_SCORES = {
    "demand": 5.0,
    "margin": 5.0,
    "automation": 5.0,
    "speed_to_revenue": 5.0,
    "recurring_revenue": 5.0,
    "defensibility": 5.0,
    "setup_complexity": 5.0,
    "compliance_risk": 5.0,
    "data_sensitivity": 5.0,
    "platform_dependency": 5.0,
}

RED_FLAG_PATTERNS = {
    "personal-data resale": [
        r"\bsell(?:ing)?\b.{0,40}\bemail list",
        r"\bbuy(?:ing)?\b.{0,40}\bemail list",
        r"\bdata brokerage?\b",
        r"\bbroker(?:ing)?\b.{0,40}\bpersonal data",
    ],
    "unauthorized inbox access": [
        r"\bscrap(?:e|ing)\b.{0,40}\b(?:gmail|inbox|mailbox)",
        r"\bextract\b.{0,40}\b(?:gmail|inbox|mailbox).{0,40}\bwithout\b",
        r"\bharvest\b.{0,40}\b(?:contact|email)",
    ],
    "spam-heavy acquisition": [
        r"\bmass\b.{0,20}\bcold email",
        r"\bunsolicited\b.{0,20}\b(?:email|outreach)",
        r"\bspam\b",
    ],
}


def clamp_score(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 5.0
    return max(0.0, min(10.0, numeric))


def load_ideas(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        ideas = raw
    elif isinstance(raw, dict) and isinstance(raw.get("ideas"), list):
        ideas = raw["ideas"]
    elif isinstance(raw, dict):
        ideas = [raw]
    else:
        raise ValueError("Input JSON must be an object, list, or object with an ideas array.")

    cleaned: list[dict[str, Any]] = []
    for item in ideas:
        if isinstance(item, dict):
            cleaned.append(item)
    if not cleaned:
        raise ValueError("No idea objects found in input.")
    return cleaned


def build_search_text(idea: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in (
        "name",
        "description",
        "revenue_model",
        "acquisition_model",
    ):
        value = idea.get(key)
        if isinstance(value, str):
            parts.append(value)

    for key in ("channels", "data_sources"):
        value = idea.get(key)
        if isinstance(value, list):
            parts.extend(str(entry) for entry in value)

    return " | ".join(parts)


def detect_red_flags(idea: dict[str, Any]) -> list[str]:
    search_text = build_search_text(idea)
    flags: list[str] = []
    for label, patterns in RED_FLAG_PATTERNS.items():
        if any(re.search(pattern, search_text, flags=re.IGNORECASE) for pattern in patterns):
            flags.append(label)
    return flags


def normalized_base_score(scores: dict[str, float]) -> float:
    positive_total = sum(scores[key] * weight for key, weight in POSITIVE_WEIGHTS.items())
    negative_total = sum(scores[key] * weight for key, weight in NEGATIVE_WEIGHTS.items())

    positive_max = sum(10.0 * weight for weight in POSITIVE_WEIGHTS.values())
    negative_max = sum(10.0 * weight for weight in NEGATIVE_WEIGHTS.values())

    combined = positive_total + (negative_max - negative_total)
    return round((combined / (positive_max + negative_max)) * 100.0, 1)


def verdict_for(score: float, scores: dict[str, float], red_flags: list[str]) -> str:
    if red_flags:
        return "reject"
    if scores["compliance_risk"] >= 7 or scores["data_sensitivity"] >= 7:
        return "redesign"
    if score >= 75:
        return "prioritize"
    if score >= 60:
        return "pilot"
    if score >= 45:
        return "backlog"
    return "drop"


def build_notes(scores: dict[str, float], red_flags: list[str]) -> list[str]:
    notes: list[str] = []
    if red_flags:
        notes.append("Red flags: " + ", ".join(red_flags))
    if scores["automation"] < 6:
        notes.append("Low automation leverage")
    if scores["recurring_revenue"] < 6:
        notes.append("Weak recurring revenue")
    if scores["speed_to_revenue"] < 5:
        notes.append("Slow path to first revenue")
    if scores["compliance_risk"] > 4:
        notes.append("Compliance review needed")
    if scores["platform_dependency"] > 6:
        notes.append("High platform dependency")
    return notes or ["Balanced profile"]


def pivot_suggestions(red_flags: list[str]) -> list[str]:
    suggestions: list[str] = []
    if "personal-data resale" in red_flags:
        suggestions.append("Replace data sales with opt-in newsletter, sponsorship, or software revenue.")
    if "unauthorized inbox access" in red_flags:
        suggestions.append("Use Gmail only for authorized internal analysis with OAuth and minimum scopes.")
    if "spam-heavy acquisition" in red_flags:
        suggestions.append("Shift to inbound content, partnerships, or consent-based lead magnets.")
    return suggestions


def score_idea(idea: dict[str, Any]) -> dict[str, Any]:
    raw_scores = idea.get("scores", {})
    score_map = {
        key: clamp_score(raw_scores.get(key, default))
        for key, default in DEFAULT_SCORES.items()
    }
    red_flags = detect_red_flags(idea)
    base_score = normalized_base_score(score_map)
    if red_flags:
        base_score = min(base_score, 25.0)

    verdict = verdict_for(base_score, score_map, red_flags)
    return {
        "name": idea.get("name", "Unnamed idea"),
        "score": base_score,
        "verdict": verdict,
        "notes": build_notes(score_map, red_flags),
        "pivots": pivot_suggestions(red_flags),
        "scores": score_map,
    }


def render_report(results: list[dict[str, Any]]) -> str:
    sorted_results = sorted(results, key=lambda item: item["score"], reverse=True)

    lines = [
        "# Opportunity Scorecard",
        "",
        "| Idea | Score | Verdict | Notes |",
        "| --- | ---: | --- | --- |",
    ]

    for result in sorted_results:
        lines.append(
            "| {name} | {score:.1f} | {verdict} | {notes} |".format(
                name=result["name"],
                score=result["score"],
                verdict=result["verdict"],
                notes="; ".join(result["notes"]),
            )
        )

    lines.append("")
    lines.append("## Detailed Rationale")
    lines.append("")

    for result in sorted_results:
        lines.append(f"### {result['name']}")
        lines.append(f"- Verdict: {result['verdict']}")
        lines.append(f"- Weighted score: {result['score']:.1f}/100")
        lines.append("- Dimension scores:")
        for key, value in result["scores"].items():
            lines.append(f"  - {key}: {value:.1f}/10")
        lines.append("- Notes:")
        for note in result["notes"]:
            lines.append(f"  - {note}")
        if result["pivots"]:
            lines.append("- Safer pivots:")
            for pivot in result["pivots"]:
                lines.append(f"  - {pivot}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score venture ideas for ethical autonomous revenue.",
    )
    parser.add_argument("input_file", help="Path to a JSON file containing idea data.")
    args = parser.parse_args()

    try:
        ideas = load_ideas(Path(args.input_file))
    except FileNotFoundError:
        print(f"Input file not found: {args.input_file}", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Unable to load ideas: {exc}", file=sys.stderr)
        return 1

    results = [score_idea(idea) for idea in ideas]
    sys.stdout.write(render_report(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
