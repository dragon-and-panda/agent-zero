#!/usr/bin/env python3

import argparse
import csv
import re
import sys
from pathlib import Path

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TRUTHY = {"1", "true", "yes", "y", "opt_in", "consented"}
ALLOWED_PROVENANCE = {
    "first_party",
    "client_owned",
    "authorized_export",
    "user_provided",
    "crm",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Keep only consent-safe, first-party contact rows."
    )
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    parser.add_argument("--email-column", default="email")
    parser.add_argument("--consent-column", default="consent")
    parser.add_argument("--provenance-column", default="provenance")
    return parser.parse_args()


def normalize(value: str) -> str:
    return value.strip().lower()


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value.strip()))


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    with input_path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []

        required_columns = {
            args.email_column,
            args.consent_column,
            args.provenance_column,
        }
        missing = sorted(required_columns - set(fieldnames))
        if missing:
            print(
                f"Missing required columns: {', '.join(missing)}",
                file=sys.stderr,
            )
            return 1

        kept_rows: list[dict[str, str]] = []
        total_rows = 0
        rejected_rows = 0

        for row in reader:
            total_rows += 1

            email = row.get(args.email_column, "").strip()
            consent = normalize(row.get(args.consent_column, ""))
            provenance = normalize(row.get(args.provenance_column, ""))

            if not is_valid_email(email):
                rejected_rows += 1
                continue

            if consent not in TRUTHY:
                rejected_rows += 1
                continue

            if provenance not in ALLOWED_PROVENANCE:
                rejected_rows += 1
                continue

            kept_rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept_rows)

    print(
        "consent_contact_extract summary: "
        f"total={total_rows} kept={len(kept_rows)} rejected={rejected_rows}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
