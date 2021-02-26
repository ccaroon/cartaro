import Vue from 'vue'
import axios from 'axios'

import MarkdownIt from 'markdown-it'
import MDEmoji from 'markdown-it-emoji'

import App from './App'
import router from './router'
// import store from './store'

import Vuetify from 'vuetify'
import('vuetify/dist/vuetify.min.css')
import('@mdi/font/css/materialdesignicons.min.css')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.markdown = Vue.prototype.$markdown = new MarkdownIt().use(MDEmoji)
Vue.config.productionTip = false

Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  vuetify: new Vuetify({}),
  components: { App },
  router,
  // store,
  template: '<App/>'
}).$mount('#app')
