from __future__ import annotations

import argparse
import csv
import json
import mailbox
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email import policy
from email.message import Message
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Dict, Iterable, Iterator


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
TEXT_FILE_EXTENSIONS = {".txt", ".csv", ".json", ".md", ".log"}


@dataclass
class ContactRecord:
    email: str
    total_mentions: int = 0
    from_mentions: int = 0
    to_mentions: int = 0
    cc_mentions: int = 0
    bcc_mentions: int = 0
    reply_to_mentions: int = 0
    body_mentions: int = 0
    file_mentions: int = 0
    received_mentions: int = 0
    sent_mentions: int = 0
    unknown_direction_mentions: int = 0
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    source_files: set[str] = field(default_factory=set)

    def apply_seen_time(self, seen_at: datetime) -> None:
        if self.first_seen is None or seen_at < self.first_seen:
            self.first_seen = seen_at
        if self.last_seen is None or seen_at > self.last_seen:
            self.last_seen = seen_at

    def as_csv_row(self) -> dict:
        return {
            "email": self.email,
            "total_mentions": self.total_mentions,
            "from_mentions": self.from_mentions,
            "to_mentions": self.to_mentions,
            "cc_mentions": self.cc_mentions,
            "bcc_mentions": self.bcc_mentions,
            "reply_to_mentions": self.reply_to_mentions,
            "body_mentions": self.body_mentions,
            "file_mentions": self.file_mentions,
            "received_mentions": self.received_mentions,
            "sent_mentions": self.sent_mentions,
            "unknown_direction_mentions": self.unknown_direction_mentions,
            "first_seen_utc": self.first_seen.isoformat() if self.first_seen else "",
            "last_seen_utc": self.last_seen.isoformat() if self.last_seen else "",
            "source_file_count": len(self.source_files),
            "source_files": ";".join(sorted(self.source_files)),
        }


def normalize_email(value: str) -> str | None:
    cleaned = value.strip().strip("<>").lower()
    if not cleaned:
        return None
    if not EMAIL_RE.fullmatch(cleaned):
        return None
    return cleaned


def parse_header_addresses(message: Message, header: str) -> list[str]:
    addresses = getaddresses(message.get_all(header, []))
    out: list[str] = []
    for _, raw in addresses:
        normalized = normalize_email(raw)
        if normalized:
            out.append(normalized)
    return out


def parse_seen_time(message: Message) -> datetime:
    raw_date = message.get("Date", "")
    if raw_date:
        try:
            parsed = parsedate_to_datetime(raw_date)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except Exception:
            pass
    return datetime.now(tz=timezone.utc)


def classify_direction(message: Message, owner_emails: set[str]) -> str:
    if not owner_emails:
        return "unknown"
    from_addrs = set(parse_header_addresses(message, "From"))
    recip_addrs = set(parse_header_addresses(message, "To"))
    recip_addrs.update(parse_header_addresses(message, "Cc"))
    recip_addrs.update(parse_header_addresses(message, "Bcc"))
    owner_in_from = bool(from_addrs.intersection(owner_emails))
    owner_in_recipients = bool(recip_addrs.intersection(owner_emails))
    if owner_in_from and not owner_in_recipients:
        return "sent"
    if owner_in_recipients and not owner_in_from:
        return "received"
    return "unknown"


def iter_body_emails(message: Message) -> Iterator[str]:
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type() or ""
            if not content_type.startswith("text/"):
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            text = payload.decode(errors="ignore")
            for raw in EMAIL_RE.findall(text):
                normalized = normalize_email(raw)
                if normalized:
                    yield normalized
        return
    payload = message.get_payload(decode=True)
    if not payload:
        return
    text = payload.decode(errors="ignore")
    for raw in EMAIL_RE.findall(text):
        normalized = normalize_email(raw)
        if normalized:
            yield normalized


def update_contact(
    contacts: Dict[str, ContactRecord],
    *,
    email_addr: str,
    source_file: str,
    seen_at: datetime,
    role: str,
    direction: str,
) -> None:
    rec = contacts.setdefault(email_addr, ContactRecord(email=email_addr))
    rec.total_mentions += 1
    rec.apply_seen_time(seen_at)
    rec.source_files.add(source_file)

    if role == "from":
        rec.from_mentions += 1
    elif role == "to":
        rec.to_mentions += 1
    elif role == "cc":
        rec.cc_mentions += 1
    elif role == "bcc":
        rec.bcc_mentions += 1
    elif role == "reply_to":
        rec.reply_to_mentions += 1
    elif role == "body":
        rec.body_mentions += 1
    elif role == "file":
        rec.file_mentions += 1

    if direction == "received":
        rec.received_mentions += 1
    elif direction == "sent":
        rec.sent_mentions += 1
    else:
        rec.unknown_direction_mentions += 1


def process_message(
    contacts: Dict[str, ContactRecord],
    *,
    message: Message,
    source_file: str,
    owner_emails: set[str],
    include_owner: bool,
    scan_body: bool,
) -> None:
    seen_at = parse_seen_time(message)
    direction = classify_direction(message, owner_emails)
    header_map = {
        "from": "From",
        "to": "To",
        "cc": "Cc",
        "bcc": "Bcc",
        "reply_to": "Reply-To",
    }
    for role, header in header_map.items():
        for email_addr in parse_header_addresses(message, header):
            if not include_owner and email_addr in owner_emails:
                continue
            update_contact(
                contacts,
                email_addr=email_addr,
                source_file=source_file,
                seen_at=seen_at,
                role=role,
                direction=direction,
            )
    if scan_body:
        for email_addr in iter_body_emails(message):
            if not include_owner and email_addr in owner_emails:
                continue
            update_contact(
                contacts,
                email_addr=email_addr,
                source_file=source_file,
                seen_at=seen_at,
                role="body",
                direction=direction,
            )


