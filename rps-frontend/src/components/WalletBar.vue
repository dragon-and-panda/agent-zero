<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { ethers } from 'ethers'

import { shortAddress } from '../lib/format'

const props = defineProps({
  wallet: { type: Object, required: true },
})

const emit = defineEmits(['update:wallet'])

const requiredChainId = Number(import.meta.env.VITE_CHAIN_ID || 80001)

function updateWallet(patch) {
  emit('update:wallet', { ...props.wallet, ...patch })
}

const isConnected = computed(() => Boolean(props.wallet?.address))
const wrongChain = computed(() => isConnected.value && props.wallet?.chainId && props.wallet.chainId !== requiredChainId)

async function connect() {
  if (!window.ethereum) {
    alert('MetaMask (window.ethereum) not found')
    return
  }

  const provider = new ethers.BrowserProvider(window.ethereum)
  await provider.send('eth_requestAccounts', [])
  const signer = await provider.getSigner()
  const address = await signer.getAddress()
  const network = await provider.getNetwork()

  updateWallet({
    provider,
    signer,
    address,
    chainId: Number(network.chainId),
  })
}

function disconnect() {
  updateWallet({ provider: null, signer: null, address: null, chainId: null })
}

async function switchNetwork() {
  if (!window.ethereum) return
  const chainIdHex = `0x${requiredChainId.toString(16)}`
  await window.ethereum.request({
    method: 'wallet_switchEthereumChain',
    params: [{ chainId: chainIdHex }],
  })
}

function handleAccountsChanged(accounts) {
  if (!accounts?.length) {
    disconnect()
    return
  }
  updateWallet({ address: accounts[0] })
}

function handleChainChanged(chainIdHex) {
  const chainId = Number.parseInt(chainIdHex, 16)
  updateWallet({ chainId })
}

onMounted(() => {
  const eth = window.ethereum
  if (!eth?.on) return
  eth.on('accountsChanged', handleAccountsChanged)
  eth.on('chainChanged', handleChainChanged)
})

onUnmounted(() => {
  const eth = window.ethereum
  if (!eth?.removeListener) return
  eth.removeListener('accountsChanged', handleAccountsChanged)
  eth.removeListener('chainChanged', handleChainChanged)
})
</script>

<template>
  <v-app-bar color="surface" elevation="1">
    <v-app-bar-title>RPS Wagering (Polygon)</v-app-bar-title>
    <v-spacer />

    <template v-if="isConnected">
      <v-chip class="mr-3" variant="tonal">
        {{ shortAddress(wallet.address) }}
      </v-chip>
      <v-chip class="mr-3" variant="tonal">
        Chain {{ wallet.chainId ?? '—' }}
      </v-chip>

      <v-btn v-if="wrongChain" color="warning" variant="flat" class="mr-2" @click="switchNetwork">
        Switch network
      </v-btn>
      <v-btn variant="outlined" @click="disconnect">Disconnect</v-btn>
    </template>
    <template v-else>
      <v-btn color="primary" variant="flat" @click="connect">Connect wallet</v-btn>
    </template>
  </v-app-bar>
</template>

