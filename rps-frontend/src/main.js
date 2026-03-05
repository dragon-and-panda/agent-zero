import { createApp } from 'vue'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import { vuetify } from './plugins/vuetify'

createApp(App).use(vuetify).mount('#app')
