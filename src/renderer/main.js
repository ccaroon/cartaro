import Vue from 'vue'
import axios from 'axios'

import MarkdownIt from 'markdown-it'
import MDItEmoji from 'markdown-it-emoji'
import MDItTasks from 'markdown-it-task-lists'
import hljs from 'highlight.js'

import App from './App'
import router from './router'
// import store from './store'

import Vuetify from 'vuetify'
import('vuetify/dist/vuetify.min.css')
import('@mdi/font/css/materialdesignicons.min.css')
import('highlight.js/styles/atom-one-dark.css')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios

const mdItOpts = {
  breaks: true,
  linkify: true,
  typographer: true,
  langPrefix: 'language-',
  highlight: function (str, lang) {
    const prefix = '<pre class="hljs"><code>'
    const suffix = '</code></pre>'
    let block = str
    if (lang && hljs.getLanguage(lang)) {
      try {
        block = hljs.highlight(str, { language: lang, ignoreIllegals: true }).value
      } catch (err) {
        console.log(err)
      }
    }

    return `${prefix}${block}${suffix}`
  }
  // highlight: (str, lang) => {
  //   let block = ''
  //   if (lang && hljs.getLanguage(lang)) {
  //     try {
  //       block = hljs.highlight(str, { language: lang }).value
  //     } catch (err) {
  //       console.log(err)
  //     }
  //   }

  //   return block
  // }
}
Vue.markdown = Vue.prototype.$markdown = new MarkdownIt(mdItOpts)
  .use(MDItEmoji)
  .use(MDItTasks, { enabled: true })

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
