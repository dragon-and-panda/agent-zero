#!/usr/bin/env python3
"""
Extract contact emails from exported email data.

Supported inputs:
- mbox files
- .eml files
- plain text files (regex-based address scan)

This utility is designed for consent-based CRM and relationship management
workflows. It is not intended for spam or unauthorized data resale.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import email
import mailbox
import re
from collections import Counter
from dataclasses import dataclass, field
from email.message import Message
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Iterable, Iterator


EMAIL_REGEX = re.compile(r"[A-Z0-9._%+\-']+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.IGNORECASE)
SUPPORTED_FILE_SUFFIXES = {".mbox", ".eml", ".txt"}
HEADER_SOURCES = [
    "from",
    "to",
    "cc",
    "bcc",
    "reply-to",
    "sender",
    "resent-from",
    "resent-to",
    "resent-cc",
]


@dataclass
class ContactRecord:
    email: str
    names: Counter[str] = field(default_factory=Counter)
    sources: Counter[str] = field(default_factory=Counter)
    first_seen: dt.datetime | None = None
    last_seen: dt.datetime | None = None
    message_count: int = 0

    def register(
        self,
        display_name: str,
        source: str,
        seen_at: dt.datetime | None,
    ) -> None:
        if display_name:
            self.names[display_name] += 1
        self.sources[source] += 1
        self.message_count += 1

        if seen_at is None:
            return
        if self.first_seen is None or seen_at < self.first_seen:
            self.first_seen = seen_at
        if self.last_seen is None or seen_at > self.last_seen:
            self.last_seen = seen_at

    def best_name(self) -> str:
        if not self.names:
            return ""
        return self.names.most_common(1)[0][0]

    def sources_str(self) -> str:
        return ";".join(sorted(self.sources.keys()))

    def to_csv_row(self) -> dict[str, str | int]:
        return {
            "email": self.email,
            "name": self.best_name(),
            "message_count": self.message_count,
            "first_seen": to_iso(self.first_seen),
            "last_seen": to_iso(self.last_seen),
            "sources": self.sources_str(),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract and deduplicate emails from mbox/eml/txt files for "
            "consent-based contact management."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input files or directories (mbox, .eml, .txt).",
    )
    parser.add_argument(
        "--output-csv",
        default="contacts.csv",
        help="Path for CSV output (default: contacts.csv).",
    )
    parser.add_argument(
        "--exclude-domain",
        action="append",
        default=[],
        help="Domain to exclude (can be provided multiple times).",
    )
    parser.add_argument(
        "--include-bcc",
        action="store_true",
        help="Include BCC headers when present in exported data.",
    )
    return parser.parse_args()


def iter_input_files(inputs: list[str]) -> Iterator[Path]:
    for entry in inputs:
        path = Path(entry).expanduser().resolve()
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_FILE_SUFFIXES:
            yield path
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in SUPPORTED_FILE_SUFFIXES:
                    yield child


def iter_mbox_messages(path: Path) -> Iterator[Message]:
    box = mailbox.mbox(str(path))
    for message in box:
        if isinstance(message, Message):
            yield message
            continue
        parsed = email.message_from_bytes(bytes(message))
        yield parsed


def iter_eml_message(path: Path) -> Iterator[Message]:
    with path.open("rb") as file:
        yield email.message_from_binary_file(file)


def iter_text_candidates(path: Path) -> Iterator[tuple[str, str, dt.datetime | None]]:
    mtime = dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)
    content = path.read_text(encoding="utf-8", errors="ignore")
    for match in EMAIL_REGEX.findall(content):
        yield "", normalize_email(match), mtime


def normalize_email(candidate: str) -> str:
    email_clean = candidate.strip().lower()
    if email_clean.startswith("<") and email_clean.endswith(">"):
        email_clean = email_clean[1:-1]
    return email_clean


def is_valid_email(candidate: str) -> bool:
    return bool(EMAIL_REGEX.fullmatch(candidate))


def message_date(message: Message) -> dt.datetime | None:
    raw = message.get("date")
    if not raw:
        return None
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def to_iso(value: dt.datetime | None) -> str:
    if value is None:
        return ""
    return value.isoformat()


def extract_from_message(
    message: Message,
    include_bcc: bool,
) -> Iterable[tuple[str, str, str, dt.datetime | None]]:
    seen_at = message_date(message)
    for header in HEADER_SOURCES:
        if header == "bcc" and not include_bcc:
            continue
        values = message.get_all(header, [])
        if not values:
            continue
        for display_name, address in getaddresses(values):
            email_normalized = normalize_email(address)
            if not is_valid_email(email_normalized):
                continue
            yield display_name.strip(), email_normalized, header, seen_at


def save_csv(path: Path, records: list[ContactRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "email",
                "name",
                "message_count",
                "first_seen",
                "last_seen",
                "sources",
            ],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_csv_row())


def main() -> int:
    args = parse_args()
    exclude_domains = {domain.lower().strip() for domain in args.exclude_domain}

    contacts: dict[str, ContactRecord] = {}
    scanned_files = 0

    for file_path in iter_input_files(args.inputs):
        scanned_files += 1
        suffix = file_path.suffix.lower()

        if suffix == ".mbox":
            for message in iter_mbox_messages(file_path):
                for display_name, email_addr, source, seen_at in extract_from_message(
                    message, include_bcc=args.include_bcc
                ):
                    domain = email_addr.split("@", 1)[-1]
                    if domain in exclude_domains:
                        continue
                    record = contacts.setdefault(email_addr, ContactRecord(email=email_addr))
                    record.register(display_name, source, seen_at)
            continue

        if suffix == ".eml":
            for message in iter_eml_message(file_path):
                for display_name, email_addr, source, seen_at in extract_from_message(
                    message, include_bcc=args.include_bcc
                ):
                    domain = email_addr.split("@", 1)[-1]
                    if domain in exclude_domains:
                        continue
                    record = contacts.setdefault(email_addr, ContactRecord(email=email_addr))
                    record.register(display_name, source, seen_at)
            continue

        if suffix == ".txt":
            for display_name, email_addr, seen_at in iter_text_candidates(file_path):
                domain = email_addr.split("@", 1)[-1]
                if domain in exclude_domains:
                    continue
                record = contacts.setdefault(email_addr, ContactRecord(email=email_addr))
                record.register(display_name, "text_scan", seen_at)

    records = sorted(contacts.values(), key=lambda rec: rec.email)
    output_csv = Path(args.output_csv).expanduser().resolve()
    save_csv(output_csv, records)

    print(f"Scanned files: {scanned_files}")
    print(f"Unique contacts: {len(records)}")
    print(f"CSV written to: {output_csv}")
    if exclude_domains:
        print(f"Excluded domains: {', '.join(sorted(exclude_domains))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
