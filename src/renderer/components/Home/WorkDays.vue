<template>
  <v-sheet width="100%">
    <v-list dense rounded>
      <v-row dense no-gutters>
        <v-col cols="2" v-for="(workDay, idx) in workDays" :key="workDay.id">
          <v-list-item :class="dayColor(idx, workDay)" dense>
            <v-list-item-avatar>
              <v-icon>mdi-{{ constants.ICONS.workDays[workDay.type] }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                <strong>{{
                  format.formatDate(workDay.date * 1000, "dddd")
                }}</strong>
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ displayHoursWorked(workDay) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
        <v-col cols="2">
          <v-list-item class="grey lighten-1">
            <v-list-item-avatar>
              <v-icon>mdi-calendar-week</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title><strong>Total</strong></v-list-item-title>
              <v-list-item-subtitle> {{ totalHours() }} </v-list-item-subtitle>
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
      var self = this
      var query = {
        start: Moment().startOf('week').format('YYYY-MM-DD'),
        days: 7
      }

      WorkDay.fetch(query, '/range', {
        handlers: {
          onSuccess: function (days, totalCount) {
            self.workDays = days
          },
          onError: function (err) {
            Notification.error(`HM.WDays.load: ${err}`)
          }
        }
      })
    },

    displayHoursWorked: function (workDay) {
      var duration = workDay.hoursWorked()
      return `${duration.hours()}h ${duration.minutes()}m`
    },

    totalHours: function () {
      let total = 0
      this.workDays.forEach(day => {
        const duration = day.hoursWorked()
        total += duration.asHours()
      })

      return total.toFixed(1)
    },

    dayColor: function (idx, workDay) {
      var color = Utils.rowColor(idx)

      if (Moment().startOf('day').isSame(workDay.date * 1000)) {
        color = Constants.COLORS.ITEM_HIGHLIGHT
      }

      return color
    }
  },

  data () {
    return {
      workDays: [],
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
