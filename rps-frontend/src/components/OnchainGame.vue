<script setup>
import { ethers } from 'ethers'
import { computed, ref } from 'vue'

import { ERC20_ABI, RPS_ABI } from '../contracts/abis'
import { formatUnits, shortAddress } from '../lib/format'

const props = defineProps({
  wallet: { type: Object, required: true },
  room: { type: Object, required: true },
})

const contractAddress = ref(import.meta.env.VITE_RPS_CONTRACT_ADDRESS || '')
const gameId = ref('')
const move = ref('1') // 1=Rock,2=Paper,3=Scissors
const statusText = ref('')
const game = ref(null)
const decimals = ref(6)

const isConnected = computed(() => Boolean(props.wallet?.signer && props.wallet?.address))
const wagerAmount = computed(() => BigInt(props.room.wager_amount || 0))

function rpsContract() {
  return new ethers.Contract(contractAddress.value, RPS_ABI, props.wallet.signer)
}

async function tokenContract() {
  const addr = props.room.token_address
  const c = new ethers.Contract(addr, ERC20_ABI, props.wallet.signer)
  const d = await c.decimals()
  decimals.value = Number(d)
  return c
}

function storageKey() {
  return `rps_commit_${contractAddress.value}_${gameId.value}_${props.wallet.address}`
}

async function approveIfNeeded() {
  statusText.value = 'Checking allowance…'
  const token = await tokenContract()
  const allowance = await token.allowance(props.wallet.address, contractAddress.value)
  if (allowance >= wagerAmount.value) {
    statusText.value = 'Allowance OK'
    return
  }
  statusText.value = 'Approving token…'
  const tx = await token.approve(contractAddress.value, wagerAmount.value)
  await tx.wait()
  statusText.value = 'Approved'
}

async function createGame() {
  if (!contractAddress.value) throw new Error('Set contract address')
  await approveIfNeeded()

  const rps = rpsContract()
  statusText.value = 'Creating game…'
  const tx = await rps.createGame(wagerAmount.value)
  const receipt = await tx.wait()

  for (const log of receipt.logs) {
    try {
      const parsed = rps.interface.parseLog(log)
      if (parsed?.name === 'GameCreated') {
        gameId.value = parsed.args.gameId.toString()
      }
    } catch {
      // ignore
    }
  }
  statusText.value = `Game created (id=${gameId.value || '—'})`
  await loadGame()
}

async function joinGame() {
  if (!contractAddress.value) throw new Error('Set contract address')
  if (!gameId.value) throw new Error('Set gameId')
  await approveIfNeeded()

  const rps = rpsContract()
  statusText.value = 'Joining game…'
  const tx = await rps.joinGame(BigInt(gameId.value))
  await tx.wait()
  statusText.value = 'Joined'
  await loadGame()
}

async function commit() {
  if (!gameId.value) throw new Error('Set gameId')
  const rps = rpsContract()

  const salt = ethers.hexlify(ethers.randomBytes(32))
  const commitment = ethers.solidityPackedKeccak256(
    ['uint256', 'address', 'uint8', 'bytes32'],
    [BigInt(gameId.value), props.wallet.address, Number(move.value), salt],
  )

  statusText.value = 'Committing…'
  const tx = await rps.commitMove(BigInt(gameId.value), commitment)
  await tx.wait()

  localStorage.setItem(storageKey(), JSON.stringify({ salt, move: Number(move.value) }))
  statusText.value = 'Committed (saved salt locally for reveal)'
  await loadGame()
}

async function reveal() {
  if (!gameId.value) throw new Error('Set gameId')
  const saved = localStorage.getItem(storageKey())
  if (!saved) throw new Error('No saved commit salt/move for this game')
  const { salt, move: savedMove } = JSON.parse(saved)

  const rps = rpsContract()
  statusText.value = 'Revealing…'
  const tx = await rps.revealMove(BigInt(gameId.value), savedMove, salt)
  await tx.wait()
  statusText.value = 'Revealed'
  await loadGame()
}

async function forceSettle() {
  if (!gameId.value) throw new Error('Set gameId')
  const rps = rpsContract()
  statusText.value = 'Force settling…'
  const tx = await rps.forceSettle(BigInt(gameId.value))
  await tx.wait()
  statusText.value = 'Force settled'
  await loadGame()
}

async function loadGame() {
  if (!contractAddress.value || !gameId.value) return
  const rps = rpsContract()
  const g = await rps.games(BigInt(gameId.value))
  game.value = {
    player1: g.player1,
    player2: g.player2,
    wager: g.wager?.toString?.() ?? String(g.wager),
    state: Number(g.state),
    commitDeadline: Number(g.commitDeadline),
    revealDeadline: Number(g.revealDeadline),
    p1Reveal: Number(g.p1Reveal),
    p2Reveal: Number(g.p2Reveal),
  }
}
</script>

<template>
  <v-alert v-if="!isConnected" type="info" variant="tonal">
    Connect your wallet to interact with the contract.
  </v-alert>

  <div v-else>
    <v-row dense>
      <v-col cols="12">
        <v-text-field v-model="contractAddress" label="RPS contract address" density="compact" />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field v-model="gameId" label="Game ID" density="compact" />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="move"
          density="compact"
          label="Move"
          :items="[
            { title: 'Rock', value: '1' },
            { title: 'Paper', value: '2' },
            { title: 'Scissors', value: '3' },
          ]"
        />
      </v-col>
    </v-row>

    <v-row dense class="mt-2">
      <v-col cols="12" md="6">
        <v-btn block color="primary" :disabled="!contractAddress" @click="createGame">
          Approve + Create (wager {{ formatUnits(room.wager_amount, decimals) }})
        </v-btn>
      </v-col>
      <v-col cols="12" md="6">
        <v-btn block variant="outlined" :disabled="!contractAddress || !gameId" @click="joinGame">
          Approve + Join
        </v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn block variant="tonal" :disabled="!contractAddress || !gameId" @click="commit">Commit</v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn block variant="tonal" :disabled="!contractAddress || !gameId" @click="reveal">Reveal</v-btn>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn block color="warning" variant="tonal" :disabled="!contractAddress || !gameId" @click="forceSettle">
          Force settle
        </v-btn>
      </v-col>
    </v-row>

    <v-btn class="mt-2" variant="text" :disabled="!contractAddress || !gameId" @click="loadGame">Load game state</v-btn>

    <v-alert v-if="statusText" class="mt-3" type="info" variant="tonal">{{ statusText }}</v-alert>

    <v-card v-if="game" class="mt-3" variant="tonal">
      <v-card-text>
        <div><strong>Player1</strong>: {{ shortAddress(game.player1) }}</div>
        <div><strong>Player2</strong>: {{ shortAddress(game.player2) }}</div>
        <div><strong>Wager</strong>: {{ formatUnits(game.wager, decimals) }}</div>
        <div><strong>State</strong>: {{ game.state }} (0=open,1=committed,2=revealed,3=settled)</div>
        <div><strong>Reveals</strong>: p1={{ game.p1Reveal }} p2={{ game.p2Reveal }}</div>
        <div><strong>Commit deadline</strong>: {{ game.commitDeadline }}</div>
        <div><strong>Reveal deadline</strong>: {{ game.revealDeadline }}</div>
      </v-card-text>
    </v-card>
  </div>
</template>

