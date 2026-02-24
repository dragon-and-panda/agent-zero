import { createVuetify } from 'vuetify'
import { mdi } from 'vuetify/iconsets/mdi'

export const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    sets: { mdi },
  },
})

