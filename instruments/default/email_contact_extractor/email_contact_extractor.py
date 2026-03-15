#!/usr/bin/env python3
"""Extract and normalize contact addresses from mailbox files.

This utility is designed for first-party, permissioned mailbox data.
Use of extracted contacts must comply with applicable laws and platform terms.
"""

from __future__ import annotations

import argparse
import csv
import json
import mailbox
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


FIELD_ROLE_MAP = {
    "from": ["from", "sender", "reply-to", "return-path"],
    "to": ["to", "resent-to", "delivered-to"],
    "cc": ["cc", "resent-cc"],
    "bcc": ["bcc", "resent-bcc"],
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class ContactStats:
    email: str
    name: str = ""
    total_occurrences: int = 0
    roles: Counter = field(default_factory=Counter)
    fields: Counter = field(default_factory=Counter)
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    sample_sources: List[str] = field(default_factory=list)

    def absorb_timestamp(self, timestamp: Optional[str]) -> None:
        if not timestamp:
            return
        if self.first_seen is None or timestamp < self.first_seen:
            self.first_seen = timestamp
        if self.last_seen is None or timestamp > self.last_seen:
            self.last_seen = timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract deduplicated contacts from .mbox/.eml files."
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="Input file or directory (can be repeated).",
    )
    parser.add_argument(
        "--output-csv",
        required=True,
        help="Output CSV path for deduplicated contacts.",
    )
    parser.add_argument(
        "--output-json",
        default="",
        help="Optional summary JSON path. Defaults to <output-csv>.summary.json",
    )
    parser.add_argument(
        "--consent-csv",
        default="",
        help="Optional CSV with columns: email, consent_status, suppressed",
    )
    parser.add_argument(
        "--allow-domain",
        action="append",
        default=[],
        help="Only include addresses from these domains (repeatable).",
    )
    parser.add_argument(
        "--exclude-domain",
        action="append",
        default=[],
        help="Exclude addresses from these domains (repeatable).",
    )
    parser.add_argument(
        "--max-sources-per-contact",
        type=int,
        default=5,
        help="Max number of sample sources stored per contact.",
    )
    return parser.parse_args()


def normalize_email(value: str) -> Optional[str]:
    cleaned = value.strip().lower()
    if not cleaned:
        return None
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip().lower()
    if not EMAIL_RE.match(cleaned):
        return None
    return cleaned


def parse_date_header(date_value: Optional[str]) -> Optional[str]:
    if not date_value:
        return None
    try:
        dt = parsedate_to_datetime(date_value)
    except (TypeError, ValueError):
        return None
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def serialize_counter(counter: Counter) -> str:
    if not counter:
        return ""
    parts = [f"{key}:{counter[key]}" for key in sorted(counter)]
    return ";".join(parts)


def gather_input_files(inputs: Sequence[str]) -> List[Path]:
    discovered: List[Path] = []
    for raw_path in inputs:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            continue
        if path.is_file():
            discovered.append(path)
            continue
        for file_path in path.rglob("*"):
            if file_path.is_file():
                discovered.append(file_path)
    return discovered


def is_mbox_file(path: Path) -> bool:
    lower = path.name.lower()
    return lower.endswith(".mbox") or lower.endswith(".mbx")


def is_eml_file(path: Path) -> bool:
    lower = path.name.lower()
    return lower.endswith(".eml") or lower.endswith(".email") or lower.endswith(".msg")


