## RPS Wagering Contracts (Polygon / USDC)

This folder contains a Hardhat project for a **commit–reveal Rock-Paper-Scissors** wagering game using an ERC-20 token (USDC on Polygon testnet, or `MockUSDC` for local testing).

### Quick start (local Hardhat)

```bash
cd rps-contracts
npm install
npx hardhat test
```

### Deploy (local node)

Terminal A:

```bash
cd rps-contracts
npx hardhat node
```

Terminal B:

```bash
cd rps-contracts
npx hardhat run scripts/deploy.js --network localhost
```

### Deploy (Polygon Mumbai)

1) Copy `.env.example` to `.env` and set:
- `MUMBAI_RPC_URL`
- `PRIVATE_KEY`
- optional `USDC_TOKEN` (if unset, the deploy script deploys `MockUSDC`)

2) Deploy:

```bash
cd rps-contracts
npx hardhat run scripts/deploy.js --network mumbai
```

### Commit format (frontend/backend)

Commitment hash:

\[
\text{commitment} = keccak256(abi.encodePacked(gameId, playerAddress, uint8(move), salt))
\]

Where `move` is `1=Rock`, `2=Paper`, `3=Scissors` and `salt` is 32 random bytes.

