#!/usr/bin/env python3

import argparse
import json
import re
import sys
from typing import Any

EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)
ALLOWED_PROVENANCE = {
    "crm_export",
    "customer_relationship",
    "first_party_opt_in",
    "owner_provided",
}
BLOCKED_PROVENANCE = {
    "brokered",
    "gmail_export",
    "inbox_scrape",
    "leaked",
    "personal_correspondence",
    "purchased",
    "scraped",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filter contacts to consented, owner-authorized records.")
    parser.add_argument("--input", required=True, help="Path to a JSON file containing a list of contact records.")
    parser.add_argument(
        "--allowed-domains",
        required=True,
        help="Comma-separated list of allowed email domains.",
    )
    parser.add_argument(
        "--owner-authorized",
        action="store_true",
        help="Treat the entire dataset as owner-authorized.",
    )
    return parser.parse_args()


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return False


def load_records(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError("input JSON must be a list of contact objects")
    records: list[dict[str, Any]] = []
    for item in payload:
        if isinstance(item, dict):
            records.append(item)
        else:
            records.append({"raw": item})
    return records


def parse_domains(raw: str) -> set[str]:
    return {domain.strip().lower() for domain in raw.split(",") if domain.strip()}


def email_domain(email: str) -> str:
    return email.rsplit("@", 1)[-1].lower()


def record_reason(record: dict[str, Any], allowed_domains: set[str], dataset_owner_authorized: bool) -> str | None:
    email = str(record.get("email", "")).strip()
    if not email or not EMAIL_RE.match(email):
        return "invalid_email"

    domain = email_domain(email)
    if domain not in allowed_domains:
        return "domain_not_allowed"

    owner_authorized = dataset_owner_authorized or to_bool(record.get("owner_authorized"))
    if not owner_authorized:
        return "owner_authorization_missing"

    if not to_bool(record.get("consent")):
        return "consent_missing"

    provenance = str(record.get("provenance", "")).strip().lower()
    if provenance in BLOCKED_PROVENANCE:
        return "blocked_provenance"
    if provenance not in ALLOWED_PROVENANCE:
        return "unknown_provenance"

    return None


def main() -> int:
    args = parse_args()
    allowed_domains = parse_domains(args.allowed_domains)
    if not allowed_domains:
        raise ValueError("at least one allowed domain is required")

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for record in load_records(args.input):
        reason = record_reason(record, allowed_domains, args.owner_authorized)
        if reason is None:
            accepted.append(record)
        else:
            rejected.append({"reason": reason, "record": record})

    summary = {
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted": accepted,
        "rejected": rejected,
    }
    json.dump(summary, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
