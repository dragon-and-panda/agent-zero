#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

EMAIL_RE = re.compile(r"^[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}$", re.IGNORECASE)
TRUTHY = {"1", "true", "yes", "y", "opt-in", "opt_in", "subscribed"}
APPROVED_BASES = {"consent", "contract", "customer", "client", "vendor", "partner"}


def normalize(value: object) -> str:
    return str(value or "").strip()


def is_email(value: object) -> bool:
    return bool(EMAIL_RE.match(normalize(value)))


def read_records(path: Path) -> list[dict[str, object]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("JSON input must be an array of objects.")
        if any(not isinstance(item, dict) for item in data):
            raise ValueError("JSON input must contain only objects.")
        return data
    raise ValueError("Supported input formats are .csv and .json.")


def consent_ok(record: dict[str, object], consent_column: str, lawful_basis_column: str) -> tuple[bool, str]:
    consent_value = normalize(record.get(consent_column)).lower()
    if consent_value in TRUTHY:
        return True, f"{consent_column}={consent_value}"

    lawful_basis_value = normalize(record.get(lawful_basis_column)).lower()
    if lawful_basis_value in APPROVED_BASES:
        return True, f"{lawful_basis_column}={lawful_basis_value}"

    return False, "missing_consent_evidence"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract consent-compatible contacts.")
    parser.add_argument("--input", required=True, help="Path to a CSV or JSON contacts file.")
    parser.add_argument("--email-column", default="email")
    parser.add_argument("--consent-column", default="consent")
    parser.add_argument("--lawful-basis-column", default="lawful_basis")
    args = parser.parse_args()

    path = Path(args.input)
    records = read_records(path)

    accepted: list[dict[str, object]] = []
    rejected: list[dict[str, object]] = []

    for index, record in enumerate(records, start=1):
        email_value = record.get(args.email_column)
        if not is_email(email_value):
            rejected.append(
                {
                    "row": index,
                    "reason": "invalid_or_missing_email",
                }
            )
            continue

        allowed, evidence = consent_ok(
            record,
            consent_column=args.consent_column,
            lawful_basis_column=args.lawful_basis_column,
        )
        if not allowed:
            rejected.append(
                {
                    "row": index,
                    "email": normalize(email_value),
                    "reason": evidence,
                }
            )
            continue

        accepted.append(
            {
                "row": index,
                "email": normalize(email_value),
                "evidence": evidence,
            }
        )

    print(
        json.dumps(
            {
                "input": str(path),
                "accepted_count": len(accepted),
                "rejected_count": len(rejected),
                "accepted": accepted,
                "rejected": rejected,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
