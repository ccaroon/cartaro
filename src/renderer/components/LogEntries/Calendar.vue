<template>
  <div>
    <v-sheet tile class="d-flex">
      <v-row>
        <v-col offset="4" cols="1" align="end">
          <v-btn icon @click="$refs.calendar.prev()">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn icon @click="goToToday()">
            <v-icon>mdi-calendar-today</v-icon>
          </v-btn>
          <v-btn icon @click="$refs.calendar.next()">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="3" align="start">
          <span class="text-h4">{{
            format.formatDate(calDate, "MMMM YYYY")
          }}</span>
        </v-col>
      </v-row>
    </v-sheet>
    <v-sheet :height="calHeight">
      <v-calendar
        ref="calendar"
        v-model="calDate"
        color="grey"
        event-text-color="black"
        :event-more="false"
        :events="events"
        @click:event="editEntry"
        @click:date="newEntry"
      >
      </v-calendar>
    </v-sheet>
  </div>
</template>
<script>
import Moment from 'moment'
import format from '../../lib/format'

export default {
  name: 'log-entries-calendar',
  props: ['logEntries'],

  mounted: function () {
    this.createEvents()
  },

  methods: {
    editEntry: function (event) {
      this.$emit('edit', event.event.entry)
    },

    newEntry: function (event) {
      this.$emit('new', Moment(event.date).unix())
    },

    goToToday: function () {
      this.calDate = format.formatDate(new Date(), 'YYYY-MM-DD')
    },

    createEvents: function () {
      const events = []
      this.logEntries.forEach((entry) => {
        const name = entry.subject

        const logDate = Moment.unix(entry.logged_at)
        events.push({
          name,
          start: logDate.toDate(),
          end: logDate.toDate(),
          color: entry.color(),
          timed: false,
          entry: entry
        })
      })

      this.events = events
    },

    refresh: function () {
      this.$emit('refresh', { calDate: this.calDate })
    }
  },

  watch: {
    calDate: function () {
      this.refresh()
    },

    logEntries: function () {
      this.createEvents()
    }
  },

  data () {
    return {
      calDate: format.formatDate(new Date(), 'YYYY-MM-DD'),
      // weekStart: Moment().startOf('week'),
      // weekEnd: Moment().endOf('week'),
      events: [],
      calHeight: Math.round(window.innerHeight * 0.85),
      format: format
    }
  }
}
</script>
