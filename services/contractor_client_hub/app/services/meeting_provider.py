from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass


@dataclass
class MeetingRoom:
    room_url: str


@dataclass
class MeetingJoinToken:
    token: str
    expires_at: float
    room_url: str


class MeetingProvider:
    """Simple room + join token provider.

    This is a backend-issued token model designed to be replaced by a managed
    WebRTC provider later (e.g., LiveKit/Twilio/Daily).
    """

    def __init__(self, room_base_url: str, signing_secret: str, ttl_seconds: int = 3600) -> None:
        self._room_base_url = room_base_url.rstrip("/")
        self._secret = signing_secret.encode("utf-8")
        self._ttl_seconds = max(60, int(ttl_seconds))

    def create_room(self, thread_id: str, meeting_id: str) -> MeetingRoom:
        room_url = f"{self._room_base_url}/room/{thread_id}/{meeting_id}"
        return MeetingRoom(room_url=room_url)

    def issue_join_token(
        self,
        *,
        thread_id: str,
        meeting_id: str,
        participant_id: str,
        participant_role: str,
    ) -> MeetingJoinToken:
        now = int(time.time())
        exp = now + self._ttl_seconds
        payload = {
            "tid": thread_id,
            "mid": meeting_id,
            "pid": participant_id,
            "role": participant_role,
            "iat": now,
            "exp": exp,
        }
        payload_raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        payload_b64 = _b64url(payload_raw)
        sig = hmac.new(self._secret, payload_b64.encode("utf-8"), hashlib.sha256).digest()
        token = f"cch1.{payload_b64}.{_b64url(sig)}"
        room = self.create_room(thread_id=thread_id, meeting_id=meeting_id)
        return MeetingJoinToken(token=token, expires_at=float(exp), room_url=room.room_url)


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")
