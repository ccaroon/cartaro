<template>
  <v-container>
    <AppBar
      v-bind:name="'Work Days'"
      v-bind:numPages="Math.ceil(totalDays / perPage)"
      v-bind:newItem="newWeek"
      v-bind:newIcon="'mdi-calendar-plus'"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list>
      <v-list-item
        v-for="(workDay, idx) in workDays"
        :key="workDay.id"
        :class="rowColor(idx)"
      >
        <v-list-item-avatar>
          <v-icon>mdi-{{ constants.ICONS.workDays[workDay.type] }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title
            :class="
              workDay.deleted_at !== null ? 'text-decoration-line-through' : ''
            "
            ><strong>{{ displayTitle(workDay) }}</strong></v-list-item-title
          >
          <v-list-item-subtitle>
            {{ displaySubtitle(workDay) }}
          </v-list-item-subtitle>
          <v-list-item-subtitle>
            {{ displayHoursWorked(workDay) }}
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-row dense align="center" justify="space-around">
          <v-col cols="2">
            <v-menu
              ref="timeInPicker"
              v-model="showTimeInMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="workDay.time_in"
                  label="IN"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-model="workDay.time_in"
                color="green"
                ampm-in-title
                scrollable
              ></v-time-picker>
              <v-sheet width="100%">
                <v-row dense align="center" justify="space-around">
                  <v-col cols="2">
                    <v-btn
                      color="green"
                      small
                      rounded
                      @click="
                        save(workDay);
                        $set(showTimeInMenu, idx, false);
                      "
                      >OK</v-btn
                    >
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      color="red"
                      text
                      @click="$set(showTimeInMenu, idx, false)"
                      >Cancel</v-btn
                    >
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
          <v-col cols="2">
            <v-menu
              ref="timeOutPicker"
              v-model="showTimeOutMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="workDay.time_out"
                  label="OUT"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-time-picker
                v-model="workDay.time_out"
                color="red"
                ampm-in-title
                scrollable
              ></v-time-picker>
              <v-sheet width="100%">
                <v-row dense align="center" justify="space-around">
                  <v-col cols="2">
                    <v-btn
                      color="green"
                      small
                      rounded
                      @click="
                        save(workDay);
                        $set(showTimeOutMenu, idx, false);
                      "
                      >OK</v-btn
                    >
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      color="red"
                      text
                      @click="$set(showTimeOutMenu, idx, false)"
                      >Cancel</v-btn
                    >
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
          <v-col cols="2">
            <v-btn-toggle
              v-model="workDay.type"
              dense
              rounded
              mandatory
              @change="changeType(workDay)"
            >
              <v-btn icon value="normal">
                <v-icon>mdi-{{ constants.ICONS.workDays.normal }}</v-icon>
              </v-btn>
              <v-btn icon value="holiday">
                <v-icon>mdi-{{ constants.ICONS.workDays.holiday }}</v-icon>
              </v-btn>
              <v-btn icon value="pto">
                <v-icon>mdi-{{ constants.ICONS.workDays.pto }}</v-icon>
              </v-btn>
              <v-btn icon value="sick">
                <v-icon>mdi-{{ constants.ICONS.workDays.sick }}</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-col>
          <v-col cols="5" full-width>
            <v-text-field
              v-model="workDay.note"
              placeholder="Note"
              autofocus
              @change="save(workDay)"
            ></v-text-field>
          </v-col>
        </v-row>
        <Actions
          v-bind:actions="{ remove: remove }"
          v-bind:item="workDay"
        ></Actions>
      </v-list-item>
    </v-list>
    <v-footer absolute>
      {{ displayWorkDates() }}
      <v-spacer></v-spacer>
      {{ displayYearWeek() }}
      <v-spacer></v-spacer>
      Hours Worked: {{ totalHours() }}
    </v-footer>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'
import Notification from '../lib/Notification'
import Utils from '../lib/Utils'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import Tags from './Shared/Tags'

import { fetchWorkDays } from '../models/WorkDay'

// TODO: Move consts to WorkDay model
const DAYS_PER_WEEK = 7
const WEEKS_TO_SHOW = 5

const DEFAULT_IN = '09:00'
const DEFAULT_OUT = '16:30'

export default {
  name: 'workDays-main',
  components: { Actions, AppBar, Tags },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newWeek()
        return false
      })
    },

    displayTitle: function (workDay) {
      return Format.formatDate(workDay.date * 1000, 'dddd')
    },

    displaySubtitle: function (workDay) {
      return Format.formatDate(workDay.date * 1000, 'MMM DD, YYYY')
    },

    displayHoursWorked: function (workDay) {
      const duration = workDay.hoursWorked()
      return `${duration.hours()}h ${duration.minutes()}m`
    },

    displayWorkDates: function () {
      let dateStr = ''
      if (this.workDays[0] && this.workDays[4]) {
        const start = Format.formatDate(this.workDays[0].date * 1000, 'MMM DD, YYYY')
        const end = Format.formatDate(this.workDays[4].date * 1000, 'MMM DD, YYYY')

        dateStr = `${start} to ${end}`
      }
      return dateStr
    },

    displayYearWeek: function () {
      let weekStr = ''
      if (this.workDays[0]) {
        weekStr = `Week ${Format.formatDate(this.workDays[0].date * 1000, 'WW')}`
      }
      return weekStr
    },

    totalHours: function () {
      let total = 0
      this.workDays.forEach(day => {
        const duration = day.hoursWorked()
        total += duration.asHours()
      })

      return total.toFixed(1)
    },

    refresh: function (page = null, searchText = '') {
      if (page !== null) {
        this.page = page
        this.currWeek = Moment().startOf('week').subtract((this.page - 1) * 7, 'days')
      }

      if (searchText !== '') {
        this.searchText = searchText
      }

      this.load()
    },

    load: function () {
      if (this.searchText) {
        this.search()
      } else {
        this.loadWeek()
      }
    },

    search: function () {
      var self = this
      this.perPage = 10

      var query = {
        page: this.page,
        pp: this.perPage
      }

      var parts = this.searchText.split(':', 2)
      if (parts.length === 2) {
        query[parts[0].trim()] = parts[1].trim()
      } else {
        query.note = this.searchText
      }

      fetchWorkDays(query, '/', {
        onSuccess: function (days, totalCount) {
          self.totalDays = totalCount
          self.workDays = days
        },
        onError: (err) => {
          Notification.error(err.toString())
        }
      })
    },

    loadWeek: function () {
      var self = this
      this.perPage = DAYS_PER_WEEK
      var query = {
        pp: this.perPage,
        start: this.currWeek.format('YYYY-MM-DD'),
        days: DAYS_PER_WEEK
      }

      fetchWorkDays(query, '/range', {
        onSuccess: function (days, totalCount) {
          self.totalDays = WEEKS_TO_SHOW * DAYS_PER_WEEK
          self.workDays = days
        },
        onError: (err) => {
          Notification.error(err.toString())
        }
      })
    },

    newDay: function (day = Moment().startOf('week').add(1, 'day')) {
      var workDay = {
        date: null,
        time_in: DEFAULT_IN,
        time_out: DEFAULT_OUT,
        note: null,
        type: 'normal'
      }

      workDay.date = day.unix()
      return this.$http.post(`http://127.0.0.1:4242/work_days/`, workDay)
    },

    newWeek: async function () {
      // This Monday
      var day = Moment().startOf('week').add(1, 'day')

      for (let i = 1; i <= 5; i++) {
        await this.newDay(day)
        day.add(1, 'day')
      }
      this.load()
    },

    changeType: function (workDay) {
      // TODO: Define type constants in WorkDay model
      if (workDay.type !== 'normal') {
        this.clearInOut(workDay)
      } else {
        workDay.time_in = DEFAULT_IN
        workDay.time_out = DEFAULT_OUT
      }

      this.save(workDay)
    },

    clearInOut: function (workDay) {
      workDay.time_in = '00:00'
      workDay.time_out = '00:00'
    },

    save: function (workDay) {
      this.$http.put(`http://127.0.0.1:4242/work_days/${workDay.id}`, workDay)
        .then(resp => {
        })
        .catch(err => {
          Notification.error(err.toString())
        })
    },

    remove: function (workDay) {
      var self = this
      var safe = 1
      var msg = `Safe Delete "${this.displayName(workDay)}"?`

      if (workDay.deleted_at) {
        safe = 0
        msg = `Delete "${this.displayName(workDay)}"?`
      }

      var doDelete = confirm(msg)
      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/work_days/${workDay.id}?safe=${safe}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            Notification.error(err.toString())
          })
      }
    },

    rowColor: function (idx) {
      var workDay = this.workDays[idx]
      let color = Utils.rowColor(idx)

      if (workDay && Moment().isSame(Moment.unix(workDay.date), 'day')) {
        color = Constants.COLORS.ITEM_HIGHLIGHT
      }

      return color
    }
  },

  data () {
    return {
      // Note: start of the week is a Sunday
      currWeek: Moment().startOf('week'),
      workDays: [], // a Week
      page: 1,
      perPage: DAYS_PER_WEEK,
      totalDays: 0,
      constants: Constants,
      format: Format,
      searchText: null,
      showTimeInMenu: [],
      showTimeOutMenu: []
    }
  }
}
</script>
