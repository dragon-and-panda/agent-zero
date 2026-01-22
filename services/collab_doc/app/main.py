from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


@dataclass(frozen=True)
class Client:
    websocket: WebSocket


app = FastAPI(title="Collab Doc Relay", version="0.1.0")

# For browser-based clients hosted on a different port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# doc_id -> set of connected clients
_rooms: DefaultDict[str, Set[Client]] = defaultdict(set)
_locks: DefaultDict[str, asyncio.Lock] = defaultdict(asyncio.Lock)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"ok": "true"}


async def _broadcast(doc_id: str, sender: Client, message: str | bytes) -> None:
    # Snapshot recipients under lock, then send without holding lock.
    async with _locks[doc_id]:
        recipients = [c for c in _rooms[doc_id] if c != sender]

    # Best-effort fanout: a failed client doesn't block others.
    for c in recipients:
        try:
            if isinstance(message, bytes):
                await c.websocket.send_bytes(message)
            else:
                await c.websocket.send_text(message)
        except Exception:
            # Ignore send errors; disconnect handling will clean up eventually.
            pass


@app.websocket("/ws/{doc_id}")
async def ws_doc(doc_id: str, websocket: WebSocket) -> None:
    await websocket.accept()
    client = Client(websocket=websocket)

    async with _locks[doc_id]:
        _rooms[doc_id].add(client)

    try:
        while True:
            msg = await websocket.receive()
            if msg.get("bytes") is not None:
                await _broadcast(doc_id, client, msg["bytes"])
            elif msg.get("text") is not None:
                await _broadcast(doc_id, client, msg["text"])
            else:
                # Ignore ping/pong or other frames we don't care about.
                pass
    except WebSocketDisconnect:
        pass
    finally:
        async with _locks[doc_id]:
            _rooms[doc_id].discard(client)
            if not _rooms[doc_id]:
                # Cleanup empty rooms to avoid unbounded growth.
                _rooms.pop(doc_id, None)
                _locks.pop(doc_id, None)

