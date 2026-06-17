#!/usr/bin/env python3

import csv
import sys
from pathlib import Path

ALLOWED_CONSENT = {
    "opt_in",
    "explicit_yes",
    "customer",
    "contract",
    "subscribed",
}

ALLOWED_OWNER_SCOPES = {
    "first_party",
    "client_authorized",
}

REQUIRED_FIELDS = {
    "email",
    "consent_status",
    "source_system",
    "owner_scope",
}


def normalize(value: str) -> str:
    return value.strip().lower()


def validate_headers(fieldnames: list[str] | None) -> None:
    headers = set(fieldnames or [])
    missing = REQUIRED_FIELDS - headers
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"missing required columns: {missing_list}")


def extract_rows(source_path: Path) -> list[dict[str, str]]:
    with source_path.open(newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        validate_headers(reader.fieldnames)

        accepted: list[dict[str, str]] = []
        seen_emails: set[str] = set()

        for row in reader:
            email = normalize(row.get("email", ""))
            consent_status = normalize(row.get("consent_status", ""))
            owner_scope = normalize(row.get("owner_scope", ""))
            source_system = row.get("source_system", "").strip()

            if not email or "@" not in email:
                continue
            if consent_status not in ALLOWED_CONSENT:
                continue
            if owner_scope not in ALLOWED_OWNER_SCOPES:
                continue
            if not source_system:
                continue
            if email in seen_emails:
                continue

            seen_emails.add(email)
            accepted.append(
                {
                    "email": email,
                    "consent_status": consent_status,
                    "source_system": source_system,
                    "owner_scope": owner_scope,
                }
            )

    return accepted


def write_rows(output_path: Path, rows: list[dict[str, str]]) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=["email", "consent_status", "source_system", "owner_scope"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: consent_contact_extract.py <source.csv> <output.csv>",
            file=sys.stderr,
        )
        return 2

    source_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not source_path.exists():
        print(f"source file not found: {source_path}", file=sys.stderr)
        return 2

    try:
        rows = extract_rows(source_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_rows(output_path, rows)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"exported_rows={len(rows)} output={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
