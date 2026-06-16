#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


DEFAULT_CONSENT_COLUMNS = (
    "consent",
    "marketing_consent",
    "email_consent",
    "opt_in",
    "opted_in",
    "subscribed",
)
DEFAULT_ALLOWED_VALUES = {"yes", "true", "1", "opt_in", "opt-in", "subscribed", "consented"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract unique consented contacts from first-party CSV or JSON data."
    )
    parser.add_argument("--input", required=True, help="Path to the CSV or JSON input file.")
    parser.add_argument("--output", required=True, help="Path to the output CSV file.")
    parser.add_argument("--report", help="Optional path to write a JSON summary report.")
    parser.add_argument(
        "--email-column",
        default="email",
        help="Column containing email addresses. Defaults to 'email'.",
    )
    parser.add_argument(
        "--consent-columns",
        nargs="*",
        default=list(DEFAULT_CONSENT_COLUMNS),
        help="Columns checked for explicit consent values.",
    )
    parser.add_argument(
        "--allowed-values",
        nargs="*",
        default=sorted(DEFAULT_ALLOWED_VALUES),
        help="Values treated as explicit consent.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ValueError("JSON input must be an array of objects.")
        return data
    raise ValueError("Input must be a .csv or .json file.")


def normalize(value: str) -> str:
    return str(value or "").strip().lower().replace(" ", "_")


def row_has_consent(row: dict, consent_columns: list[str], allowed_values: set[str]) -> bool:
    for column in consent_columns:
        if normalize(row.get(column, "")) in allowed_values:
            return True
    return False


def write_output(path: Path, rows: list[dict], email_column: str) -> None:
    fieldnames = [email_column, "source_row_index"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    report_path = Path(args.report) if args.report else None

    rows = load_rows(input_path)
    allowed_values = {normalize(value) for value in args.allowed_values}

    accepted = []
    seen_emails = set()
    missing_email = 0
    no_consent = 0

    for index, row in enumerate(rows, start=1):
        email = str(row.get(args.email_column, "")).strip().lower()
        if not email:
            missing_email += 1
            continue
        if not row_has_consent(row, args.consent_columns, allowed_values):
            no_consent += 1
            continue
        if email in seen_emails:
            continue
        seen_emails.add(email)
        accepted.append(
            {
                args.email_column: email,
                "source_row_index": index,
            }
        )

    write_output(output_path, accepted, args.email_column)

    report = {
        "input_rows": len(rows),
        "accepted_rows": len(accepted),
        "missing_email_rows": missing_email,
        "rejected_without_consent": no_consent,
        "output_file": str(output_path),
    }

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
