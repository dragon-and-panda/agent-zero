import csv
import io
import time
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from ..schemas import (
    ConsentStatus,
    ContactSource,
    CsvIngestionRequest,
    HeaderIngestionRequest,
    IngestionSummary,
)
from .normalization import normalize_email, split_contact_cell
from .store import ContactStore


@dataclass
class _AddressEvent:
    email: str
    source: str
    consent_status: str
    suppression_flag: bool


def _parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.strip().lower()
    return normalized in {"1", "true", "yes", "y", "on"}


def _parse_consent(value: str | None, default: ConsentStatus) -> ConsentStatus:
    if value is None:
        return default

    token = value.strip().lower().replace(" ", "_").replace("-", "_")
    mapping = {
        "unknown": ConsentStatus.unknown,
        "opted_in": ConsentStatus.opted_in,
        "transactional": ConsentStatus.transactional,
        "opted_out": ConsentStatus.opted_out,
        "do_not_contact": ConsentStatus.do_not_contact,
        "dnc": ConsentStatus.do_not_contact,
        "unsubscribe": ConsentStatus.opted_out,
        "unsubscribed": ConsentStatus.opted_out,
    }
    return mapping.get(token, default)


class ContactIngestionService:
    def __init__(self, store: ContactStore):
        self.store = store

    def ingest_headers(self, payload: HeaderIngestionRequest) -> tuple[IngestionSummary, list[str]]:
        if not payload.owner_consent_asserted:
            raise PermissionError("Owner consent assertion is required for ingestion.")

        processed_items = len(payload.messages)
        raw_events: list[tuple[str, str]] = []
        invalid_addresses = 0

        for message in payload.messages:
            address_groups = [
                (ContactSource.received.value, message.from_addresses),
                (ContactSource.sent.value, message.to_addresses),
                (ContactSource.cc.value, message.cc_addresses),
                (ContactSource.bcc.value, message.bcc_addresses),
            ]
            for source, values in address_groups:
                for raw in values:
                    normalized = normalize_email(raw)
                    if not normalized:
                        invalid_addresses += 1
                        continue
                    raw_events.append((normalized, source))

        events = [
            _AddressEvent(
                email=e,
                source=s,
                consent_status=payload.default_consent_status.value,
                suppression_flag=False,
            )
            for e, s in raw_events
        ]
        return self._persist_events(payload.owner_id, processed_items, events, invalid_addresses)

    def ingest_csv(self, payload: CsvIngestionRequest) -> tuple[IngestionSummary, list[str]]:
        if not payload.owner_consent_asserted:
            raise PermissionError("Owner consent assertion is required for ingestion.")

        reader = csv.DictReader(io.StringIO(payload.csv_content))
        headers = reader.fieldnames or []
        if payload.email_column not in headers:
            raise ValueError(f"CSV missing required email column: {payload.email_column}")

        processed_items = 0
        invalid_addresses = 0
        events: list[_AddressEvent] = []

        for row in reader:
            processed_items += 1
            raw_email_cell = row.get(payload.email_column)
            candidates = split_contact_cell(raw_email_cell)

            consent = _parse_consent(
                row.get(payload.consent_column) if payload.consent_column else None,
                payload.default_consent_status,
            )
            suppression_flag = _parse_bool(
                row.get(payload.suppression_column) if payload.suppression_column else None
            )

            for candidate in candidates:
                normalized = normalize_email(candidate)
                if not normalized:
                    invalid_addresses += 1
                    continue
                events.append(
                    _AddressEvent(
                        email=normalized,
                        source=payload.default_source.value,
                        consent_status=consent.value,
                        suppression_flag=suppression_flag,
                    )
                )

        return self._persist_events(payload.owner_id, processed_items, events, invalid_addresses)

    def _persist_events(
        self,
        owner_id: str,
        processed_items: int,
        events: Iterable[_AddressEvent],
        invalid_addresses: int,
    ) -> tuple[IngestionSummary, list[str]]:
        event_list = list(events)
        unique_emails = {event.email for event in event_list}
        duplicate_addresses = len(event_list) - len(unique_emails)

        inserted = 0
        updated = 0
        now = time.time()
        for event in event_list:
            action = self.store.upsert_contact(
                owner_id=owner_id,
                email=event.email,
                source=event.source,
                consent_status=event.consent_status,
                suppression_flag=event.suppression_flag,
                seen_at=now,
            )
            if action == "inserted":
                inserted += 1
            else:
                updated += 1

        summary = IngestionSummary(
            processed_items=processed_items,
            unique_valid_addresses=len(unique_emails),
            inserted=inserted,
            updated=updated,
            invalid_addresses=invalid_addresses,
            duplicate_addresses=duplicate_addresses,
        )
        return summary, sorted(unique_emails)
