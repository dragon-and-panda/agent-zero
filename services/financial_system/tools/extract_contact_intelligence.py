#!/usr/bin/env python3
"""
Build contact intelligence tables from authorized mailbox exports and related files.
"""

from __future__ import annotations

import argparse
import csv
import json
import mailbox
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email import message_from_binary_file
from email.message import Message
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Iterable

EMAIL_REGEX = re.compile(r"\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b", re.IGNORECASE)

SUPPORTED_SUFFIXES = {
    ".mbox",
    ".eml",
    ".csv",
    ".tsv",
    ".json",
    ".txt",
    ".md",
    ".log",
}

VALID_STATUSES = {"opt_in", "opt_out", "suppressed", "unknown"}

ROLE_ALIASES = {
    "from": "from",
    "sender": "from",
    "to": "to",
    "recipient": "to",
    "recipients": "to",
    "cc": "cc",
    "bcc": "bcc",
    "reply-to": "reply_to",
    "reply_to": "reply_to",
}

HEADER_ROLE_MAP = {
    "from": "from",
    "sender": "from",
    "to": "to",
    "cc": "cc",
    "bcc": "bcc",
    "reply-to": "reply_to",
}


@dataclass
class ContactStats:
    email: str
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    role_counts: Counter[str] = field(default_factory=Counter)
    direction_counts: Counter[str] = field(default_factory=Counter)
    source_files: set[str] = field(default_factory=set)

    def add(
        self,
        role: str,
        source_file: Path,
        seen_at: datetime | None,
        direction: str,
    ) -> None:
        self.role_counts[role] += 1
        self.direction_counts[direction] += 1
        self.source_files.add(str(source_file))
        if seen_at is None:
            return
        if self.first_seen is None or seen_at < self.first_seen:
            self.first_seen = seen_at
        if self.last_seen is None or seen_at > self.last_seen:
            self.last_seen = seen_at

    @property
    def total_mentions(self) -> int:
        return sum(self.role_counts.values())


@dataclass
class RunStats:
    files_scanned: int = 0
    files_processed: int = 0
    files_skipped: int = 0
    mentions_total: int = 0
    by_role: Counter[str] = field(default_factory=Counter)
    by_direction: Counter[str] = field(default_factory=Counter)
    parser_errors: list[str] = field(default_factory=list)


def normalize_email(value: str) -> str | None:
    value = value.strip().lower()
    value = value.strip("<>[](){}\"'")
    if not value:
        return None
    if value.startswith("mailto:"):
        value = value[7:]
    if "@" not in value:
        return None
    if value.count("@") != 1:
        return None
    local, domain = value.split("@", 1)
    if not local or "." not in domain:
        return None
    return f"{local}@{domain}"


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        pass
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def infer_direction_from_path(path: Path) -> str:
    lowered = {part.lower() for part in path.parts}
    sent_tokens = {"sent", "sent_mail", "sent-items", "sent_items", "outbox"}
    recv_tokens = {"inbox", "received", "archive"}
    if lowered & sent_tokens:
        return "sent"
    if lowered & recv_tokens:
        return "received"
    return "unknown"


def infer_role_from_field(field_name: str) -> str:
    normalized = field_name.strip().lower()
    if not normalized:
        return "other"

    if normalized in ROLE_ALIASES:
        return ROLE_ALIASES[normalized]

    tokens = {token for token in re.split(r"[^a-z0-9]+", normalized) if token}
    if "reply" in tokens and "to" in tokens:
        return "reply_to"
    if "from" in tokens or "sender" in tokens:
        return "from"
    if "to" in tokens or "recipient" in tokens or "recipients" in tokens:
        return "to"
    if "cc" in tokens:
        return "cc"
    if "bcc" in tokens:
        return "bcc"
    return "other"


def parse_address_list(raw_value: str) -> list[str]:
    addresses: list[str] = []
    for _, addr in getaddresses([raw_value]):
        normalized = normalize_email(addr)
        if normalized:
            addresses.append(normalized)
    return addresses


