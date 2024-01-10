import Vue from 'vue'
import axios from 'axios'

import MarkdownIt from 'markdown-it'
import { full as MDItEmoji } from 'markdown-it-emoji'
import MDItForInline from 'markdown-it-for-inline'
import MDItTasks from 'markdown-it-task-lists'
import hljs from 'highlight.js'

import App from './App'
import router from './router'

import vuetify from './plugins/vuetify'

import '@fortawesome/fontawesome-free/js/all.js'
import Config from '@/shared/Config'
import RestClient from './lib/RestClient'
import crypto from './lib/crypto'
import('highlight.js/styles/panda-syntax-dark.css')

Vue.config.productionTip = false

Vue.http = Vue.prototype.$http = axios

const mdItOpts = {
  breaks: true,
  linkify: true,
  typographer: true,
  langPrefix: 'language-',
  highlight: function (str, lang) {
    const prefix = '<pre class="hljs">'
    const suffix = '</pre>'
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
}

Vue.markdown = Vue.prototype.$markdown = new MarkdownIt(mdItOpts)
  .use(MDItEmoji)
  .use(MDItTasks, { enabled: true })
  // Add `target=_blank` to a hrefs
  .use(MDItForInline, 'url_new_win', 'link_open', function (tokens, idx) {
    const aIndex = tokens[idx].attrIndex('target')

    if (aIndex < 0) {
      tokens[idx].attrPush(['target', '_blank'])
    } else {
      tokens[idx].attrs[aIndex][1] = '_blank'
    }
  })

Vue.config.productionTip = false

async function loadConfig () {
  const configData = await window.Config.data()
  const config = new Config(configData)

  crypto.init(config.get('encryption_password'))
  RestClient.init(config.get('server:port'))

  global.Cartaro = {
    config
  }
}

loadConfig().then(() => {
  new Vue({
    router,
    vuetify,
    render: h => h(App)
  }).$mount('#app')
})
