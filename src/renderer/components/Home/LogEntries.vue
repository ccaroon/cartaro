<template>
  <div>
    <LogEntryEditor
      v-model="showEditor"
      v-bind:logEntry="logEntry"
      v-on:close="closeEditor"
    ></LogEntryEditor>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Log Entries
        <v-btn icon x-small @click="newEntry"><v-icon>mdi-plus</v-icon></v-btn>
      </v-card-title>

      <v-virtual-scroll :items="logEntries" item-height="50" height="500">
        <template v-slot:default="{ index, item }">
          <v-list-item
            :class="rowColor(item, index)"
            @click="editEntry(item)"
            dense
          >
            <v-list-item-icon>
              <v-btn
                fab
                x-small
                v-if="item.ticket_link"
                @click.stop="utils.openLink('Jira', item.ticket_link)"
              >
                <v-icon color="grey darken-1"
                  >mdi-{{
                    constants.ICONS.logEntries[item.category.toLowerCase()]
                  }}</v-icon
                >
              </v-btn>
              <v-btn fab x-small plain v-else>
                <v-icon
                  >mdi-{{
                    constants.ICONS.logEntries[item.category.toLowerCase()]
                  }}</v-icon
                >
              </v-btn>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.subject }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ format.formatDate(item.logged_at * 1000, "ddd") }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
import Moment from 'moment'

import LogEntryEditor from '../LogEntries/Editor'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Utils from '../../lib/Utils'

export default {
  name: 'home-log-entries',
  components: { LogEntryEditor },

  mounted: function () {
    this.loadEntries()
  },

  methods: {
    newEntry: function () {
      this.logEntry = {
        logged_at: Moment().unix()
      }
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

    loadEntries: function () {
      var self = this
      const startOfWeek = Moment().startOf('week')
      var qs = `logged_at=gte:${startOfWeek.unix()}&sort_by=logged_at:desc`

      this.$http.get(`http://127.0.0.1:4242/log_entries/?${qs}`)
        .then(resp => {
          self.logEntries = resp.data.log_entries
        })
        .catch(err => {
          self.$emit('error', 'error', `Log Entries: ${err.response.status} - ${err.response.data.error.substring(0, 120)}`)
        })
    },

    rowColor: function (entry, index) {
      var color = Utils.rowColor(index)

      if (Moment(entry.logged_at * 1000).isSame(Moment(), 'day')) {
        color = 'light-green accent-1'
        if (index % 2 === 1) {
          color = 'light-green accent-2'
        }
      }

      return color
    }
  },

  data () {
    return {
      logEntries: [],
      logEntry: {},
      showEditor: false,
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
