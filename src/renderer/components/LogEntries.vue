<template>
  <v-container>
    <AppBar
      v-bind:name="'Log Entries'"
      v-bind:numPages="Math.ceil(totalEntries / perPage)"
      v-bind:refresh="refresh"
      v-bind:buttons="appBarButtons"
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
        :class="utils.rowColor(idx)"
        @click.stop
      >
        <v-list-item-avatar>
          <v-icon>{{ logEntry.icon() }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(logEntry)">
          <v-list-item-title
            :class="
              logEntry.isDeleted()
                ? 'subtitle-1 text-decoration-line-through'
                : 'subtitle-1'
            "
            >{{ logEntry.subject }}</v-list-item-title
          >
          <v-list-item-subtitle>
            {{ logEntry.category }} |
            {{
              logEntry.logged_at
                ? format.formatDate(logEntry.logged_at * 1000)
                : "--"
            }}
            <Tags
              v-bind:tags="logEntry.tags"
              v-bind:color="utils.rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{
            onEdit: (item) => {
              edit(item);
            },
            onArchiveDelete: (event, item) => {
              if (event.startsWith('post-')) {
                refresh();
              }
            },
          }"
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
import Utils from '../lib/Utils'

import LogEntry from '../models/LogEntry'

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
      const self = this

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
      const self = this
      const query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'logged_at:desc'
      }

      if (this.searchText) {
        const parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          query[parts[0].trim()] = parts[1].trim()
        } else {
          query.subject = this.searchText
          query.content = this.searchText
        }
      }

      LogEntry.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalEntries = total
            self.logEntries = items
          },
          onError: (err) => { Notification.error(`LE.Main.load: ${err.toString()}`) }
        }
      })
    },

    view: function (logEntry) {
      this.logEntry = logEntry
      this.showViewer = true
    },

    newEntry: function () {
      const entry = new LogEntry({
        logged_at: Moment().unix()
      })
      this.edit(entry)
    },

    edit: function (logEntry) {
      this.logEntry = logEntry
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeViewer: function () {
      this.showViewer = false
    }
  },

  data () {
    return {
      logEntry: new LogEntry({}),
      logEntries: [],
      page: 1,
      perPage: 15,
      totalEntries: 0,
      showEditor: false,
      showViewer: false,
      constants: Constants,
      format: Format,
      utils: Utils,
      searchText: null,
      appBarButtons: [
        { name: 'New', icon: 'mdi-newspaper-plus', action: this.newEntry }
      ]
    }
  }
}
</script>
