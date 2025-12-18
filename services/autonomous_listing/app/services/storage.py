from __future__ import annotations

import json
import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import get_settings


def _now() -> float:
    return time.time()


@dataclass
class StoredListingRow:
    listing_id: str
    owner_id: str | None
    created_at: float
    updated_at: float
    request: dict
    response: dict


@dataclass
class PublishJobRow:
    job_id: str
    listing_id: str
    platform: str
    mode: str  # assisted | autopublish
    status: str  # queued | running | needs_human | posted | failed
    created_at: float
    updated_at: float
    payload: dict
    result: dict


class ListingStore:
    """
    Minimal SQLite persistence for listings + publish jobs.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or get_settings().db_path
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS listings (
                    listing_id TEXT PRIMARY KEY,
                    owner_id TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    request_json TEXT NOT NULL,
                    response_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_listings_owner_id ON listings(owner_id)"
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS publish_jobs (
                    job_id TEXT PRIMARY KEY,
                    listing_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    payload_json TEXT NOT NULL,
                    result_json TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_publish_jobs_listing_id ON publish_jobs(listing_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_publish_jobs_status ON publish_jobs(status)"
            )

    # --- listings ---

    def upsert_listing(
        self,
        *,
        listing_id: str,
        owner_id: str | None,
        request: dict,
        response: dict,
    ) -> None:
        now = _now()
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT listing_id, created_at FROM listings WHERE listing_id = ?",
                (listing_id,),
            ).fetchone()
            created_at = float(existing["created_at"]) if existing else now
            conn.execute(
                """
                INSERT INTO listings(listing_id, owner_id, created_at, updated_at, request_json, response_json)
                VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(listing_id) DO UPDATE SET
                    owner_id=excluded.owner_id,
                    updated_at=excluded.updated_at,
                    request_json=excluded.request_json,
                    response_json=excluded.response_json
                """,
                (
                    listing_id,
                    owner_id,
                    created_at,
                    now,
                    json.dumps(request, ensure_ascii=False),
                    json.dumps(response, ensure_ascii=False),
                ),
            )

    def get_listing(self, listing_id: str) -> Optional[StoredListingRow]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM listings WHERE listing_id = ?",
                (listing_id,),
            ).fetchone()
            if not row:
                return None
            return StoredListingRow(
                listing_id=row["listing_id"],
                owner_id=row["owner_id"],
                created_at=float(row["created_at"]),
                updated_at=float(row["updated_at"]),
                request=json.loads(row["request_json"]),
                response=json.loads(row["response_json"]),
            )

    def list_listings(
        self, *, owner_id: str | None = None, limit: int = 50
    ) -> List[StoredListingRow]:
        limit = max(1, min(200, int(limit)))
        with self._connect() as conn:
            if owner_id:
                rows = conn.execute(
                    "SELECT * FROM listings WHERE owner_id = ? ORDER BY created_at DESC LIMIT ?",
                    (owner_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM listings ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        out: List[StoredListingRow] = []
        for row in rows:
            out.append(
                StoredListingRow(
                    listing_id=row["listing_id"],
                    owner_id=row["owner_id"],
                    created_at=float(row["created_at"]),
                    updated_at=float(row["updated_at"]),
                    request=json.loads(row["request_json"]),
                    response=json.loads(row["response_json"]),
                )
            )
        return out

    # --- publish jobs ---

    def create_publish_jobs(
        self,
        *,
        listing_id: str,
        platform_publication: Dict[str, dict],
        mode_by_platform: Dict[str, str] | None = None,
    ) -> List[PublishJobRow]:
        """
        Create one publish job per platform present in platform_publication.
        Returns created jobs.
        """
        created: List[PublishJobRow] = []
        now = _now()
        with self._connect() as conn:
            for platform, pub in platform_publication.items():
                job_id = str(uuid.uuid4())
                mode = (mode_by_platform or {}).get(platform, "assisted")
                status = "needs_human" if mode == "assisted" else "queued"
                payload = {"platform_publication": pub}
                result = {}
                conn.execute(
                    """
                    INSERT INTO publish_jobs(job_id, listing_id, platform, mode, status, created_at, updated_at, payload_json, result_json)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job_id,
                        listing_id,
                        platform,
                        mode,
                        status,
                        now,
                        now,
                        json.dumps(payload, ensure_ascii=False),
                        json.dumps(result, ensure_ascii=False),
                    ),
                )
                created.append(
                    PublishJobRow(
                        job_id=job_id,
                        listing_id=listing_id,
                        platform=platform,
                        mode=mode,
                        status=status,
                        created_at=now,
                        updated_at=now,
                        payload=payload,
                        result=result,
                    )
                )
        return created

    def list_publish_jobs(
        self,
        *,
        status: str | None = None,
        platform: str | None = None,
        limit: int = 50,
    ) -> List[PublishJobRow]:
        limit = max(1, min(200, int(limit)))
        where = []
        params: list[Any] = []
        if status:
            where.append("status = ?")
            params.append(status)
        if platform:
            where.append("platform = ?")
            params.append(platform)
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        sql = f"SELECT * FROM publish_jobs{where_sql} ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()

        out: List[PublishJobRow] = []
        for row in rows:
            out.append(
                PublishJobRow(
                    job_id=row["job_id"],
                    listing_id=row["listing_id"],
                    platform=row["platform"],
                    mode=row["mode"],
                    status=row["status"],
                    created_at=float(row["created_at"]),
                    updated_at=float(row["updated_at"]),
                    payload=json.loads(row["payload_json"]),
                    result=json.loads(row["result_json"]),
                )
            )
        return out

    def mark_job_posted(
        self,
        *,
        job_id: str,
        posted_url: str | None = None,
        reference_id: str | None = None,
        notes: str | None = None,
    ) -> Optional[PublishJobRow]:
        now = _now()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM publish_jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if not row:
                return None
            result = json.loads(row["result_json"])
            result.update(
                {
                    "posted_url": posted_url,
                    "reference_id": reference_id,
                    "notes": notes,
                    "posted_at": now,
                }
            )
            conn.execute(
                """
                UPDATE publish_jobs
                SET status = ?, updated_at = ?, result_json = ?
                WHERE job_id = ?
                """,
                (
                    "posted",
                    now,
                    json.dumps(result, ensure_ascii=False),
                    job_id,
                ),
            )
            payload = json.loads(row["payload_json"])
            return PublishJobRow(
                job_id=row["job_id"],
                listing_id=row["listing_id"],
                platform=row["platform"],
                mode=row["mode"],
                status="posted",
                created_at=float(row["created_at"]),
                updated_at=now,
                payload=payload,
                result=result,
            )