def process_text_file(
    contacts: Dict[str, ContactRecord],
    *,
    path: Path,
    owner_emails: set[str],
    include_owner: bool,
) -> None:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return
    now = datetime.now(tz=timezone.utc)
    for raw in EMAIL_RE.findall(content):
        normalized = normalize_email(raw)
        if not normalized:
            continue
        if not include_owner and normalized in owner_emails:
            continue
        update_contact(
            contacts,
            email_addr=normalized,
            source_file=str(path),
            seen_at=now,
            role="file",
            direction="unknown",
        )


def iter_input_files(input_path: Path) -> Iterator[Path]:
    if input_path.is_file():
        yield input_path
        return
    for path in input_path.rglob("*"):
        if path.is_file():
            yield path


def process_inputs(
    input_path: Path,
    *,
    owner_emails: set[str],
    include_owner: bool,
    scan_body: bool,
) -> dict[str, ContactRecord]:
    contacts: dict[str, ContactRecord] = {}
    for path in iter_input_files(input_path):
        suffix = path.suffix.lower()
        if suffix == ".mbox":
            try:
                box = mailbox.mbox(path)
                for message in box:
                    process_message(
                        contacts,
                        message=message,
                        source_file=str(path),
                        owner_emails=owner_emails,
                        include_owner=include_owner,
                        scan_body=scan_body,
                    )
            except Exception:
                continue
        elif suffix == ".eml":
            try:
                with path.open("rb") as fh:
                    message = BytesParser(policy=policy.default).parse(fh)
                process_message(
                    contacts,
                    message=message,
                    source_file=str(path),
                    owner_emails=owner_emails,
                    include_owner=include_owner,
                    scan_body=scan_body,
                )
            except Exception:
                continue
        elif suffix in TEXT_FILE_EXTENSIONS:
            process_text_file(
                contacts,
                path=path,
                owner_emails=owner_emails,
                include_owner=include_owner,
            )
    return contacts


def write_csv(out_csv: Path, contacts: Iterable[ContactRecord], min_mentions: int) -> int:
    rows = [
        c.as_csv_row()
        for c in contacts
        if c.total_mentions >= min_mentions
    ]
    rows.sort(key=lambda row: (-int(row["total_mentions"]), row["email"]))
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "email",
        "total_mentions",
        "from_mentions",
        "to_mentions",
        "cc_mentions",
        "bcc_mentions",
        "reply_to_mentions",
        "body_mentions",
        "file_mentions",
        "received_mentions",
        "sent_mentions",
        "unknown_direction_mentions",
        "first_seen_utc",
        "last_seen_utc",
        "source_file_count",
        "source_files",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_summary(
    out_json: Path,
    *,
    contacts: dict[str, ContactRecord],
    exported_count: int,
    owner_emails: set[str],
    input_path: Path,
    min_mentions: int,
) -> None:
    summary = {
        "input_path": str(input_path),
        "owner_emails": sorted(owner_emails),
        "total_unique_contacts": len(contacts),
        "exported_contacts": exported_count,
        "min_mentions": min_mentions,
        "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract and de-duplicate email contacts from mailbox exports. "
            "Use only on data you own or are authorized to process."
        )
    )
    parser.add_argument("--input", required=True, help="Path to a file or directory with .mbox/.eml/text files.")
    parser.add_argument("--out-csv", default="contacts_for_orange.csv", help="Output CSV path.")
    parser.add_argument("--out-json", default="contacts_summary.json", help="Output JSON summary path.")
    parser.add_argument(
        "--owner-email",
        action="append",
        default=[],
        help="Owner account email address. Add multiple times when needed.",
    )
    parser.add_argument(
        "--include-owner",
        action="store_true",
        help="Include owner email addresses in output (excluded by default).",
    )
    parser.add_argument(
        "--scan-body",
        action="store_true",
        help="Also scan email body text for addresses (off by default).",
    )
    parser.add_argument(
        "--min-mentions",
        type=int,
        default=1,
        help="Export contacts with at least this many mentions.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input path does not exist: {input_path}")

    owner_emails = {
        normalized
        for item in args.owner_email
        for normalized in [normalize_email(item)]
        if normalized
    }
    contacts = process_inputs(
        input_path,
        owner_emails=owner_emails,
        include_owner=args.include_owner,
        scan_body=args.scan_body,
    )
    out_csv = Path(args.out_csv).expanduser().resolve()
    exported_count = write_csv(out_csv, contacts.values(), args.min_mentions)
    out_json = Path(args.out_json).expanduser().resolve()
    write_summary(
        out_json,
        contacts=contacts,
        exported_count=exported_count,
        owner_emails=owner_emails,
        input_path=input_path,
        min_mentions=args.min_mentions,
    )

    print(f"Processed input: {input_path}")
    print(f"Unique contacts found: {len(contacts)}")
    print(f"Contacts exported to CSV: {exported_count}")
    print(f"CSV output: {out_csv}")
    print(f"Summary output: {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
