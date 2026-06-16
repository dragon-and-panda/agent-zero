from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


EMAIL_FIELDS = ("email", "email_address", "primary_email")
FIRST_NAME_FIELDS = ("first_name", "firstname", "given_name")
LAST_NAME_FIELDS = ("last_name", "lastname", "family_name", "surname")
CONSENT_FIELDS = (
    "consent",
    "opt_in",
    "optin",
    "email_opt_in",
    "marketing_consent",
    "subscribed",
)
POSITIVE_VALUES = {"true", "1", "yes", "y", "opted_in", "subscribed", "active"}
NEGATIVE_VALUES = {"false", "0", "no", "n", "opted_out", "unsubscribed", "inactive"}


def _read_records(path: Path) -> list[dict[str, object]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        raise ValueError("JSON input must be a list of objects")
    if suffix == ".jsonl":
        rows: list[dict[str, object]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                if isinstance(payload, dict):
                    rows.append(payload)
        return rows
    raise ValueError("Unsupported input format. Use CSV, JSON, or JSONL.")


def _stringify(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _pick(record: dict[str, object], field_names: Iterable[str]) -> str:
    lowered = {key.lower(): key for key in record.keys()}
    for field_name in field_names:
        actual_key = lowered.get(field_name)
        if actual_key:
            return _stringify(record.get(actual_key))
    return ""


def _consent_status(record: dict[str, object]) -> tuple[bool, str, str]:
    lowered = {key.lower(): key for key in record.keys()}
    for field_name in CONSENT_FIELDS:
        actual_key = lowered.get(field_name)
        if not actual_key:
            continue
        raw_value = _stringify(record.get(actual_key)).lower()
        if raw_value in POSITIVE_VALUES:
            return True, actual_key, raw_value
        if raw_value in NEGATIVE_VALUES:
            return False, actual_key, raw_value
    return False, "", ""


def extract_consented_contacts(records: Iterable[dict[str, object]], source_file: str) -> list[dict[str, str]]:
    extracted: list[dict[str, str]] = []
    for record in records:
        allowed, consent_field, consent_value = _consent_status(record)
        if not allowed:
            continue

        email = _pick(record, EMAIL_FIELDS)
        if not email:
            continue

        extracted.append(
            {
                "email": email,
                "first_name": _pick(record, FIRST_NAME_FIELDS),
                "last_name": _pick(record, LAST_NAME_FIELDS),
                "consent_field": consent_field,
                "consent_value": consent_value,
                "source_file": source_file,
            }
        )
    return extracted


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract explicitly consented contacts from structured files.")
    parser.add_argument("--input", required=True, help="Path to CSV, JSON, or JSONL input.")
    parser.add_argument("--output", required=True, help="Path to normalized CSV output.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    records = _read_records(input_path)
    contacts = extract_consented_contacts(records, input_path.name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "email",
                "first_name",
                "last_name",
                "consent_field",
                "consent_value",
                "source_file",
            ],
        )
        writer.writeheader()
        writer.writerows(contacts)

    print(f"wrote {len(contacts)} consented contacts to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
