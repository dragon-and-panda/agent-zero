#!/usr/bin/env python3

"""Extract contact analytics from an MBOX mailbox export.

This script is designed for consent-aware CRM building and internal analytics.
It does not classify contacts as marketable; that step should be done manually
with legal/compliance review.
"""

from __future__ import annotations

import argparse
import csv
import json
import mailbox
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Iterable


@dataclass
class ContactStats:
    email: str
    name: str = ""
    domain: str = ""
    from_count: int = 0
    to_count: int = 0
    cc_count: int = 0
    bcc_count: int = 0
    reply_to_count: int = 0
    sent_to_count: int = 0
    received_from_count: int = 0
    total_mentions: int = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    consent_status: str = "unknown"
    notes: str = ""

    def touch(self, seen_at: datetime | None) -> None:
        if not seen_at:
            return
        if self.first_seen is None or seen_at < self.first_seen:
            self.first_seen = seen_at
        if self.last_seen is None or seen_at > self.last_seen:
            self.last_seen = seen_at


def normalize_email(value: str) -> str:
    return value.strip().lower()


def parse_date(header_value: str | None) -> datetime | None:
    if not header_value:
        return None
    try:
        parsed = parsedate_to_datetime(header_value)
    except (TypeError, ValueError, IndexError):
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_addresses(values: Iterable[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for name, email_addr in getaddresses(values):
        email_norm = normalize_email(email_addr)
        if not email_norm or "@" not in email_norm:
            continue
        pairs.append((name.strip(), email_norm))
    return pairs


def ensure_contact(
    contacts: dict[str, ContactStats], email_addr: str, suggested_name: str
) -> ContactStats:
    if email_addr not in contacts:
        domain = email_addr.split("@", 1)[1]
        contacts[email_addr] = ContactStats(
            email=email_addr, name=suggested_name, domain=domain
        )
    elif suggested_name and not contacts[email_addr].name:
        contacts[email_addr].name = suggested_name
    return contacts[email_addr]


def iso_or_blank(value: datetime | None) -> str:
    return value.isoformat() if value else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract contact-level analytics from MBOX files."
    )
    parser.add_argument("--mbox", required=True, help="Path to MBOX file")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for contacts.csv, edges.csv, and summary.json",
    )
    parser.add_argument(
        "--owned-email",
        action="append",
        default=[],
        help=(
            "Your own mailbox address for sent/received directionality. "
            "Pass multiple times if needed."
        ),
    )
    args = parser.parse_args()

    mbox_path = Path(args.mbox).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not mbox_path.exists():
        raise FileNotFoundError(f"MBOX file not found: {mbox_path}")

    owned_emails = {normalize_email(value) for value in args.owned_email if value}

    contacts: dict[str, ContactStats] = {}
    edges: Counter[tuple[str, str]] = Counter()
    role_totals = defaultdict(int)
    processed_messages = 0

    mbox = mailbox.mbox(str(mbox_path))
    for message in mbox:
        processed_messages += 1
        seen_at = parse_date(message.get("date"))

        role_addresses: dict[str, set[tuple[str, str]]] = {
            "from": set(parse_addresses(message.get_all("from", []))),
            "to": set(parse_addresses(message.get_all("to", []))),
            "cc": set(parse_addresses(message.get_all("cc", []))),
            "bcc": set(parse_addresses(message.get_all("bcc", []))),
            "reply_to": set(parse_addresses(message.get_all("reply-to", []))),
        }

        for role, pairs in role_addresses.items():
            role_totals[role] += len(pairs)
            count_field = f"{role}_count"
            for name, email_addr in pairs:
                contact = ensure_contact(contacts, email_addr, name)
                setattr(contact, count_field, getattr(contact, count_field) + 1)
                contact.total_mentions += 1
                contact.touch(seen_at)

        from_emails = {email_addr for _, email_addr in role_addresses["from"]}
        recipient_emails = {
            email_addr
            for role in ("to", "cc", "bcc")
            for _, email_addr in role_addresses[role]
        }

        if from_emails and recipient_emails:
            for sender in from_emails:
                for recipient in recipient_emails:
                    if sender != recipient:
                        edges[(sender, recipient)] += 1

        if owned_emails:
            sent_message = bool(from_emails & owned_emails)
            if sent_message:
                for recipient in recipient_emails:
                    contacts[recipient].sent_to_count += 1
            else:
                for sender in from_emails:
                    contacts[sender].received_from_count += 1

    contacts_rows = sorted(
        contacts.values(),
        key=lambda row: (row.total_mentions, row.last_seen or datetime.min.replace(tzinfo=timezone.utc)),
        reverse=True,
    )

    contacts_csv = out_dir / "contacts.csv"
    with contacts_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "email",
                "name",
                "domain",
                "from_count",
                "to_count",
                "cc_count",
                "bcc_count",
                "reply_to_count",
                "sent_to_count",
                "received_from_count",
                "total_mentions",
                "first_seen",
                "last_seen",
                "consent_status",
                "notes",
            ],
        )
        writer.writeheader()
        for row in contacts_rows:
            writer.writerow(
                {
                    "email": row.email,
                    "name": row.name,
                    "domain": row.domain,
                    "from_count": row.from_count,
                    "to_count": row.to_count,
                    "cc_count": row.cc_count,
                    "bcc_count": row.bcc_count,
                    "reply_to_count": row.reply_to_count,
                    "sent_to_count": row.sent_to_count,
                    "received_from_count": row.received_from_count,
                    "total_mentions": row.total_mentions,
                    "first_seen": iso_or_blank(row.first_seen),
                    "last_seen": iso_or_blank(row.last_seen),
                    "consent_status": row.consent_status,
                    "notes": row.notes,
                }
            )

    edges_csv = out_dir / "edges.csv"
    with edges_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "message_count"])
        writer.writeheader()
        for (source, target), message_count in edges.most_common():
            writer.writerow(
                {"source": source, "target": target, "message_count": message_count}
            )

    summary_json = out_dir / "summary.json"
    summary = {
        "mbox_path": str(mbox_path),
        "processed_messages": processed_messages,
        "unique_contacts": len(contacts_rows),
        "owned_emails": sorted(owned_emails),
        "role_totals": dict(role_totals),
        "outputs": {
            "contacts_csv": str(contacts_csv),
            "edges_csv": str(edges_csv),
            "summary_json": str(summary_json),
        },
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
