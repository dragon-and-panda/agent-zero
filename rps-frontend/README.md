## RPS Wagering Frontend (Vue + Vite + Vuetify)

### Run locally

```bash
cd rps-frontend
npm install
cp .env.example .env
npm run dev
```

### Env vars

- `VITE_BACKEND_URL`: Django backend URL (default `http://localhost:8000`)
- `VITE_WS_URL`: lobby websocket URL (default `ws://localhost:8000/ws/lobby/`)
- `VITE_RPS_CONTRACT_ADDRESS`: deployed `RockPaperScissors` contract address
- `VITE_USDC_ADDRESS`: token address used for lobby wagers (USDC/mock)
