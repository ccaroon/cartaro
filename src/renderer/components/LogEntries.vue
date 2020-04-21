<template>
  <v-container>
    <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - Log Entries</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-row no-gutters align="center">
        <v-col cols="1">
          <v-toolbar-items>
            <v-btn icon @click.stop="newEntry()">
              <v-icon>mdi-file-document</v-icon>
            </v-btn>
          </v-toolbar-items>
        </v-col>
        <v-col cols="8">
          <v-toolbar-items>
            <v-pagination
              v-model="page"
              :length="Math.ceil(totalEntries/perPage)"
              total-visible="10"
              @input="load"
            ></v-pagination>
          </v-toolbar-items>
        </v-col>
        <v-col>
          <v-toolbar-items>
            <v-text-field
              ref="searchBox"
              v-model="searchText"
              dense
              clearable
              placeholder="Search..."
              prepend-inner-icon="mdi-magnify"
              @click:clear="clearSearch"
              @keyup.enter="search()"
              @keyup.esc="clearSearch()"
            ></v-text-field>
          </v-toolbar-items>
        </v-col>
      </v-row>
    </v-app-bar>
    <LogEntryEditor v-model="showEditor" v-bind:logEntry="logEntry" v-on:close="closeEditor"></LogEntryEditor>
    <LogEntryViewer v-model="showViewer" v-bind:logEntry="logEntry" v-on:close="closeViewer"></LogEntryViewer>
    <v-list dense>
      <v-list-item
        v-for="(logEntry,idx) in logEntries"
        :key="logEntry.id"
        :class="rowColor(idx)"
        @click
      >
        <v-list-item-content @click="view(logEntry)">
          <v-list-item-title
            class="subtitle-1"
            v-if="logEntry.deleted_at === null"
          >{{ logEntry.subject }}</v-list-item-title>
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ logEntry.subject }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ logEntry.category }} | {{ logEntry.logged_at ? format.formatDate(logEntry.logged_at*1000) : '--'}}
            <v-chip
              x-small
              label
              class="mr-1 float-right"
              :color="rowColor(idx+1)"
              v-for="(tag,tgIdx) in logEntry.tags"
              :key="tgIdx"
            >{{ tag }}</v-chip>
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon outlined @click="edit(logEntry)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-item-action>
        <v-list-item-action>
          <v-btn icon outlined @click="remove(logEntry)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'

import LogEntryEditor from './LogEntries/Editor'
import LogEntryViewer from './LogEntries/Viewer'

export default {
  name: 'logEntries-main',
  components: { LogEntryEditor, LogEntryViewer },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.edit({})
        return false
      })

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })
    },

    load: function () {
      var self = this
      var qs = `page=${self.page}&pp=${self.perPage}`

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
          console.log(`${err.response.status} - ${err.response.data.error}`)
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

      var doDelete = confirm(`Delete "${logEntry.subject}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/log_entries/${logEntry.id}?safe=1`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    closeEditor: function () {
      this.showEditor = false
      this.load()
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
    },

    search: function () {
      if (this.searchText) {
        this.page = 1
        this.load()
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.page = 1
        this.searchText = null
        this.load()
      }

      this.$refs.searchBox.blur()
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
      format: Format,
      searchText: null
    }
  }
}
</script>
