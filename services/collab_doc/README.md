# Collab Doc (MVP)

This is a minimal realtime collaboration **relay** server used by `webui/collab_doc.html`.

- It does **not** store documents yet (in-memory only, and the CRDT state lives in clients).
- It simply forwards websocket text/binary messages to other peers in the same `{doc_id}` room.

## Run locally (docker-compose)

If you use `docker/run/docker-compose.yml`, a `collab-doc` service is exposed on port `50081`.

Health check:

`http://localhost:50081/health`

Websocket endpoint:

`ws://localhost:50081/ws/<doc_id>`

