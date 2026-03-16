import json
import sqlite3
import threading
import time
from dataclasses import dataclass
from typing import Iterable, List, Optional

from ..schemas import ConsentStatus


@dataclass
class ContactRow:
    owner_id: str
    email: str
    consent_status: str
    suppression_flag: bool
    sources: list[str]
    first_seen_at: float
    last_seen_at: float
    evidence_count: int
    last_source: str | None


_CONSENT_PRIORITY = {
    ConsentStatus.unknown.value: 1,
    ConsentStatus.opted_in.value: 2,
    ConsentStatus.transactional.value: 3,
    ConsentStatus.opted_out.value: 4,
    ConsentStatus.do_not_contact.value: 5,
}


def merge_consent_status(existing: str, incoming: str) -> str:
    existing_p = _CONSENT_PRIORITY.get(existing, 1)
    incoming_p = _CONSENT_PRIORITY.get(incoming, 1)
    return incoming if incoming_p > existing_p else existing


class ContactStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS contacts (
                    owner_id TEXT NOT NULL,
                    email TEXT NOT NULL,
                    consent_status TEXT NOT NULL,
                    suppression_flag INTEGER NOT NULL DEFAULT 0,
                    sources TEXT NOT NULL,
                    first_seen_at REAL NOT NULL,
                    last_seen_at REAL NOT NULL,
                    evidence_count INTEGER NOT NULL DEFAULT 0,
                    last_source TEXT,
                    PRIMARY KEY (owner_id, email)
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_contacts_owner ON contacts(owner_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_contacts_consent ON contacts(consent_status)"
            )
            conn.commit()

    def upsert_contact(
        self,
        owner_id: str,
        email: str,
        source: str,
        consent_status: str,
        suppression_flag: bool,
        seen_at: float | None = None,
    ) -> str:
        ts = seen_at if seen_at is not None else time.time()

        with self._lock:
            with self._connect() as conn:
                existing = conn.execute(
                    """
                    SELECT owner_id, email, consent_status, suppression_flag, sources,
                           first_seen_at, last_seen_at, evidence_count, last_source
                    FROM contacts
                    WHERE owner_id = ? AND email = ?
                    """,
                    (owner_id, email),
                ).fetchone()

                if not existing:
                    conn.execute(
                        """
                        INSERT INTO contacts (
                            owner_id, email, consent_status, suppression_flag, sources,
                            first_seen_at, last_seen_at, evidence_count, last_source
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            owner_id,
                            email,
                            consent_status,
                            int(suppression_flag),
                            json.dumps([source]),
                            ts,
                            ts,
                            1,
                            source,
                        ),
                    )
                    conn.commit()
                    return "inserted"

                merged_consent = merge_consent_status(
                    existing["consent_status"], consent_status
                )
                merged_suppression = bool(existing["suppression_flag"]) or suppression_flag
                existing_sources = set(json.loads(existing["sources"]))
                existing_sources.add(source)

                conn.execute(
                    """
                    UPDATE contacts
                    SET consent_status = ?,
                        suppression_flag = ?,
                        sources = ?,
                        last_seen_at = ?,
                        evidence_count = ?,
                        last_source = ?
                    WHERE owner_id = ? AND email = ?
                    """,
                    (
                        merged_consent,
                        int(merged_suppression),
                        json.dumps(sorted(existing_sources)),
                        max(existing["last_seen_at"], ts),
                        int(existing["evidence_count"]) + 1,
                        source,
                        owner_id,
                        email,
                    ),
                )
                conn.commit()
                return "updated"

    def list_contacts(
        self,
        owner_id: str,
        consent_status: Optional[str] = None,
        suppression_flag: Optional[bool] = None,
        limit: int = 100,
    ) -> List[ContactRow]:
        clauses = ["owner_id = ?"]
        params: list[object] = [owner_id]

        if consent_status:
            clauses.append("consent_status = ?")
            params.append(consent_status)
        if suppression_flag is not None:
            clauses.append("suppression_flag = ?")
            params.append(int(suppression_flag))

        params.append(limit)
        where = " AND ".join(clauses)

        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT owner_id, email, consent_status, suppression_flag, sources,
                       first_seen_at, last_seen_at, evidence_count, last_source
                FROM contacts
                WHERE {where}
                ORDER BY last_seen_at DESC
                LIMIT ?
                """,
                tuple(params),
            ).fetchall()

        return [self._row_to_model(r) for r in rows]

    def get_contacts_by_emails(self, owner_id: str, emails: Iterable[str]) -> List[ContactRow]:
        email_list = sorted(set(emails))
        if not email_list:
            return []

        placeholders = ",".join("?" for _ in email_list)
        params: list[object] = [owner_id, *email_list]
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT owner_id, email, consent_status, suppression_flag, sources,
                       first_seen_at, last_seen_at, evidence_count, last_source
                FROM contacts
                WHERE owner_id = ? AND email IN ({placeholders})
                ORDER BY email ASC
                """,
                tuple(params),
            ).fetchall()
        return [self._row_to_model(r) for r in rows]

    @staticmethod
    def _row_to_model(row: sqlite3.Row) -> ContactRow:
        return ContactRow(
            owner_id=row["owner_id"],
            email=row["email"],
            consent_status=row["consent_status"],
            suppression_flag=bool(row["suppression_flag"]),
            sources=list(json.loads(row["sources"])),
            first_seen_at=float(row["first_seen_at"]),
            last_seen_at=float(row["last_seen_at"]),
            evidence_count=int(row["evidence_count"]),
            last_source=row["last_source"],
        )
