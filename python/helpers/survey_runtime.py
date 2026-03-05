import asyncio
import json
import os
import re
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from agent import Agent
from python.helpers import dirty_json, files
from python.helpers.memory import Memory

DATA_NAME_SURVEY_RUNTIME = "_survey_runtime"

_SURVEY_RUNTIMES: dict[str, "SurveyRuntime"] = {}
_URL_REGEX = re.compile(r"https?://[^\s\"'<>]+")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_http_url(value: str) -> bool:
    text = (value or "").strip()
    return text.startswith("http://") or text.startswith("https://")


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    found = _URL_REGEX.findall(text)
    seen = set()
    urls: list[str] = []
    for url in found:
        cleaned = url.strip().rstrip(".,);")
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            urls.append(cleaned)
    return urls


def parse_json_like(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    try:
        parsed = dirty_json.DirtyJson.parse_string(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {}


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in patch.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if slug:
        return slug
    return f"persona-{uuid.uuid4().hex[:8]}"


class SurveyDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._lock = threading.RLock()
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_schema()

    def _connect(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None):
        if row is None:
            return None
        return dict(row)

    def _initialize_schema(self):
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS personas (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    instructions TEXT DEFAULT '',
                    traits_json TEXT DEFAULT '{}',
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    profile_json TEXT DEFAULT '{}',
                    summary TEXT DEFAULT '',
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS survey_queue (
                    id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    source TEXT DEFAULT 'manual',
                    metadata_json TEXT DEFAULT '{}',
                    status TEXT DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS survey_sessions (
                    id TEXT PRIMARY KEY,
                    queue_id TEXT,
                    user_id TEXT NOT NULL,
                    persona_id TEXT,
                    survey_url TEXT NOT NULL,
                    source TEXT DEFAULT 'manual',
                    objective TEXT DEFAULT '',
                    status TEXT DEFAULT 'running',
                    summary TEXT DEFAULT '',
                    raw_result_json TEXT DEFAULT '{}',
                    error TEXT DEFAULT '',
                    started_at TEXT NOT NULL,
                    completed_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS survey_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    rationale TEXT DEFAULT '',
                    confidence REAL DEFAULT 0.0,
                    created_at TEXT NOT NULL,
                    optimized_run_id INTEGER
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS optimizer_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    input_response_count INTEGER DEFAULT 0,
                    profile_patch_json TEXT DEFAULT '{}',
                    summary TEXT DEFAULT '',
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_survey_queue_status ON survey_queue(status)"
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_survey_responses_unoptimized
                ON survey_responses(user_id, optimized_run_id)
                """
            )

    def upsert_persona(self, persona: dict[str, Any]) -> dict[str, Any]:
        persona_id = _slugify(
            str(persona.get("id") or persona.get("name") or "survey-persona")
        )
        name = str(persona.get("name") or persona_id)
        description = str(persona.get("description") or "")
        instructions = str(persona.get("instructions") or "")
        traits = persona.get("traits", {})
        if not isinstance(traits, dict):
            traits = {"raw_traits": traits}
        updated_at = utc_now()

        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO personas(id, name, description, instructions, traits_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    description=excluded.description,
                    instructions=excluded.instructions,
                    traits_json=excluded.traits_json,
                    updated_at=excluded.updated_at
                """,
                (
                    persona_id,
                    name,
                    description,
                    instructions,
                    json.dumps(traits),
                    updated_at,
                ),
            )
        return {
            "id": persona_id,
            "name": name,
            "description": description,
            "instructions": instructions,
            "traits": traits,
            "updated_at": updated_at,
        }

    def get_persona(self, persona_id: str) -> dict[str, Any] | None:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM personas WHERE id = ?",
                (persona_id,),
            ).fetchone()
        item = self._row_to_dict(row)
        if not item:
            return None
        item["traits"] = parse_json_like(item.pop("traits_json", "{}"))
        return item

    def list_personas(self, limit: int = 10) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM personas ORDER BY updated_at DESC LIMIT ?",
                (max(limit, 1),),
            ).fetchall()
        out: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["traits"] = parse_json_like(item.pop("traits_json", "{}"))
            out.append(item)
        return out

    def get_profile(self, user_id: str) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT profile_json FROM user_profiles WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        if not row:
            return {}
        return parse_json_like(str(row["profile_json"]))

    def upsert_profile(self, user_id: str, profile: dict[str, Any], summary: str = ""):
        updated_at = utc_now()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_profiles(user_id, profile_json, summary, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    profile_json=excluded.profile_json,
                    summary=excluded.summary,
                    updated_at=excluded.updated_at
                """,
                (user_id, json.dumps(profile), summary, updated_at),
            )

    def enqueue_survey(
        self, url: str, source: str = "manual", metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        now = utc_now()
        qid = str(uuid.uuid4())
        payload = metadata or {}
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO survey_queue(id, url, source, metadata_json, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'pending', ?, ?)
                """,
                (qid, url, source, json.dumps(payload), now, now),
            )
        return {
            "id": qid,
            "url": url,
            "source": source,
            "metadata": payload,
            "status": "pending",
            "created_at": now,
            "updated_at": now,
        }

    def claim_next_survey(self) -> dict[str, Any] | None:
        with self._lock, self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                """
                SELECT * FROM survey_queue
                WHERE status = 'pending'
                ORDER BY created_at ASC
                LIMIT 1
                """
            ).fetchone()
            if not row:
                conn.commit()
                return None
            now = utc_now()
            conn.execute(
                "UPDATE survey_queue SET status='claimed', updated_at=? WHERE id=?",
                (now, row["id"]),
            )
            conn.commit()
            item = dict(row)
            item["status"] = "claimed"
            item["updated_at"] = now
            item["metadata"] = parse_json_like(item.pop("metadata_json", "{}"))
            return item

    def update_queue_status(self, queue_id: str, status: str):
        with self._lock, self._connect() as conn:
            conn.execute(
                "UPDATE survey_queue SET status=?, updated_at=? WHERE id=?",
                (status, utc_now(), queue_id),
            )

    def create_session(
        self,
        session_id: str,
        user_id: str,
        survey_url: str,
        source: str,
        objective: str,
        persona_id: str | None = None,
        queue_id: str | None = None,
    ):
        now = utc_now()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO survey_sessions(
                    id, queue_id, user_id, persona_id, survey_url, source, objective,
                    status, started_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'running', ?)
                """,
                (
                    session_id,
                    queue_id,
                    user_id,
                    persona_id,
                    survey_url,
                    source,
                    objective,
                    now,
                ),
            )

    def complete_session(
        self,
        session_id: str,
        status: str,
        summary: str,
        raw_result: dict[str, Any] | None = None,
    ):
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE survey_sessions
                SET status=?, summary=?, raw_result_json=?, completed_at=?
                WHERE id=?
                """,
                (
                    status,
                    summary,
                    json.dumps(raw_result or {}),
                    utc_now(),
                    session_id,
                ),
            )

    def fail_session(self, session_id: str, error: str):
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE survey_sessions
                SET status='failed', error=?, completed_at=?
                WHERE id=?
                """,
                (error, utc_now(), session_id),
            )

    def add_survey_responses(
        self, session_id: str, user_id: str, responses: list[dict[str, Any]]
    ):
        if not responses:
            return

        rows = []
        now = utc_now()
        for response in responses:
            question = str(response.get("question", "")).strip()
            answer = str(response.get("answer", "")).strip()
            if not question or not answer:
                continue
            rationale = str(response.get("rationale", "")).strip()
            confidence_raw = response.get("confidence", 0.0)
            try:
                confidence = float(confidence_raw)
            except Exception:
                confidence = 0.0
            confidence = max(0.0, min(1.0, confidence))
            rows.append((session_id, user_id, question, answer, rationale, confidence, now))

        if not rows:
            return

        with self._lock, self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO survey_responses(
                    session_id, user_id, question, answer, rationale, confidence, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def get_unoptimized_responses(
        self, user_id: str, limit: int = 25
    ) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, question, answer, rationale, confidence, created_at
                FROM survey_responses
                WHERE user_id = ? AND optimized_run_id IS NULL
                ORDER BY id ASC
                LIMIT ?
                """,
                (user_id, max(limit, 1)),
            ).fetchall()
        return [dict(row) for row in rows]

    def record_optimizer_run(
        self,
        user_id: str,
        input_response_count: int,
        profile_patch: dict[str, Any],
        summary: str,
    ) -> int:
        with self._lock, self._connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO optimizer_runs(user_id, input_response_count, profile_patch_json, summary, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    input_response_count,
                    json.dumps(profile_patch),
                    summary,
                    utc_now(),
                ),
            )
            return int(cur.lastrowid)

    def mark_responses_optimized(self, response_ids: list[int], run_id: int):
        if not response_ids:
            return
        placeholders = ",".join(["?"] * len(response_ids))
        with self._lock, self._connect() as conn:
            conn.execute(
                f"""
                UPDATE survey_responses
                SET optimized_run_id = ?
                WHERE id IN ({placeholders})
                """,
                (run_id, *response_ids),
            )

    def get_status_summary(self, user_id: str) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            persona_count = conn.execute("SELECT COUNT(*) AS c FROM personas").fetchone()["c"]
            queue_counts = conn.execute(
                """
                SELECT status, COUNT(*) AS c
                FROM survey_queue
                GROUP BY status
                """
            ).fetchall()
            session_counts = conn.execute(
                """
                SELECT status, COUNT(*) AS c
                FROM survey_sessions
                WHERE user_id = ?
                GROUP BY status
                """,
                (user_id,),
            ).fetchall()
            unoptimized = conn.execute(
                """
                SELECT COUNT(*) AS c
                FROM survey_responses
                WHERE user_id = ? AND optimized_run_id IS NULL
                """,
                (user_id,),
            ).fetchone()["c"]

        return {
            "persona_count": int(persona_count),
            "queue": {str(row["status"]): int(row["c"]) for row in queue_counts},
            "sessions": {str(row["status"]): int(row["c"]) for row in session_counts},
            "unoptimized_responses": int(unoptimized),
            "db_path": self.db_path,
        }


