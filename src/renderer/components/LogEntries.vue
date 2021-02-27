<template>
  <v-container>
    <AppBar
      v-bind:name="'Log Entries'"
      v-bind:numPages="Math.ceil(totalEntries / perPage)"
      v-bind:newItem="newEntry"
      v-bind:newIcon="'mdi-newspaper-plus'"
      v-bind:refresh="refresh"
    ></AppBar>
    <LogEntryEditor
      v-model="showEditor"
      v-bind:logEntry="logEntry"
      v-on:close="closeEditor"
    ></LogEntryEditor>
    <LogEntryViewer
      v-model="showViewer"
      v-bind:logEntry="logEntry"
      v-on:close="closeViewer"
    ></LogEntryViewer>
    <v-list dense>
      <v-list-item
        v-for="(logEntry, idx) in logEntries"
        :key="logEntry.id"
        :class="rowColor(idx)"
        @click
      >
        <v-list-item-avatar>
          <v-icon
            >mdi-{{
              constants.ICONS.logEntries[logEntry.category.toLowerCase()]
            }}</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-content @click="view(logEntry)">
          <v-list-item-title
            class="subtitle-1"
            v-if="logEntry.deleted_at === null"
            >{{ logEntry.subject }}</v-list-item-title
          >
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ logEntry.subject }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ logEntry.category }} |
            {{
              logEntry.logged_at
                ? format.formatDate(logEntry.logged_at * 1000)
                : "--"
            }}
            <Tags
              v-bind:tags="logEntry.tags"
              v-bind:color="rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{ edit: edit, remove: remove }"
          v-bind:item="logEntry"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import LogEntryEditor from './LogEntries/Editor'
import LogEntryViewer from './LogEntries/Viewer'
import Notification from '../lib/Notification'
import Tags from './Shared/Tags'

export default {
  name: 'logEntries-main',
  components: { Actions, AppBar, LogEntryEditor, LogEntryViewer, Tags },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newEntry()
        return false
      })
    },

    refresh: function (page = null, searchText = '') {
      if (page !== null) {
        this.page = page
      }

      if (searchText !== '') {
        this.searchText = searchText
      }

      this.load()
    },

    load: function () {
      var self = this
      var qs = `page=${this.page}&pp=${this.perPage}&sort_by=logged_at:desc`

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          qs += `&${parts[0].trim()}=${parts[1].trim()}`
        } else {
          qs += `&subject=${this.searchText}&content=${this.searchText}`
        }
      }

      this.$http.get(`http://127.0.0.1:4242/log_entries/?${qs}`)
        .then(resp => {
          self.totalEntries = resp.data.total
          self.logEntries = resp.data.log_entries
        })
        .catch(err => {
          Notification.error(err.toString())
        })
    },

    view: function (logEntry) {
      this.logEntry = logEntry
      this.showViewer = true
    },

    newEntry: function () {
      this.edit({
        logged_at: Moment().unix()
      })
    },

    edit: function (logEntry) {
      this.logEntry = logEntry
      this.showEditor = true
    },

    remove: function (logEntry) {
      var self = this
      var safe = 1
      var msg = `Safe Delete "${logEntry.subject}"?`

      if (logEntry.deleted_at) {
        safe = 0
        msg = `Delete "${logEntry.subject}"?`
      }

      var doDelete = confirm(msg)
      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/log_entries/${logEntry.id}?safe=${safe}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            Notification.error(err.toString())
          })
      }
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeViewer: function () {
      this.showViewer = false
    },

    rowColor: function (idx) {
      var color = Constants.COLORS.GREY

      if (idx % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
      }
      return color
    }
  },

  data () {
    return {
      logEntry: {},
      logEntries: [],
      page: 1,
      perPage: 15,
      totalEntries: 0,
      showEditor: false,
      showViewer: false,
      constants: Constants,
      format: Format,
      searchText: null
    }
  }
}
</script>