def extract_emails_from_text(raw_text: str) -> list[str]:
    found = []
    for match in EMAIL_REGEX.findall(raw_text):
        normalized = normalize_email(match)
        if normalized:
            found.append(normalized)
    return found


def iter_supported_files(inputs: list[Path]) -> Iterable[Path]:
    for in_path in inputs:
        if in_path.is_file():
            if in_path.suffix.lower() in SUPPORTED_SUFFIXES:
                yield in_path
            continue
        if in_path.is_dir():
            for child in in_path.rglob("*"):
                if child.is_file() and child.suffix.lower() in SUPPORTED_SUFFIXES:
                    yield child


def add_contact_hits(
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
    source_file: Path,
    role: str,
    addresses: Iterable[str],
    seen_at: datetime | None,
    direction: str,
) -> None:
    for address in addresses:
        if address not in contacts:
            contacts[address] = ContactStats(email=address)
        contacts[address].add(
            role=role,
            source_file=source_file,
            seen_at=seen_at,
            direction=direction,
        )
        run_stats.mentions_total += 1
        run_stats.by_role[role] += 1
        run_stats.by_direction[direction] += 1


def process_message(
    msg: Message,
    source_file: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    direction = infer_direction_from_path(source_file)
    seen_at = parse_datetime(msg.get("Date"))

    for header, role in HEADER_ROLE_MAP.items():
        header_value = msg.get(header)
        if not header_value:
            continue
        add_contact_hits(
            contacts=contacts,
            run_stats=run_stats,
            source_file=source_file,
            role=role,
            addresses=parse_address_list(header_value),
            seen_at=seen_at,
            direction=direction,
        )


def process_mbox(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    box = mailbox.mbox(str(file_path))
    for message in box:
        process_message(
            msg=message,
            source_file=file_path,
            contacts=contacts,
            run_stats=run_stats,
        )


def process_eml(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    with file_path.open("rb") as fh:
        msg = message_from_binary_file(fh)
    process_message(msg=msg, source_file=file_path, contacts=contacts, run_stats=run_stats)


def process_csv_or_tsv(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    direction = infer_direction_from_path(file_path)
    delimiter = "\t" if file_path.suffix.lower() == ".tsv" else ","
    with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=delimiter)
        for row in reader:
            seen_at = None
            for key, value in row.items():
                if not key or not value:
                    continue
                lowered_key = key.lower()
                if "date" in lowered_key or "time" in lowered_key:
                    maybe_dt = parse_datetime(str(value))
                    if maybe_dt is not None:
                        seen_at = maybe_dt
                        break

            for key, value in row.items():
                if not key or not value:
                    continue
                role = infer_role_from_field(key)
                emails = (
                    parse_address_list(str(value))
                    if role in {"from", "to", "cc", "bcc", "reply_to"}
                    else extract_emails_from_text(str(value))
                )
                add_contact_hits(
                    contacts=contacts,
                    run_stats=run_stats,
                    source_file=file_path,
                    role=role,
                    addresses=emails,
                    seen_at=seen_at,
                    direction=direction,
                )


def walk_json(value: object, key_path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{key_path}.{key}" if key_path else str(key)
            yield from walk_json(child, child_path)
        return
    if isinstance(value, list):
        for idx, child in enumerate(value):
            child_path = f"{key_path}[{idx}]"
            yield from walk_json(child, child_path)
        return
    if isinstance(value, (str, int, float)):
        yield key_path, str(value)


def process_json(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    direction = infer_direction_from_path(file_path)
    with file_path.open("r", encoding="utf-8", errors="ignore") as fh:
        payload = json.load(fh)

    entries = list(walk_json(payload))
    timestamps: list[datetime] = []
    for key_path, text_value in entries:
        last_key = key_path.split(".")[-1].lower()
        if "date" in last_key or "time" in last_key:
            maybe_dt = parse_datetime(text_value)
            if maybe_dt is not None:
                timestamps.append(maybe_dt)
    seen_at = max(timestamps) if timestamps else None

    for key_path, text_value in entries:
        last_key = key_path.split(".")[-1].lower()
        role = infer_role_from_field(last_key)
        emails = (
            parse_address_list(text_value)
            if role in {"from", "to", "cc", "bcc", "reply_to"}
            else extract_emails_from_text(text_value)
        )
        add_contact_hits(
            contacts=contacts,
            run_stats=run_stats,
            source_file=file_path,
            role=role,
            addresses=emails,
            seen_at=seen_at,
            direction=direction,
        )


def process_text_file(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    direction = infer_direction_from_path(file_path)
    with file_path.open("r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    # Parse RFC822-like header lines when present; fallback to broad extraction otherwise.
    lines = content.splitlines()
    header_matched = False
    seen_at: datetime | None = None
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        lowered_key = key.lower()
        if "date" in lowered_key or "time" in lowered_key:
            maybe_dt = parse_datetime(value)
            if maybe_dt is not None:
                seen_at = maybe_dt
        role = infer_role_from_field(key)
        if role in {"from", "to", "cc", "bcc", "reply_to"}:
            header_matched = True
            add_contact_hits(
                contacts=contacts,
                run_stats=run_stats,
                source_file=file_path,
                role=role,
                addresses=parse_address_list(value),
                seen_at=seen_at,
                direction=direction,
            )

    if not header_matched:
        add_contact_hits(
            contacts=contacts,
            run_stats=run_stats,
            source_file=file_path,
            role="other",
            addresses=extract_emails_from_text(content),
            seen_at=seen_at,
            direction=direction,
        )


def process_file(
    file_path: Path,
    contacts: dict[str, ContactStats],
    run_stats: RunStats,
) -> None:
    suffix = file_path.suffix.lower()
    if suffix == ".mbox":
        process_mbox(file_path, contacts, run_stats)
        return
    if suffix == ".eml":
        process_eml(file_path, contacts, run_stats)
        return
    if suffix in {".csv", ".tsv"}:
        process_csv_or_tsv(file_path, contacts, run_stats)
        return
    if suffix == ".json":
        process_json(file_path, contacts, run_stats)
        return
    if suffix in {".txt", ".md", ".log"}:
        process_text_file(file_path, contacts, run_stats)
        return
    run_stats.files_skipped += 1


def load_consent_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    consent_map: dict[str, str] = {}
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            raw_email = row.get("email", "")
            raw_status = row.get("status", "unknown").strip().lower()
            email = normalize_email(raw_email)
            if not email:
                continue
            status = raw_status if raw_status in VALID_STATUSES else "unknown"
            consent_map[email] = status
    return consent_map


def write_contacts_csv(
    output_dir: Path,
    contacts: dict[str, ContactStats],
    consent_map: dict[str, str],
) -> None:
    out_file = output_dir / "contacts.csv"
    fieldnames = [
        "email",
        "domain",
        "total_mentions",
        "first_seen_utc",
        "last_seen_utc",
        "from_count",
        "to_count",
        "cc_count",
        "bcc_count",
        "reply_to_count",
        "other_count",
        "received_mentions",
        "sent_mentions",
        "unknown_direction_mentions",
        "source_file_count",
        "source_files",
        "consent_status",
        "notes",
    ]

    with out_file.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for email_addr in sorted(contacts, key=lambda e: contacts[e].total_mentions, reverse=True):
            item = contacts[email_addr]
            domain = email_addr.split("@", 1)[1]
            writer.writerow(
                {
                    "email": email_addr,
                    "domain": domain,
                    "total_mentions": item.total_mentions,
                    "first_seen_utc": item.first_seen.isoformat() if item.first_seen else "",
                    "last_seen_utc": item.last_seen.isoformat() if item.last_seen else "",
                    "from_count": item.role_counts["from"],
                    "to_count": item.role_counts["to"],
                    "cc_count": item.role_counts["cc"],
                    "bcc_count": item.role_counts["bcc"],
                    "reply_to_count": item.role_counts["reply_to"],
                    "other_count": item.role_counts["other"],
                    "received_mentions": item.direction_counts["received"],
                    "sent_mentions": item.direction_counts["sent"],
                    "unknown_direction_mentions": item.direction_counts["unknown"],
                    "source_file_count": len(item.source_files),
                    "source_files": ";".join(sorted(item.source_files)),
                    "consent_status": consent_map.get(email_addr, "unknown"),
                    "notes": "",
                }
            )


def write_domains_csv(
    output_dir: Path,
    contacts: dict[str, ContactStats],
    consent_map: dict[str, str],
) -> None:
    domain_stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for email_addr, stats in contacts.items():
        domain = email_addr.split("@", 1)[1]
        domain_stats[domain]["contact_count"] += 1
        domain_stats[domain]["total_mentions"] += stats.total_mentions
        status = consent_map.get(email_addr, "unknown")
        domain_stats[domain][f"{status}_contacts"] += 1

    out_file = output_dir / "domains.csv"
    fieldnames = [
        "domain",
        "contact_count",
        "total_mentions",
        "opt_in_contacts",
        "opt_out_contacts",
        "suppressed_contacts",
        "unknown_contacts",
    ]
    with out_file.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for domain in sorted(
            domain_stats,
            key=lambda d: domain_stats[d]["total_mentions"],
            reverse=True,
        ):
            row = domain_stats[domain]
            writer.writerow(
                {
                    "domain": domain,
                    "contact_count": row["contact_count"],
                    "total_mentions": row["total_mentions"],
                    "opt_in_contacts": row["opt_in_contacts"],
                    "opt_out_contacts": row["opt_out_contacts"],
                    "suppressed_contacts": row["suppressed_contacts"],
                    "unknown_contacts": row["unknown_contacts"],
                }
            )


def write_summary_json(
    output_dir: Path,
    run_stats: RunStats,
    contacts: dict[str, ContactStats],
) -> None:
    out_file = output_dir / "summary.json"
    summary = {
        "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "files_scanned": run_stats.files_scanned,
        "files_processed": run_stats.files_processed,
        "files_skipped": run_stats.files_skipped,
        "contacts_found": len(contacts),
        "mentions_total": run_stats.mentions_total,
        "mentions_by_role": dict(sorted(run_stats.by_role.items())),
        "mentions_by_direction": dict(sorted(run_stats.by_direction.items())),
        "parser_errors": run_stats.parser_errors,
    }
    with out_file.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract contact intelligence tables from authorized mailbox data."
    )
    parser.add_argument(
        "--input",
        dest="inputs",
        action="append",
        required=True,
        help="Input file or directory. Pass multiple times for multiple sources.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Output directory for contacts.csv, domains.csv, and summary.json",
    )
    parser.add_argument(
        "--consent-file",
        default=None,
        help="Optional CSV with columns email,status",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_paths = [Path(p).expanduser().resolve() for p in args.inputs]
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    consent_map = load_consent_map(
        Path(args.consent_file).expanduser().resolve() if args.consent_file else None
    )

    contacts: dict[str, ContactStats] = {}
    run_stats = RunStats()

    for file_path in iter_supported_files(input_paths):
        run_stats.files_scanned += 1
        try:
            process_file(file_path, contacts, run_stats)
            run_stats.files_processed += 1
        except Exception as exc:  # pragma: no cover - defensive by design
            run_stats.files_skipped += 1
            run_stats.parser_errors.append(f"{file_path}: {exc}")

    write_contacts_csv(output_dir, contacts, consent_map)
    write_domains_csv(output_dir, contacts, consent_map)
    write_summary_json(output_dir, run_stats, contacts)

    print(f"Processed files: {run_stats.files_processed}/{run_stats.files_scanned}")
    print(f"Contacts found: {len(contacts)}")
    print(f"Mentions total: {run_stats.mentions_total}")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
