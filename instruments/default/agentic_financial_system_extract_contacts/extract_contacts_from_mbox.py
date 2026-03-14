#!/usr/bin/env python3
"""
Consent-first contact extraction utility for authorized MBOX exports.

This script is intended for first-party, permissioned analysis only.
Do not use it for scraping or non-consensual outreach.
"""

from __future__ import annotations

import argparse
import csv
import mailbox
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Iterable

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
HEADER_FIELDS = ("from", "to", "cc", "bcc", "reply-to")


@dataclass
class ContactStats:
    sources: set[str] = field(default_factory=set)
    count_received: int = 0
    count_sent: int = 0
    count_cc: int = 0
    count_other: int = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None

    def observe(self, source: str, seen_at: datetime | None) -> None:
        self.sources.add(source)
        if source == "received":
            self.count_received += 1
        elif source == "sent":
            self.count_sent += 1
        elif source == "cc":
            self.count_cc += 1
        else:
            self.count_other += 1

        if seen_at is None:
            return
        if self.first_seen is None or seen_at < self.first_seen:
            self.first_seen = seen_at
        if self.last_seen is None or seen_at > self.last_seen:
            self.last_seen = seen_at


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract and deduplicate contacts from authorized MBOX files."
    )
    parser.add_argument(
        "--mbox",
        dest="mbox_files",
        action="append",
        required=True,
        help="Path to an MBOX file. Pass multiple times for multiple files.",
    )
    parser.add_argument(
        "--owner-email",
        dest="owner_emails",
        action="append",
        default=[],
        help=(
            "Your own email address for sent/received classification. "
            "Pass multiple times if needed."
        ),
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV path.",
    )
    return parser.parse_args()


def normalize_email(email_address: str) -> str | None:
    normalized = email_address.strip().lower()
    if not normalized or not EMAIL_PATTERN.match(normalized):
        return None
    return normalized


def parse_header_addresses(raw_header: str | None) -> list[str]:
    if not raw_header:
        return []
    parsed = []
    for _, address in getaddresses([raw_header]):
        normalized = normalize_email(address)
        if normalized:
            parsed.append(normalized)
    return parsed


def parse_message_date(raw_date: str | None) -> datetime | None:
    if not raw_date:
        return None
    try:
        return parsedate_to_datetime(raw_date)
    except Exception:
        return None


def classify_source_for_address(
    address: str,
    sender: set[str],
    to_list: set[str],
    cc_list: set[str],
    owners: set[str],
) -> str:
    # Address-level classification preserves explicit CC provenance.
    if address in cc_list:
        return "cc"
    if owners and sender & owners:
        return "sent"
    if owners and to_list & owners:
        return "received"
    return "other"


def collect_message_addresses(msg: mailbox.mboxMessage) -> dict[str, set[str]]:
    values: dict[str, set[str]] = {}
    for field in HEADER_FIELDS:
        addresses = parse_header_addresses(msg.get(field))
        values[field] = set(addresses)
    return values


def iter_relevant_addresses(headers: dict[str, set[str]]) -> Iterable[str]:
    yielded = set()
    for field in HEADER_FIELDS:
        for address in headers.get(field, set()):
            if address not in yielded:
                yielded.add(address)
                yield address


def process_mbox(
    mbox_path: Path,
    owners: set[str],
    stats: dict[str, ContactStats],
) -> None:
    mbox = mailbox.mbox(str(mbox_path))
    for msg in mbox:
        headers = collect_message_addresses(msg)
        sender = headers.get("from", set())
        to_list = headers.get("to", set())
        cc_list = headers.get("cc", set())
        seen_at = parse_message_date(msg.get("date"))

        for email_address in iter_relevant_addresses(headers):
            # Skip owner addresses in exported contact result.
            if email_address in owners:
                continue
            source = classify_source_for_address(
                email_address, sender, to_list, cc_list, owners
            )
            stats[email_address].observe(source, seen_at)


def write_output(output_path: Path, stats: dict[str, ContactStats]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "email",
                "sources",
                "count_received",
                "count_sent",
                "count_cc",
                "count_other",
                "first_seen",
                "last_seen",
            ]
        )
        for email_address in sorted(stats):
            record = stats[email_address]
            writer.writerow(
                [
                    email_address,
                    "|".join(sorted(record.sources)),
                    record.count_received,
                    record.count_sent,
                    record.count_cc,
                    record.count_other,
                    record.first_seen.isoformat() if record.first_seen else "",
                    record.last_seen.isoformat() if record.last_seen else "",
                ]
            )


def main() -> int:
    args = parse_args()
    stats: dict[str, ContactStats] = defaultdict(ContactStats)
    owners = {
        owner
        for owner in (normalize_email(item) for item in args.owner_emails)
        if owner is not None
    }

    mbox_paths = [Path(item).expanduser().resolve() for item in args.mbox_files]
    for mbox_path in mbox_paths:
        if not mbox_path.exists():
            raise FileNotFoundError(f"MBOX file not found: {mbox_path}")
        process_mbox(mbox_path, owners, stats)

    write_output(Path(args.output).expanduser().resolve(), stats)
    print(f"Extracted {len(stats)} unique contact(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
