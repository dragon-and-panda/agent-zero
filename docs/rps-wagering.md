## Rock-Paper-Scissors (USDC) on Polygon — Local + Testnet Runbook

This repo now contains a self-contained MVP in three folders:

- `rps-contracts/`: Hardhat + Solidity (`RockPaperScissors` + `MockUSDC`)
- `rps-backend/`: Django + DRF + Channels (lobby + matchmaking + websocket + 1inch quote/swap-tx proxy)
- `rps-frontend/`: Vue + Vite + Vuetify (wallet connect + lobby + on-chain play)

### 1) Run backend + frontend (Docker)

```bash
docker compose -f docker-compose.rps.yml up
```

- Backend: `http://localhost:8000/api/rooms/`
- Websocket: `ws://localhost:8000/ws/lobby/`
- Frontend: `http://localhost:5173`

### 2) Run contracts locally (Hardhat)

Terminal A:

```bash
cd rps-contracts
npm install
npx hardhat node
```

Terminal B:

```bash
cd rps-contracts
npx hardhat run scripts/deploy.js --network localhost
```

Copy the deployed `RockPaperScissors` address into `rps-frontend/.env` as `VITE_RPS_CONTRACT_ADDRESS`.

### 3) Testnet deploy (Polygon Mumbai)

In `rps-contracts/`:

```bash
cp .env.example .env
```

Set:
- `MUMBAI_RPC_URL`
- `PRIVATE_KEY`
- optional `USDC_TOKEN` (if unset, deploy script deploys `MockUSDC`)

Deploy:

```bash
npx hardhat run scripts/deploy.js --network mumbai
```

### Notes on fairness + fees

- The contract uses **commit–reveal** and includes **commit/reveal deadlines** so a player can’t grief the game indefinitely.
- A **1.5% fee** (configurable, capped) is taken from the pot for settled/forfeit games and tracked in `feesAccrued`.
- If neither player reveals by the deadline, the contract refunds both players (no fee).

