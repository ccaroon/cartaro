<template>
  <v-sheet width="100%">
    <v-list dense class="pa-0">
      <v-row dense no-gutters>
        <v-col cols="2" v-for="(entries, idx) in workDays" :key="idx">
          <v-list-item :class="dayColor(idx, entries[0]) + ' pa-0'" dense>
            <v-list-item-content class="pl-2">
              <v-list-item-title>
                <strong
                  >{{ format.formatDate(entries[0].date * 1000, "dddd") }}
                </strong>
                ({{ displayHoursWorked(entries) }})
              </v-list-item-title>
              <v-list-item-subtitle v-for="(day, indx) in entries" :key="indx">
                <v-icon size="small">{{ day.icon() }}</v-icon>
                <template v-if="!day.allDay()">
                  {{ format.formatDate(day.start(), "h:mma") }} -
                  {{ format.formatDate(day.end(), "h:mma") }}
                </template>
                <template v-else>
                  {{ day.note || day.type.toUpperCase() }}
                </template>
                <v-tooltip bottom v-if="day.note && !day.allDay()">
                  <template v-slot:activator="{ on }">
                    <v-icon size="small" v-on="on">mdi-note-outline</v-icon>
                  </template>
                  <span>{{ day.note || day.type.toUpperCase() }}</span>
                </v-tooltip>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
        <v-col cols="2">
          <v-list-item class="grey lighten-2 pa-0">
            <v-list-item-avatar class="ma-0">
              <v-icon>mdi-sigma</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                ><strong>Weekly Total</strong></v-list-item-title
              >
              <v-list-item-subtitle>
                <v-icon size="small" color="green">mdi-calendar-check</v-icon>
                {{ totalHours("online") }} hrs |
                <v-icon size="small" color="red">mdi-calendar-remove</v-icon>
                {{ totalHours("away") }} hrs
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
  </v-sheet>
</template>
<script>
import Moment from 'moment'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'

import WorkDay from '../../models/WorkDay'

const HOURS_PER_WEEK = 37.5

export default {
  name: 'home-work-days',
  components: {},

  mounted: function () {
    this.load()
  },

  methods: {
    refresh: function () {
      this.load()
    },

    load: function () {
      const self = this
      const query = {
        start: Moment().startOf('week').format('YYYY-MM-DD'),
        days: 7
      }

      WorkDay.fetch(query, '/range', {
        handlers: {
          onSuccess: function (days, totalCount) {
            const collatedDays = {}

            // Create a Hash of day entries
            // - key is the day's date
            // - value is a list of day entries for that date
            days.forEach(day => {
              let bucket = collatedDays[day.date]
              if (bucket === undefined) {
                bucket = []
                collatedDays[day.date] = bucket
              }
              bucket.push(day)
            })

            self.workDays = Object.values(collatedDays)
            self.workDays.forEach(entries => {
              entries.sort((day1, day2) => {
                return day1.created_at - day2.created_at
              })
            })
          },
          onError: function (err) {
            Notification.error(`HM.WDays.load: ${err}`)
          }
        }
      })
    },

    displayHoursWorked: function (entries) {
      let totalHours = 0
      let totalMins = 0
      entries.forEach(day => {
        const duration = day.hoursWorked()
        totalHours += duration.hours()
        totalMins += duration.minutes()
      })

      return `${totalHours}h ${totalMins}m`
    },

    totalHours: function (timeFrame = 'online') {
      let total = 0
      this.workDays.forEach(entries => {
        entries.forEach(day => {
          const duration = day.hoursWorked()
          total += duration.asHours()
        })
      })

      if (timeFrame === 'away') {
        total = HOURS_PER_WEEK - total
      }

      return total.toFixed(1)
    },

    dayColor: function (idx, workDay) {
      const alt = idx % 2 === 0
      let color = workDay.color('light', alt)

      if (Moment().startOf('day').isSame(workDay.date * 1000)) {
        color = Constants.COLORS.ITEM_HIGHLIGHT
      }

      return color
    }
  },

  data () {
    return {
      // List of day entries. Each day can contain more than 1 entry.
      workDays: [],
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
