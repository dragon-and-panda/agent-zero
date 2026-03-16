from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import request as urllib_request


@dataclass
class SendEmailResult:
    success: bool
    provider: str
    provider_message_id: str | None
    sent_at: float | None
    error: str | None = None


class EmailGateway:
    """Thin email sending gateway.

    Providers:
    - log: writes email payload to JSONL outbox and treats as sent.
    - relay: sends JSON payload to configured relay endpoint over HTTPS.
    """

    def __init__(
        self,
        *,
        provider: str,
        from_address: str,
        relay_endpoint: str | None = None,
        relay_bearer_token: str | None = None,
        outbox_path: str = "/workspace/logs/contract_hub/outbox.log",
    ) -> None:
        self._provider = provider.strip().lower()
        self._from = from_address
        self._relay_endpoint = relay_endpoint
        self._relay_token = relay_bearer_token
        self._outbox = Path(outbox_path)
        self._outbox.parent.mkdir(parents=True, exist_ok=True)

    def send(
        self,
        *,
        thread_id: str,
        email_id: str,
        to: list[str],
        cc: list[str],
        subject: str,
        body: str,
    ) -> SendEmailResult:
        if not to:
            return SendEmailResult(
                success=False,
                provider=self._provider,
                provider_message_id=None,
                sent_at=None,
                error="Email requires at least one recipient in 'to'.",
            )

        payload = {
            "thread_id": thread_id,
            "email_id": email_id,
            "from": self._from,
            "to": to,
            "cc": cc,
            "subject": subject,
            "body": body,
        }
        if self._provider == "relay":
            return self._send_via_relay(payload)
        # Default to safe log provider.
        return self._send_via_log(payload)

    def _send_via_log(self, payload: dict[str, Any]) -> SendEmailResult:
        now = time.time()
        provider_message_id = f"log-{uuid.uuid4().hex}"
        row = {
            "ts": now,
            "provider": "log",
            "provider_message_id": provider_message_id,
            "payload": payload,
        }
        with self._outbox.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=True))
            f.write("\n")
        return SendEmailResult(
            success=True,
            provider="log",
            provider_message_id=provider_message_id,
            sent_at=now,
        )

    def _send_via_relay(self, payload: dict[str, Any]) -> SendEmailResult:
        if not self._relay_endpoint:
            return SendEmailResult(
                success=False,
                provider="relay",
                provider_message_id=None,
                sent_at=None,
                error="Relay provider selected but no relay endpoint configured.",
            )
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self._relay_token:
            headers["Authorization"] = f"Bearer {self._relay_token}"
        req = urllib_request.Request(
            self._relay_endpoint,
            data=data,
            method="POST",
            headers=headers,
        )
        try:
            with urllib_request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8") if resp else "{}"
            body = json.loads(raw) if raw else {}
            now = time.time()
            provider_message_id = str(body.get("message_id") or f"relay-{uuid.uuid4().hex}")
            return SendEmailResult(
                success=True,
                provider="relay",
                provider_message_id=provider_message_id,
                sent_at=now,
            )
        except Exception as exc:
            return SendEmailResult(
                success=False,
                provider="relay",
                provider_message_id=None,
                sent_at=None,
                error=str(exc),
            )
