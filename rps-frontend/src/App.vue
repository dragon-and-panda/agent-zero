<template>
  <v-app>
    <WalletBar v-model:wallet="wallet" />
    <v-main>
      <v-container class="py-6">
        <Lobby :wallet="wallet" />
      </v-container>
    </v-main>
  </v-app>
</template>
<script setup>
import { ref } from 'vue'
import Lobby from './components/Lobby.vue'
import WalletBar from './components/WalletBar.vue'

const wallet = ref({
  address: null,
  chainId: null,
  provider: null,
  signer: null,
})
</script>
