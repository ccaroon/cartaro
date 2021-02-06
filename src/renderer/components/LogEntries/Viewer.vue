<template>
  <v-dialog v-model="value" persistent scrollable max-width="75%">
    <v-card>
      <v-card-title>
        {{ logEntry.subject }}
        <v-spacer></v-spacer>
        <v-chip
          small
          label
          class="mr-1"
          v-for="(tag, idx) in logEntry.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
      </v-card-title>
      <v-card-subtitle>
        <template v-if="logEntry.category === 'Ticket'">
          <span
            style="cursor: pointer"
            class="blue--text"
            @click="openLink(logEntry.ticket_link)"
          >
            {{ logEntry.category }}
            <v-icon x-small color="blue">mdi-open-in-new</v-icon>
          </span>
        </template>
        <template v-else>{{ logEntry.category }}</template>
        |
        {{
          logEntry.logged_at
            ? format.formatDate(logEntry.logged_at * 1000)
            : "--"
        }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text
        v-html="md.render(logEntry.content || '')"
        class="body-1 pt-3"
        style="height: 500px"
      ></v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import MarkdownIt from 'markdown-it'
import MDEmoji from 'markdown-it-emoji'

import Format from '../../lib/Format'

const { BrowserWindow } = require('electron').remote

export default {
  name: 'logEntry-viewer',
  components: {},
  props: ['logEntry', 'value'],

  methods: {
    // openLink: function (url) {
    //   const win = BrowserWindow.getFocusedWindow()
    //   const view = new BrowserView()
    //   win.setBrowserView(view)
    //   view.setBounds({ x: 0, y: 0, width: 300, height: 300 })
    //   view.webContents.loadURL('https://electronjs.org')
    // },
    openLink: function (url) {
      const main = BrowserWindow.getFocusedWindow()
      const child = new BrowserWindow({
        parent: main,
        modal: true,
        title: 'Jira',
        fullscreenable: false,
        webPreferences: {
          devTools: false
        },
        autoHideMenuBar: true,
        width: 1200,
        height: 900
      })

      child.loadURL(url)
      // child.once('ready-to-show', () => {
      //   child.show()
      // })
    },

    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return {
      // TODO: move to Vue instance like $http
      md: new MarkdownIt().use(MDEmoji),
      format: Format
    }
  }
}
</script>
