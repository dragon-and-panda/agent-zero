#!/usr/bin/env python3
"""Consent-aware contact audit for mailbox exports.

This utility extracts email addresses from mailbox headers and merges them with a
consent ledger. It is designed for compliance-first segmentation:
unknown contacts are blocked by default.
"""

from __future__ import annotations

import argparse
import csv
import json
import mailbox
from collections import Counter, defaultdict
from email.utils import getaddresses
from pathlib import Path

HEADER_SOURCES = {
    "from": "from_mentions",
    "to": "to_mentions",
    "cc": "cc_mentions",
    "bcc": "bcc_mentions",
    "reply-to": "reply_to_mentions",
}

ALLOWED_CONSENT_STATUSES = {
    "opt_in",
    "customer_relationship",
    "contractual",
}


def normalize_email(raw: str) -> str:
    return raw.strip().lower()


def load_consent_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Consent CSV not found: {path}")

    consent_map: dict[str, str] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"email", "consent_status"}
        missing = expected - set(reader.fieldnames or [])
        if missing:
            missing_display = ", ".join(sorted(missing))
            raise ValueError(
                f"Consent CSV missing required columns: {missing_display}"
            )
        for row in reader:
            email = normalize_email(row["email"])
            if not email or "@" not in email:
                continue
            consent_status = normalize_email(row["consent_status"])
            consent_map[email] = consent_status
    return consent_map


def parse_mailbox_addresses(mbox_path: Path) -> dict[str, Counter]:
    if not mbox_path.exists():
        raise FileNotFoundError(f"MBOX file not found: {mbox_path}")

    records: dict[str, Counter] = defaultdict(Counter)
    mbox = mailbox.mbox(mbox_path)

    for message in mbox:
        for header_name, metric_name in HEADER_SOURCES.items():
            raw_value = message.get(header_name, "")
            if not raw_value:
                continue
            for _, address in getaddresses([raw_value]):
                email = normalize_email(address)
                if not email or "@" not in email:
                    continue
                records[email][metric_name] += 1
                records[email]["total_mentions"] += 1

    return records


def build_output_rows(
    records: dict[str, Counter], consent_map: dict[str, str]
) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for email, metrics in records.items():
        consent_status = consent_map.get(email, "unknown")
        eligible = consent_status in ALLOWED_CONSENT_STATUSES
        rows.append(
            {
                "email": email,
                "total_mentions": metrics.get("total_mentions", 0),
                "from_mentions": metrics.get("from_mentions", 0),
                "to_mentions": metrics.get("to_mentions", 0),
                "cc_mentions": metrics.get("cc_mentions", 0),
                "bcc_mentions": metrics.get("bcc_mentions", 0),
                "reply_to_mentions": metrics.get("reply_to_mentions", 0),
                "consent_status": consent_status,
                "eligible": "yes" if eligible else "no",
            }
        )
    rows.sort(
        key=lambda row: (
            int(row["total_mentions"]),
            str(row["email"]),
        ),
        reverse=True,
    )
    return rows


def write_csv(path: Path, rows: list[dict[str, str | int]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit mailbox addresses against consent statuses."
    )
    parser.add_argument(
        "--mbox",
        required=True,
        help="Path to mailbox export (.mbox).",
    )
    parser.add_argument(
        "--consent-csv",
        default=None,
        help="Optional consent CSV with columns: email, consent_status.",
    )
    parser.add_argument(
        "--output-dir",
        default="logs/consent_contact_audit",
        help="Directory for output reports.",
    )
    args = parser.parse_args()

    mbox_path = Path(args.mbox).expanduser().resolve()
    consent_csv = (
        Path(args.consent_csv).expanduser().resolve()
        if args.consent_csv
        else None
    )
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    consent_map = load_consent_map(consent_csv)
    records = parse_mailbox_addresses(mbox_path)
    rows = build_output_rows(records, consent_map)

    all_fields = [
        "email",
        "total_mentions",
        "from_mentions",
        "to_mentions",
        "cc_mentions",
        "bcc_mentions",
        "reply_to_mentions",
        "consent_status",
        "eligible",
    ]
    write_csv(output_dir / "discovered_addresses.csv", rows, all_fields)

    eligible_rows = [row for row in rows if row["eligible"] == "yes"]
    write_csv(
        output_dir / "eligible_contacts.csv",
        eligible_rows,
        ["email", "consent_status", "total_mentions"],
    )

    blocked_rows = [
        {
            "email": row["email"],
            "consent_status": row["consent_status"],
            "reason": "missing_or_insufficient_consent",
            "total_mentions": row["total_mentions"],
        }
        for row in rows
        if row["eligible"] == "no"
    ]
    write_csv(
        output_dir / "blocked_contacts.csv",
        blocked_rows,
        ["email", "consent_status", "reason", "total_mentions"],
    )

    summary = {
        "total_discovered": len(rows),
        "eligible_contacts": len(eligible_rows),
        "blocked_contacts": len(blocked_rows),
        "allowed_consent_statuses": sorted(ALLOWED_CONSENT_STATUSES),
        "output_dir": str(output_dir),
    }
    with (output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