class LocalSurveyChatbot:
    def __init__(self, db: SurveyDatabase):
        self.db = db

    def _normalize_persona(self, candidate: dict[str, Any], fallback: str) -> dict[str, Any]:
        persona_name = str(candidate.get("name") or fallback or "Default Survey Persona")
        persona_id = _slugify(str(candidate.get("id") or persona_name))
        description = str(candidate.get("description") or "")
        instructions = str(candidate.get("instructions") or "")
        traits = candidate.get("traits", {})
        if not isinstance(traits, dict):
            traits = {"raw_traits": traits}
        return {
            "id": persona_id,
            "name": persona_name,
            "description": description,
            "instructions": instructions,
            "traits": traits,
        }

    async def refine_persona(
        self,
        agent: Agent,
        user_id: str,
        objective: str = "",
        requested_persona: str = "",
        persona_id: str = "",
        background: bool = False,
    ) -> dict[str, Any]:
        if persona_id:
            existing = self.db.get_persona(persona_id)
            if existing and not requested_persona.strip():
                return existing

        profile = self.db.get_profile(user_id)
        known_personas = self.db.list_personas(limit=8)

        system = """
You are a local persona chatbot for a survey-filling agent.
Create or refine a persona that can be used to answer surveys consistently.
Return JSON only with fields:
{
  "id": "persona-id",
  "name": "Persona name",
  "description": "short profile",
  "instructions": "direct behavioral instructions for survey answering",
  "traits": {"age_range":"", "tone":"", "preferences":[]}
}
Keep instructions concise and practical.
"""
        message = json.dumps(
            {
                "requested_persona": requested_persona,
                "objective": objective,
                "existing_profile": profile,
                "known_personas": known_personas,
            }
        )

        raw = await agent.call_utility_model(
            system=system, message=message, background=background
        )
        candidate = parse_json_like(raw)
        normalized = self._normalize_persona(
            candidate=candidate,
            fallback=requested_persona or "Adaptive Survey Persona",
        )
        return self.db.upsert_persona(normalized)

    async def optimize_profile(
        self,
        agent: Agent,
        user_id: str,
        min_responses: int = 4,
        batch_size: int = 25,
        background: bool = True,
    ) -> dict[str, Any] | None:
        responses = self.db.get_unoptimized_responses(user_id=user_id, limit=batch_size)
        if len(responses) < min_responses:
            return None

        current_profile = self.db.get_profile(user_id=user_id)
        system = """
You are a local profile optimizer chatbot for survey automation.
Infer stable user profile traits from recent survey responses.
Return JSON only:
{
  "profile_patch": {"demographics":{}, "preferences":{}, "behavior":{}},
  "summary": "short explanation"
}
Never remove keys from existing profile. Provide only additive or corrective updates.
"""
        message = json.dumps(
            {
                "current_profile": current_profile,
                "recent_responses": responses,
            }
        )
        raw = await agent.call_utility_model(
            system=system, message=message, background=background
        )
        parsed = parse_json_like(raw)
        patch = parsed.get("profile_patch", {})
        if not isinstance(patch, dict):
            patch = {}
        summary = str(parsed.get("summary", "Profile optimized from survey responses."))

        merged_profile = deep_merge(current_profile, patch)
        self.db.upsert_profile(user_id=user_id, profile=merged_profile, summary=summary)

        run_id = self.db.record_optimizer_run(
            user_id=user_id,
            input_response_count=len(responses),
            profile_patch=patch,
            summary=summary,
        )
        response_ids = [int(item["id"]) for item in responses]
        self.db.mark_responses_optimized(response_ids=response_ids, run_id=run_id)

        return {
            "run_id": run_id,
            "response_count": len(responses),
            "summary": summary,
            "profile": merged_profile,
            "patch": patch,
        }


