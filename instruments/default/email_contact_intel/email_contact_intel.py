#!/usr/bin/env python3

"""Extract contact intelligence from authorized email and text exports."""

from __future__ import annotations

import argparse
import csv
import json
import mailbox
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Iterable


EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


@dataclass
class ContactStats:
    counts: Counter = field(default_factory=Counter)
    names: Counter = field(default_factory=Counter)
    first_seen: datetime | None = None
    last_seen: datetime | None = None

    def add(self, source: str, when: datetime | None, display_name: str | None = None) -> None:
        self.counts[source] += 1
        if display_name:
            cleaned = " ".join(display_name.split()).strip()
            if cleaned:
                self.names[cleaned] += 1
        if when:
            if self.first_seen is None or when < self.first_seen:
                self.first_seen = when
            if self.last_seen is None or when > self.last_seen:
                self.last_seen = when

    @property
    def total_count(self) -> int:
        return int(sum(self.counts.values()))


def normalize_email(raw: str) -> str | None:
    value = raw.strip().lower()
    if not value:
        return None
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    if "@" not in value or value.startswith("@") or value.endswith("@"):
        return None
    if ".." in value:
        return None
    if not re.fullmatch(r"[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}", value):
        return None
    return value


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def header_addresses(message: mailbox.mboxMessage, header_names: Iterable[str]) -> list[tuple[str, str]]:
    values: list[str] = []
    for header_name in header_names:
        for value in message.get_all(header_name, []):
            values.append(value)
    pairs = []
    for name, addr in getaddresses(values):
        normalized = normalize_email(addr)
        if normalized:
            pairs.append((name, normalized))
    return pairs


def resolve_direction(
    owner_emails: set[str],
    from_addresses: set[str],
    recipient_addresses: set[str],
) -> str:
    is_sent = bool(from_addresses & owner_emails)
    is_received = bool(recipient_addresses & owner_emails)
    if is_sent and not is_received:
        return "sent"
    if is_received and not is_sent:
        return "received"
    if is_received and is_sent:
        return "internal"
    return "unknown"


def write_contacts_csv(path: Path, contacts: list[dict[str, object]]) -> None:
    fieldnames = [
        "email",
        "total_count",
        "first_seen_utc",
        "last_seen_utc",
        "sources_json",
        "display_names_json",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)


def iso_or_empty(value: datetime | None) -> str:
    if not value:
        return ""
    return value.isoformat().replace("+00:00", "Z")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract deduplicated contact intelligence from authorized email/text exports."
    )
    parser.add_argument(
        "--mbox",
        action="append",
        default=[],
        help="Path to an .mbox file. Provide multiple times for multiple files.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Path to additional text-like file(s) to scan for email addresses.",
    )
    parser.add_argument(
        "--owner",
        action="append",
        default=[],
        help="Owner email(s) used to classify sent vs received messages.",
    )
    parser.add_argument(
        "--output-dir",
        default="output/email_contact_intel",
        help="Output directory for contacts.csv, contacts.json, and summary.json.",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="Minimum total observations required to keep a contact.",
    )
    parser.add_argument(
        "--include-owner",
        action="store_true",
        help="Include owner addresses in output (excluded by default).",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    mbox_paths = [Path(item).expanduser().resolve() for item in args.mbox]
    file_paths = [Path(item).expanduser().resolve() for item in args.file]
    owner_emails = {normalized for raw in args.owner if (normalized := normalize_email(raw))}

    if not mbox_paths and not file_paths:
        parser.error("At least one --mbox or --file input is required.")

    contact_map: dict[str, ContactStats] = defaultdict(ContactStats)
    processed_messages = 0
    scanned_files = 0

    for mbox_path in mbox_paths:
        if not mbox_path.exists():
            raise FileNotFoundError(f"Mbox file not found: {mbox_path}")
        mbox_obj = mailbox.mbox(str(mbox_path))
        for message in mbox_obj:
            processed_messages += 1
            observed_at = parse_date(message.get("Date"))

            from_pairs = header_addresses(message, ["From"])
            to_pairs = header_addresses(message, ["To", "Delivered-To", "X-Original-To"])
            cc_pairs = header_addresses(message, ["Cc"])
            bcc_pairs = header_addresses(message, ["Bcc"])
            reply_to_pairs = header_addresses(message, ["Reply-To"])

            from_addrs = {addr for _, addr in from_pairs}
            recipient_addrs = {addr for _, addr in to_pairs + cc_pairs + bcc_pairs}
            direction = resolve_direction(owner_emails, from_addrs, recipient_addrs) if owner_emails else "unknown"

            bucket_map = {
                "from": from_pairs,
                "to": to_pairs,
                "cc": cc_pairs,
                "bcc": bcc_pairs,
                "reply_to": reply_to_pairs,
            }
            for bucket, pairs in bucket_map.items():
                source = f"{direction}_{bucket}"
                for display_name, email_value in pairs:
                    if not args.include_owner and email_value in owner_emails:
                        continue
                    contact_map[email_value].add(source=source, when=observed_at, display_name=display_name)

    for file_path in file_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"Additional file not found: {file_path}")
        scanned_files += 1
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        file_time = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
        for raw_match in EMAIL_REGEX.findall(text):
            normalized = normalize_email(raw_match)
            if not normalized:
                continue
            if not args.include_owner and normalized in owner_emails:
                continue
            contact_map[normalized].add(source="other_files", when=file_time, display_name=None)

    records: list[dict[str, object]] = []
    for email_value, stats in contact_map.items():
        if stats.total_count < args.min_count:
            continue
        records.append(
            {
                "email": email_value,
                "total_count": stats.total_count,
                "first_seen_utc": iso_or_empty(stats.first_seen),
                "last_seen_utc": iso_or_empty(stats.last_seen),
                "sources_json": json.dumps(dict(stats.counts), sort_keys=True),
                "display_names_json": json.dumps(dict(stats.names.most_common(5)), ensure_ascii=True),
            }
        )

    records.sort(key=lambda item: (-int(item["total_count"]), str(item["email"])))

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    contacts_csv_path = output_dir / "contacts.csv"
    contacts_json_path = output_dir / "contacts.json"
    summary_json_path = output_dir / "summary.json"

    write_contacts_csv(contacts_csv_path, records)
    contacts_json_path.write_text(json.dumps(records, indent=2, sort_keys=False), encoding="utf-8")

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "mbox_files": [str(path) for path in mbox_paths],
        "additional_files": [str(path) for path in file_paths],
        "owner_emails": sorted(owner_emails),
        "processed_messages": processed_messages,
        "scanned_files": scanned_files,
        "unique_contacts": len(records),
        "min_count": args.min_count,
        "include_owner": bool(args.include_owner),
    }
    summary_json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Processed messages: {processed_messages}")
    print(f"Scanned additional files: {scanned_files}")
    print(f"Unique contacts saved: {len(records)}")
    print(f"Output directory: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
