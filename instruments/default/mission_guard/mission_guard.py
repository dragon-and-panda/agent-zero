#!/usr/bin/env python3
"""Mission guard scanner for autonomous workflow compliance."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str
    pattern: str
    reason: str
    safer_alternative: str


RULES = [
    Rule(
        id="R001",
        severity="high",
        pattern=r"\b(sell|resell|broker|trade)\b.{0,80}\b(email lists?|mailing lists?|contact lists?)\b",
        reason="Selling personal contact lists is generally non-compliant and can violate privacy law/platform terms.",
        safer_alternative="Use consent-based outreach and sell analytics/services instead of raw personal data.",
    ),
    Rule(
        id="R002",
        severity="high",
        pattern=r"\b(scrape(?:d|s|ing)?|harvest(?:ed|s|ing)?|extract(?:ed|s|ing)?)\b.{0,80}\b(gmail|inbox|email)\b",
        reason="Inbox extraction without explicit authorization and consent controls is unsafe.",
        safer_alternative="Use OAuth-based account-owner access and attach consent/provenance metadata.",
    ),
    Rule(
        id="R003",
        severity="high",
        pattern=r"\b(spam|bulk blast|unsolicited)\b",
        reason="Unsolicited messaging workflows are prohibited by anti-spam policies and laws.",
        safer_alternative="Require opt-in audiences and include suppression/unsubscribe handling.",
    ),
    Rule(
        id="R004",
        severity="medium",
        pattern=r"\bguaranteed\b.{0,40}\b(profit|returns?)\b",
        reason="Guaranteed investment return claims are misleading and risky.",
        safer_alternative="Use evidence-based performance reporting with clear risk disclosures.",
    ),
    Rule(
        id="R005",
        severity="high",
        pattern=r"(\b(auto|automate|automatic)\b.{0,80}\b(send|transfer|deposit|payout)s?\b.{0,80}\b(cash app|bank|wallet)\b)|(\b(cash app|bank|wallet)\b.{0,80}\b(auto|automate|automatic)\b.{0,80}\b(send|transfer|deposit|payout)s?\b)",
        reason="Automated fund transfers need explicit authorization, controls, and auditability.",
        safer_alternative="Queue transfers as explicit treasury actions with approvals and reconciliation.",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan mission text for compliance risks.")
    parser.add_argument("--file", type=Path, help="Path to mission text file.")
    parser.add_argument("--text", type=str, help="Mission text provided directly.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    return parser.parse_args()


def load_text(args: argparse.Namespace) -> str:
    if args.file and args.text:
        raise ValueError("Use either --file or --text, not both.")
    if args.file:
        return args.file.read_text(encoding="utf-8")
    if args.text:
        return args.text
    raise ValueError("Provide mission input with --file or --text.")


def scan(text: str) -> dict:
    findings = []
    lowered = text.lower()

    for rule in RULES:
        matches = [m.group(0) for m in re.finditer(rule.pattern, lowered, flags=re.IGNORECASE | re.DOTALL)]
        if matches:
            findings.append(
                {
                    "id": rule.id,
                    "severity": rule.severity,
                    "reason": rule.reason,
                    "safer_alternative": rule.safer_alternative,
                    "matches": matches[:3],
                }
            )

    severity_rank = {"high": 3, "medium": 2, "low": 1}
    highest = "none"
    if findings:
        highest = max((f["severity"] for f in findings), key=lambda sev: severity_rank.get(sev, 0))

    return {
        "status": "fail" if highest == "high" else "review" if findings else "pass",
        "highest_severity": highest,
        "findings": findings,
        "rule_count": len(RULES),
    }


def print_human(report: dict) -> None:
    print(f"mission_guard status: {report['status']}")
    print(f"highest severity: {report['highest_severity']}")
    print(f"rules checked: {report['rule_count']}")
    if not report["findings"]:
        print("No risky patterns detected.")
        return
    print("")
    for finding in report["findings"]:
        print(f"- [{finding['severity'].upper()}] {finding['id']}")
        print(f"  reason: {finding['reason']}")
        print(f"  safer:  {finding['safer_alternative']}")
        if finding["matches"]:
            print(f"  sample: {finding['matches'][0]}")


def main() -> int:
    args = parse_args()
    try:
        text = load_text(args)
    except Exception as exc:  # pragma: no cover - user input handling path
        print(f"error: {exc}", file=sys.stderr)
        return 2

    report = scan(text)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)

    if report["highest_severity"] == "high":
        return 2
    if report["findings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
