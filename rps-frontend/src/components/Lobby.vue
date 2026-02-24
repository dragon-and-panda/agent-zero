<script setup>
import axios from 'axios'
import { computed, onMounted, onUnmounted, ref } from 'vue'

import { formatUnits } from '../lib/format'
import OnchainGame from './OnchainGame.vue'

const props = defineProps({
  wallet: { type: Object, required: true },
})

const backendUrl = (import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000').replace(/\/$/, '')
const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/lobby/'
const defaultChainId = Number(import.meta.env.VITE_CHAIN_ID || 80001)
const defaultToken = import.meta.env.VITE_USDC_ADDRESS || '0x0000000000000000000000000000000000000000'

const rooms = ref([])
const selectedRoom = ref(null)
const loading = ref(false)
const error = ref(null)

const wagerUsdc = ref('1')
const chainId = ref(defaultChainId)
const tokenAddress = ref(defaultToken)

let ws = null

const isConnected = computed(() => Boolean(props.wallet?.address))

async function fetchRooms() {
  loading.value = true
  error.value = null
  try {
    const resp = await axios.get(`${backendUrl}/api/rooms/`, { params: { status: 'open', chainId: chainId.value, token: tokenAddress.value } })
    rooms.value = resp.data
  } catch (e) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

function upsertRoom(updated) {
  const idx = rooms.value.findIndex((r) => r.id === updated.id)
  if (idx === -1) rooms.value.unshift(updated)
  else rooms.value[idx] = updated
}

function removeRoom(id) {
  rooms.value = rooms.value.filter((r) => r.id !== id)
}

function connectWs() {
  try {
    ws = new WebSocket(wsUrl)
    ws.onmessage = (msg) => {
      const payload = JSON.parse(msg.data)
      if (payload.type === 'rooms.snapshot') {
        rooms.value = payload.rooms || []
        return
      }
      if (payload.type?.startsWith('room.')) {
        const room = payload.room
        if (!room) return
        if (room.status === 'open') upsertRoom(room)
        else removeRoom(room.id)
      }
    }
  } catch {
    // ignore in dev
  }
}

async function matchmake() {
  if (!isConnected.value) return
  const wagerAmount = Math.round(Number(wagerUsdc.value) * 1e6)
  const resp = await axios.post(`${backendUrl}/api/matchmake/`, {
    chain_id: chainId.value,
    token_address: tokenAddress.value,
    wager_amount: wagerAmount,
    player_address: props.wallet.address,
  })

  selectedRoom.value = resp.data.room
}

async function createRoom() {
  if (!isConnected.value) return
  const wagerAmount = Math.round(Number(wagerUsdc.value) * 1e6)
  const resp = await axios.post(`${backendUrl}/api/rooms/`, {
    chain_id: chainId.value,
    token_address: tokenAddress.value,
    wager_amount: wagerAmount,
    player1_address: props.wallet.address,
  })
  selectedRoom.value = resp.data
}

async function joinRoom(roomId) {
  if (!isConnected.value) return
  const resp = await axios.post(`${backendUrl}/api/rooms/${roomId}/join/`, {
    player2_address: props.wallet.address,
  })
  selectedRoom.value = resp.data
}

onMounted(async () => {
  await fetchRooms()
  connectWs()
})

onUnmounted(() => {
  if (ws) ws.close()
  ws = null
})
</script>

<template>
  <v-row>
    <v-col cols="12" md="5">
      <v-card>
        <v-card-title>Lobby</v-card-title>
        <v-card-text>
          <v-alert v-if="!isConnected" type="info" variant="tonal">
            Connect your wallet to create/join rooms.
          </v-alert>
          <v-alert v-else-if="error" type="error" variant="tonal">{{ error }}</v-alert>

          <v-row class="mt-2" dense>
            <v-col cols="12" md="6">
              <v-text-field v-model="wagerUsdc" label="Wager (USDC)" density="compact" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="chainId" label="Chain ID" density="compact" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="tokenAddress" label="Token address" density="compact" />
            </v-col>
          </v-row>

          <v-row dense class="mt-1">
            <v-col cols="6">
              <v-btn block color="primary" :disabled="!isConnected" @click="matchmake">Matchmake</v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn block variant="outlined" :disabled="!isConnected" @click="createRoom">Create room</v-btn>
            </v-col>
          </v-row>

          <v-divider class="my-4" />

          <v-btn variant="text" :loading="loading" @click="fetchRooms">Refresh</v-btn>

          <v-list density="compact">
            <v-list-item v-for="room in rooms" :key="room.id">
              <v-list-item-title>
                {{ formatUnits(room.wager_amount, 6) }} USDC
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ room.player1_address }}
              </v-list-item-subtitle>
              <template #append>
                <v-btn
                  size="small"
                  variant="tonal"
                  :disabled="!isConnected || room.player1_address?.toLowerCase() === wallet.address?.toLowerCase()"
                  @click="joinRoom(room.id)"
                >
                  Join
                </v-btn>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="7">
      <v-card>
        <v-card-title>On-chain game</v-card-title>
        <v-card-text>
          <v-alert v-if="!selectedRoom" type="info" variant="tonal">
            Pick a room (create/match/join) to start the on-chain flow.
          </v-alert>
          <OnchainGame v-else :wallet="wallet" :room="selectedRoom" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

