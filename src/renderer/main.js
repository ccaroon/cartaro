import Vue from 'vue'
import axios from 'axios'

import MarkdownIt from 'markdown-it'
import MDItEmoji from 'markdown-it-emoji'
import MDItForInline from 'markdown-it-for-inline'
import MDItTasks from 'markdown-it-task-lists'
import hljs from 'highlight.js'

import App from './App'
import router from './router'

import vuetify from './plugins/vuetify'

import '@fortawesome/fontawesome-free/js/all.js'
import('highlight.js/styles/atom-one-dark.css')

Vue.config.productionTip = false

// import Vuetify from 'vuetify'
// import('vuetify/dist/vuetify.min.css')
// import('@mdi/font/css/materialdesignicons.min.css')
// import('material-design-icons-iconfont/dist/material-design-icons.css')

// if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
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

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
