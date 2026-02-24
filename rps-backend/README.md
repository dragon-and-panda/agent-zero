## RPS Wagering Backend (Django + DRF + Channels)

### What’s in here

- REST API for lobby rooms (create/list/join) + **matchmaking by wager (±10%)**
- Websocket lobby feed (`/ws/lobby/`) for real-time room updates
- 1inch Classic Swap API proxy endpoints:
  - `GET /api/swap/1inch/quote/`
  - `GET /api/swap/1inch/swap-tx/` (returns calldata; client signs/broadcasts)

### Local run

1) Start Redis:

```bash
docker run --rm -p 6379:6379 redis:7-alpine
```

2) Install deps + migrate:

```bash
cd rps-backend
python3 -m pip install -r requirements.txt
python3 manage.py migrate
```

3) Run server (ASGI):

```bash
cd rps-backend
python3 -m daphne -b 0.0.0.0 -p 8000 rps_backend.asgi:application
```

### API quick test

Create/match a room:

```bash
curl -s -X POST "http://localhost:8000/api/matchmake/" \
  -H "Content-Type: application/json" \
  -d '{"chain_id":80001,"token_address":"0x0000000000000000000000000000000000000000","wager_amount":1000000,"player_address":"0x0000000000000000000000000000000000000001"}'
```

