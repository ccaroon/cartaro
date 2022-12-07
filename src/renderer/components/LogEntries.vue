<template>
  <v-container :fluid="activeView === 'calendar'">
    <AppBar
      v-bind:name="'Log Entries'"
      v-bind:numPages="Math.ceil(totalEntries / perPage)"
      v-bind:buttons="appBarButtons"
      @refresh="refresh"
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
    <LogEntryList
      v-show="activeView === 'list'"
      v-bind:logEntries="logEntries"
      @edit="edit"
      @view="view"
      @refresh="refresh"
    ></LogEntryList>
    <LogEntryCalendar
      v-show="activeView === 'calendar'"
      v-bind:logEntries="logEntries"
      @edit="edit"
      @view="view"
      @new="newEntry"
      @refresh="refresh"
    ></LogEntryCalendar>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import notification from '../lib/notification'

import LogEntry from '../models/LogEntry'

import AppBar from './Shared/AppBar'
import LogEntryList from './LogEntries/List'
import LogEntryCalendar from './LogEntries/Calendar'
import LogEntryEditor from './LogEntries/Editor'
import LogEntryViewer from './LogEntries/Viewer'

const VIEW_LIST = 'list'
const VIEW_CAL = 'calendar'

export default {
  name: 'log-entries-main',
  components: { AppBar, LogEntryCalendar, LogEntryList, LogEntryEditor, LogEntryViewer },
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

    toggleView: function () {
      if (this.activeView === VIEW_LIST) {
        this.activeView = VIEW_CAL
      } else if (this.activeView === VIEW_CAL) {
        this.activeView = VIEW_LIST
      }
    },

    refresh: function (opts = {}) {
      if (opts.page) {
        this.page = opts.page
      }

      if (opts.searchText !== '') {
        this.searchText = opts.searchText
      }

      if (opts.calDate) {
        this.calDate = opts.calDate
      }

      this.load()
    },

    loadQuery: function () {
      let date = Moment()
      let query = null

      if (this.calDate) {
        date = Moment(this.calDate)
      }

      switch (this.activeView) {
        case VIEW_LIST:
          query = {
            page: this.page,
            pp: this.perPage,
            sort_by: 'logged_at:desc'
          }
          break
        case VIEW_CAL:
          query = {
            page: 1,
            pp: 999,
            logged_at: `btw:${date.startOf('month').unix()}:${date.endOf('month').unix()}`,
            sort_by: 'logged_at'
          }
          break
      }

      return query
    },

    load: function () {
      const self = this
      const query = this.loadQuery()

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
          onError: (err) => { notification.error(`LE.Main.load: ${err.toString()}`) }
        }
      })
    },

    view: function (logEntry) {
      this.logEntry = logEntry
      this.showViewer = true
    },

    newEntry: function (logDate = Moment().unix()) {
      const entry = new LogEntry({
        logged_at: logDate
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

  watch: {
    activeView: function () {
      this.refresh()
    }
  },

  data () {
    const itemHeight = 65

    return {
      logEntry: new LogEntry({}),
      logEntries: [],
      page: 1,
      perPage: Math.round(window.innerHeight / itemHeight) - 1,
      calDate: null,
      totalEntries: 0,
      activeView: VIEW_CAL,
      showEditor: false,
      showViewer: false,
      searchText: null,
      appBarButtons: [
        { name: 'New', icon: 'mdi-newspaper-plus', action: this.newEntry },
        { name: 'ToggleView', icon: 'mdi-view-dashboard', action: this.toggleView }
      ]
    }
  }
}
</script>