def load_consent_map(consent_path: str) -> Dict[str, Dict[str, str]]:
    if not consent_path:
        return {}
    path = Path(consent_path).expanduser().resolve()
    if not path.exists():
        return {}

    output: Dict[str, Dict[str, str]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            email_value = normalize_email((row.get("email") or "").strip())
            if not email_value:
                continue
            output[email_value] = {
                "consent_status": (row.get("consent_status") or "unknown").strip() or "unknown",
                "suppressed": (row.get("suppressed") or "").strip() or "false",
            }
    return output


def should_include_domain(email_value: str, allow: Set[str], exclude: Set[str]) -> bool:
    domain = email_value.rsplit("@", 1)[-1]
    if allow and domain not in allow:
        return False
    if domain in exclude:
        return False
    return True


def update_contact(
    contacts: Dict[str, ContactStats],
    name: str,
    email_value: str,
    role: str,
    field_name: str,
    timestamp: Optional[str],
    source: str,
    max_sources_per_contact: int,
) -> None:
    item = contacts.get(email_value)
    if item is None:
        item = ContactStats(email=email_value)
        contacts[email_value] = item

    normalized_name = (name or "").strip()
    if normalized_name and len(normalized_name) > len(item.name):
        item.name = normalized_name

    item.total_occurrences += 1
    item.roles[role] += 1
    item.fields[field_name.lower()] += 1
    item.absorb_timestamp(timestamp)

    if len(item.sample_sources) < max_sources_per_contact and source not in item.sample_sources:
        item.sample_sources.append(source)


def iter_message_addresses(message) -> Iterable[Tuple[str, str, str]]:
    for role, field_names in FIELD_ROLE_MAP.items():
        for field_name in field_names:
            raw_values = message.get_all(field_name, [])
            if not raw_values:
                continue
            for name, email_value in getaddresses(raw_values):
                normalized = normalize_email(email_value or "")
                if not normalized:
                    continue
                yield role, field_name, name, normalized


def process_mbox(
    file_path: Path,
    contacts: Dict[str, ContactStats],
    role_counts: Counter,
    domain_counts: Counter,
    allow_domains: Set[str],
    exclude_domains: Set[str],
    max_sources_per_contact: int,
) -> int:
    processed_messages = 0
    box = mailbox.mbox(str(file_path))
    for index, message in enumerate(box, start=1):
        processed_messages += 1
        timestamp = parse_date_header(message.get("date"))
        source = f"{file_path}:{index}"
        for role, field_name, name, email_value in iter_message_addresses(message):
            if not should_include_domain(email_value, allow_domains, exclude_domains):
                continue
            update_contact(
                contacts=contacts,
                name=name,
                email_value=email_value,
                role=role,
                field_name=field_name,
                timestamp=timestamp,
                source=source,
                max_sources_per_contact=max_sources_per_contact,
            )
            role_counts[role] += 1
            domain_counts[email_value.rsplit("@", 1)[-1]] += 1
    return processed_messages


def process_eml(
    file_path: Path,
    contacts: Dict[str, ContactStats],
    role_counts: Counter,
    domain_counts: Counter,
    allow_domains: Set[str],
    exclude_domains: Set[str],
    max_sources_per_contact: int,
) -> int:
    data = file_path.read_bytes()
    message = BytesParser(policy=policy.default).parsebytes(data)
    timestamp = parse_date_header(message.get("date"))
    source = str(file_path)
    for role, field_name, name, email_value in iter_message_addresses(message):
        if not should_include_domain(email_value, allow_domains, exclude_domains):
            continue
        update_contact(
            contacts=contacts,
            name=name,
            email_value=email_value,
            role=role,
            field_name=field_name,
            timestamp=timestamp,
            source=source,
            max_sources_per_contact=max_sources_per_contact,
        )
        role_counts[role] += 1
        domain_counts[email_value.rsplit("@", 1)[-1]] += 1
    return 1


def write_contacts_csv(
    output_path: Path,
    contacts: Dict[str, ContactStats],
    consent_map: Dict[str, Dict[str, str]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "email",
                "name",
                "total_occurrences",
                "roles",
                "header_fields",
                "first_seen",
                "last_seen",
                "sample_sources",
                "consent_status",
                "suppressed",
            ],
        )
        writer.writeheader()
        for email_value in sorted(contacts):
            item = contacts[email_value]
            consent = consent_map.get(email_value, {})
            writer.writerow(
                {
                    "email": item.email,
                    "name": item.name,
                    "total_occurrences": item.total_occurrences,
                    "roles": serialize_counter(item.roles),
                    "header_fields": serialize_counter(item.fields),
                    "first_seen": item.first_seen or "",
                    "last_seen": item.last_seen or "",
                    "sample_sources": "|".join(item.sample_sources),
                    "consent_status": consent.get("consent_status", "unknown"),
                    "suppressed": consent.get("suppressed", "false"),
                }
            )


def main() -> int:
    args = parse_args()
    input_files = gather_input_files(args.input)
    if not input_files:
        raise SystemExit("No input files found.")

    allow_domains = {d.strip().lower() for d in args.allow_domain if d.strip()}
    exclude_domains = {d.strip().lower() for d in args.exclude_domain if d.strip()}

    contacts: Dict[str, ContactStats] = {}
    role_counts: Counter = Counter()
    domain_counts: Counter = Counter()
    processed_messages = 0
    processed_files = 0

    for path in input_files:
        try:
            if is_mbox_file(path):
                processed_messages += process_mbox(
                    file_path=path,
                    contacts=contacts,
                    role_counts=role_counts,
                    domain_counts=domain_counts,
                    allow_domains=allow_domains,
                    exclude_domains=exclude_domains,
                    max_sources_per_contact=args.max_sources_per_contact,
                )
                processed_files += 1
                continue
            if is_eml_file(path):
                processed_messages += process_eml(
                    file_path=path,
                    contacts=contacts,
                    role_counts=role_counts,
                    domain_counts=domain_counts,
                    allow_domains=allow_domains,
                    exclude_domains=exclude_domains,
                    max_sources_per_contact=args.max_sources_per_contact,
                )
                processed_files += 1
        except Exception:
            # Skip malformed or unsupported files while keeping the run resilient.
            continue

    consent_map = load_consent_map(args.consent_csv)
    output_csv = Path(args.output_csv).expanduser().resolve()
    write_contacts_csv(output_csv, contacts, consent_map)

    output_json = args.output_json
    if not output_json:
        output_json = str(output_csv) + ".summary.json"

    consent_breakdown = Counter()
    for email_value in contacts:
        consent_breakdown[consent_map.get(email_value, {}).get("consent_status", "unknown")] += 1

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [str(Path(p).expanduser().resolve()) for p in args.input],
        "processed_files": processed_files,
        "processed_messages": processed_messages,
        "contacts_total": len(contacts),
        "role_counts": dict(sorted(role_counts.items())),
        "domain_counts_top_20": dict(domain_counts.most_common(20)),
        "consent_breakdown": dict(sorted(consent_breakdown.items())),
        "output_csv": str(output_csv),
    }

    summary_path = Path(output_json).expanduser().resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