class SurveyRuntime:
    def __init__(self, db: SurveyDatabase):
        self.db = db
        self.chatbot = LocalSurveyChatbot(db)
        self._active_surveys = 0
        self._background_task: asyncio.Task | None = None
        self._optimizer_lock = asyncio.Lock()
        self._last_optimizer_run = 0.0
        self.background_cooldown_seconds = 120.0
        self.last_optimizer_result: dict[str, Any] | None = None

    def mark_survey_active(self):
        self._active_surveys += 1

    def mark_survey_inactive(self):
        self._active_surveys = max(0, self._active_surveys - 1)

    def is_busy(self) -> bool:
        return self._active_surveys > 0

    async def _run_optimizer(
        self,
        agent: Agent,
        user_id: str,
        force: bool = False,
        background: bool = True,
    ) -> dict[str, Any] | None:
        async with self._optimizer_lock:
            if self.is_busy() and not force:
                return None
            self._last_optimizer_run = time.time()
            result = await self.chatbot.optimize_profile(
                agent=agent,
                user_id=user_id,
                background=background,
            )
            self.last_optimizer_result = result
            return result

    def _consume_background_result(self, task: asyncio.Task):
        try:
            task.result()
        except Exception:
            # background optimization is best-effort and should not break message loop
            pass

    def maybe_start_background_optimizer(self, agent: Agent, user_id: str = "default") -> bool:
        if self.is_busy():
            return False
        if self._background_task and not self._background_task.done():
            return False
        now = time.time()
        if (now - self._last_optimizer_run) < self.background_cooldown_seconds:
            return False

        self._background_task = asyncio.create_task(
            self._run_optimizer(
                agent=agent,
                user_id=user_id,
                force=False,
                background=True,
            )
        )
        self._background_task.add_done_callback(self._consume_background_result)
        return True

    async def run_optimizer_now(
        self, agent: Agent, user_id: str = "default", force: bool = True
    ) -> dict[str, Any] | None:
        if self._background_task and not self._background_task.done():
            await self._background_task
        return await self._run_optimizer(
            agent=agent,
            user_id=user_id,
            force=force,
            background=False,
        )


