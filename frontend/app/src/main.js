import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import {createVuetify} from 'vuetify'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import {VCalendar} from 'vuetify/labs/VCalendar'

import { isAuthenticated } from './utils/auth'

const vuetify = createVuetify({
    components: {
        ...components,
        VCalendar,
    },
    directives,
})

const app = createApp(App)
app.use(vuetify)
app.use(router)

console.log('Starting app. Authentication status:', isAuthenticated() ? 'Authenticated' : 'Not authenticated')

app.mount('#app')
