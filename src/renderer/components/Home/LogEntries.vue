<template>
  <v-card>
    <v-card-title :class="constants.COLORS.GREY">Log Entries</v-card-title>
    <v-card-text>
      <v-list dense>
        <v-list-item
          v-for="(entry, idx) in logEntries"
          :key="idx"
          :class="utils.rowColor(idx)"
          dense
        >
          <v-list-item-icon>
            <v-btn
              fab
              x-small
              v-if="entry.ticket_link"
              @click="utils.openLink('Jira', entry.ticket_link)"
            >
              <v-icon color="grey darken-1"
                >mdi-{{
                  constants.ICONS.logEntries[entry.category.toLowerCase()]
                }}</v-icon
              >
            </v-btn>
            <v-btn fab x-small plain v-else>
              <v-icon
                >mdi-{{
                  constants.ICONS.logEntries[entry.category.toLowerCase()]
                }}</v-icon
              >
            </v-btn>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>
              {{ entry.subject }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ format.formatDate(entry.logged_at * 1000, "ddd") }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>
<script>
// import Moment from 'moment'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Utils from '../../lib/Utils'

export default {
  name: 'home-log-entries',
  components: {},

  mounted: function () {
    this.loadEntries()
  },

  methods: {
    loadEntries: function () {
      var self = this
      // TODO: currently no way to search for things < or > etc.
      // const startDate = Moment().startOf('week')
      // const endDate = Moment().endOf('week')
      var qs = `pp=10&sort_by=logged_at:desc`

      this.$http.get(`http://127.0.0.1:4242/log_entries/?${qs}`)
        .then(resp => {
          self.logEntries = resp.data.log_entries
        })
        .catch(err => {
          self.$emit('error', 'error', `Log Entries: ${err.response.status} - ${err.response.data.error.substring(0, 120)}`)
        })
    }
  },

  data () {
    return {
      logEntries: [],
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
