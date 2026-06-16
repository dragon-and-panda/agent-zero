#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".log"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract emails from authorized customer-provided files."
    )
    parser.add_argument("--consent", required=True, help="Must be 'yes'.")
    parser.add_argument("--ownership", required=True, help="Must be 'yes'.")
    parser.add_argument(
        "--input",
        dest="inputs",
        action="append",
        required=True,
        help="Path to a customer-provided file. Repeat for multiple files.",
    )
    parser.add_argument(
        "--allow-domain",
        dest="allow_domains",
        action="append",
        default=[],
        help="Optional domain allowlist. Repeat for multiple domains.",
    )
    return parser.parse_args()


def reject(message: str) -> int:
    print(json.dumps({"status": "REJECT", "reason": message}, indent=2))
    return 2


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in TEXT_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_from_csv(path: Path) -> list[str]:
    emails: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            emails.extend(EMAIL_RE.findall(" ".join(row)))
    return emails


def extract_emails(path: Path) -> list[str]:
    if path.suffix.lower() == ".csv":
        return extract_from_csv(path)
    return EMAIL_RE.findall(read_text(path))


def main() -> int:
    args = parse_args()

    if args.consent.strip().lower() != "yes":
        return reject("Explicit permission confirmation is required.")
    if args.ownership.strip().lower() != "yes":
        return reject("Ownership or client authorization confirmation is required.")

    allow_domains = {domain.lower() for domain in args.allow_domains}
    results: dict[str, list[str]] = {}
    unique_emails: set[str] = set()

    for raw_path in args.inputs:
        path = Path(raw_path)
        if not path.exists():
            return reject(f"Input does not exist: {path}")
        emails = [email.lower() for email in extract_emails(path)]
        if allow_domains:
            emails = [
                email for email in emails if email.split("@", 1)[-1] in allow_domains
            ]
        deduped = sorted(set(emails))
        results[str(path)] = deduped
        unique_emails.update(deduped)

    print(
        json.dumps(
            {
                "status": "PASS",
                "file_count": len(results),
                "email_count": len(unique_emails),
                "emails": sorted(unique_emails),
                "files": results,
                "note": "Use only for authorized first-party contact operations.",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(json.dumps({"status": "REJECT", "reason": str(exc)}, indent=2))
        raise SystemExit(2) from exc
