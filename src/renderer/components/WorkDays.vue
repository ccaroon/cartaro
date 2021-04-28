<template>
  <v-container>
    <AppBar
      v-bind:name="'Work Days'"
      v-bind:numPages="Math.ceil(totalDays / perPage)"
      v-bind:buttons="appBarButtons"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list>
      <v-list-item
        v-for="(workDay, idx) in workDays"
        :key="workDay.id"
        :class="rowColor(idx)"
      >
        <v-list-item-avatar>
          <v-icon>{{ workDay.icon() }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title
            :class="workDay.isDeleted() ? 'text-decoration-line-through' : ''"
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
              :disabled="workDay.isDeleted()"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="workDay.time_in"
                  label="IN"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                  :disabled="workDay.isDeleted()"
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
              :disabled="workDay.isDeleted()"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="workDay.time_out"
                  label="OUT"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                  :disabled="workDay.isDeleted()"
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
              <v-btn icon value="normal" :disabled="workDay.isDeleted()">
                <v-icon>{{ icons.get("workday") }}</v-icon>
              </v-btn>
              <v-btn icon value="holiday" :disabled="workDay.isDeleted()">
                <v-icon>{{ icons.get("holiday") }}</v-icon>
              </v-btn>
              <v-btn icon value="pto" :disabled="workDay.isDeleted()">
                <v-icon>{{ icons.get("pto") }}</v-icon>
              </v-btn>
              <v-btn icon value="sick" :disabled="workDay.isDeleted()">
                <v-icon>{{ icons.get("sick") }}</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-col>
          <v-col cols="5" full-width>
            <v-text-field
              v-model="workDay.note"
              placeholder="Note"
              autofocus
              :disabled="workDay.isDeleted()"
              @change="save(workDay)"
            ></v-text-field>
          </v-col>
        </v-row>
        <Actions
          v-bind:actions="{
            onArchiveDelete: (event, item) => {
              if (event.startsWith('post-')) {
                refresh();
              }
            },
          }"
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
import Icon from '../lib/Icon'
import Notification from '../lib/Notification'
import Utils from '../lib/Utils'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'

import WorkDay from '../models/WorkDay'

const DAYS_PER_WEEK = 7
const WEEKS_TO_SHOW = 5

export default {
  name: 'workDays-main',
  components: { Actions, AppBar },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

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
      const self = this
      this.perPage = 10

      const query = {
        page: this.page,
        pp: this.perPage
      }

      const parts = this.searchText.split(':', 2)
      if (parts.length === 2) {
        query[parts[0].trim()] = parts[1].trim()
      } else {
        query.note = this.searchText
      }

      WorkDay.fetch(query, '/', {
        handlers: {
          onSuccess: function (days, totalCount) {
            self.totalDays = totalCount
            self.workDays = days
          },
          onError: (err) => {
            Notification.error(`WD.Main.search: ${err.toString()}`)
          }
        }
      })
    },

    loadWeek: function () {
      const self = this
      this.perPage = DAYS_PER_WEEK
      const query = {
        pp: this.perPage,
        start: this.currWeek.format('YYYY-MM-DD'),
        days: DAYS_PER_WEEK
      }

      WorkDay.fetch(query, '/range', {
        handlers: {
          onSuccess: function (days, totalCount) {
            self.totalDays = WEEKS_TO_SHOW * DAYS_PER_WEEK
            self.workDays = days
          },
          onError: (err) => {
            Notification.error(`WD.Main.loadWeek: ${err.toString()}`)
          }
        }
      })
    },

    newDay: function (day = Moment().startOf('week').add(1, 'day')) {
      const workDay = new WorkDay({
        date: day.unix(),
        time_in: WorkDay.DEFAULT_IN,
        time_out: WorkDay.DEFAULT_OUT,
        note: null,
        type: WorkDay.TYPE_NORMAL
      })

      return workDay.save({ asPromise: true })
    },

    newWeek: async function () {
      // This Monday
      const day = Moment().startOf('week').add(1, 'day')

      for (let i = 1; i <= 5; i++) {
        await this.newDay(day)
        day.add(1, 'day')
      }
      this.load()
    },

    changeType: function (workDay) {
      if (workDay.type !== WorkDay.TYPE_NORMAL) {
        workDay.clearInOut()
      } else {
        workDay.time_in = WorkDay.DEFAULT_IN
        workDay.time_out = WorkDay.DEFAULT_OUT
      }

      this.save(workDay)
    },

    save: function (workDay) {
      workDay.save({
        handlers: {
          onSuccess: null,
          onError: (err) => Notification.error(`WD.Main.save: ${err.toString()}`)
        }
      })
    },

    rowColor: function (idx) {
      const workDay = this.workDays[idx]
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
      icons: Icon,
      searchText: null,
      showTimeInMenu: [],
      showTimeOutMenu: [],
      appBarButtons: [
        { name: 'New Week', icon: 'mdi-calendar-plus', action: this.newWeek }
      ]
    }
  }
}
</script>
