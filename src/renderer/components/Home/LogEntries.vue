<template>
  <div>
    <LogEntryEditor
      v-model="showEditor"
      v-bind:logEntry="logEntry"
      v-on:close="closeEditor"
      v-on:view="closeAndView"
    ></LogEntryEditor>
    <LogEntryViewer
      v-model="showViewer"
      v-bind:logEntry="logEntry"
      v-on:close="showViewer = false"
      v-on:edit="closeAndEdit"
    ></LogEntryViewer>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Log Entries
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ logEntries.length }})</span
        >
        <v-btn icon x-small @click="newEntry()"
          ><v-icon>mdi-plus</v-icon></v-btn
        >
      </v-card-title>

      <v-virtual-scroll
        :items="logEntries"
        item-height="45"
        :height="listHeight"
      >
        <template v-slot:default="{ index, item }">
          <v-list-item
            :class="rowColor(item, index)"
            @click="viewEntry(item)"
            dense
          >
            <v-list-item-icon>
              <v-icon
                v-if="item.ticket_link"
                @click.stop="utils.openLink(item.ticket_link)"
                color="blue"
                >{{ item.icon() }}</v-icon
              >
              <v-icon v-else>{{ item.icon() }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.subject }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ format.formatDate(item.logged_at * 1000, "ddd") }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-icon>
              <v-btn x-small icon outlined class="ma-1">
                <v-icon small outline @click.stop="editEntry(item)"
                  >mdi-pencil</v-icon
                >
              </v-btn>
              <v-btn x-small icon outlined class="ma-1">
                <v-icon small outline @click.stop="dupEntry(item)"
                  >mdi-content-duplicate</v-icon
                >
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
import Moment from 'moment'

import LogEntryEditor from '../LogEntries/Editor'
import LogEntryViewer from '../LogEntries/Viewer'

import LogEntry from '../../models/LogEntry'

import constants from '../../lib/constants'
import format from '../../lib/format'
import notification from '../../lib/notification'
import utils from '../../lib/utils'

export default {
  name: 'home-log-entries',
  components: { LogEntryEditor, LogEntryViewer },

  mounted: function () {
    this.loadEntries()
  },

  methods: {
    newEntry: function () {
      this.logEntry = new LogEntry({
        logged_at: Moment().unix()
      })
      this.showEditor = true
    },

    dupEntry: function (entry) {
      this.logEntry = new LogEntry({
        subject: entry.subject,
        category: entry.category,
        ticket_link: entry.ticket_link,
        tags: entry.tags,
        logged_at: Moment().unix()
      })
      this.showEditor = true
    },

    editEntry: function (entry) {
      this.logEntry = entry
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.loadEntries()
    },

    viewEntry: function (entry) {
      this.logEntry = entry
      this.showViewer = true
    },

    closeAndEdit: function () {
      this.showViewer = false
      this.editEntry(this.logEntry)
    },

    closeAndView: function () {
      this.showEditor = false
      this.viewEntry(this.logEntry)
    },

    loadEntries: function () {
      const self = this
      const startOfWeek = Moment().startOf('week')
      const query = {
        pp: 25,
        logged_at: `gte:${startOfWeek.unix()}`,
        sort_by: 'logged_at:desc'
      }

      LogEntry.fetch(query, '/', {
        handlers: {
          onSuccess: (items) => {
            self.logEntries = items
          },
          onError: (err) => { notification.error(`HM.LogEnt.loadEntries: ${err}`) }
        }
      })
    },

    rowColor: function (entry, index) {
      return utils.rowColor(index, entry.isToday())
    }
  },

  data () {
    return {
      logEntries: [],
      logEntry: {},
      listHeight: Math.round(window.innerHeight * 0.50),
      showEditor: false,
      showViewer: false,
      constants: constants,
      format: format,
      utils: utils
    }
  }
}
</script>