def get_survey_runtime(agent: Agent) -> SurveyRuntime:
    runtime = agent.get_data(DATA_NAME_SURVEY_RUNTIME)
    if isinstance(runtime, SurveyRuntime):
        return runtime

    key = agent.context.id
    existing = _SURVEY_RUNTIMES.get(key)
    if existing:
        agent.set_data(DATA_NAME_SURVEY_RUNTIME, existing)
        return existing

    memory_subdir = agent.config.memory_subdir or "default"
    db_path = files.get_abs_path("memory", memory_subdir, "survey_agent", "survey_agent.db")
    created = SurveyRuntime(db=SurveyDatabase(db_path=db_path))
    _SURVEY_RUNTIMES[key] = created
    agent.set_data(DATA_NAME_SURVEY_RUNTIME, created)
    return created


async def discover_urls_with_rag(
    agent: Agent, query: str, limit: int = 5
) -> list[str]:
    if not query.strip():
        return []

    try:
        db = await Memory.get(agent)
        docs = await db.search_similarity_threshold(
            query=query,
            limit=max(limit, 1),
            threshold=0.15,
        )
    except Exception:
        return []

    urls: list[str] = []
    seen = set()
    for doc in docs:
        chunks = [doc.page_content, json.dumps(doc.metadata)]
        for chunk in chunks:
            for url in extract_urls(str(chunk)):
                if url not in seen:
                    seen.add(url)
                    urls.append(url)
                if len(urls) >= limit:
                    return urls
    return urls
