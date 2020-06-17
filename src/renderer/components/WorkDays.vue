<template>
  <v-container>
    <AppBar
      v-bind:name="'Work Days'"
      v-bind:numPages="Math.ceil(totalDays/perPage)"
      v-bind:newItem="newWeek"
      v-bind:newIcon="'mdi-calendar-plus'"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list dense>
      <v-list-item v-for="(workDay,idx) in workDays" :key="workDay.id" :class="rowColor(idx)">
        <v-list-item-content>
          <v-list-item-title
            class="subtitle-1"
            v-if="workDay.deleted_at === null"
          >{{ displayName(workDay) }}</v-list-item-title>
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ displayName(workDay) }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ hoursWorked(workDay) }}
            <Tags v-bind:tags="workDay.tags" v-bind:color="rowColor(idx+1)"></Tags>
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
              <v-time-picker v-model="workDay.time_in" color="green" ampm-in-title scrollable></v-time-picker>
              <v-sheet width="100%">
                <v-row dense align="center" justify="space-around">
                  <v-col cols="2">
                    <v-btn
                      color="green"
                      small
                      rounded
                      @click="save(workDay); $set(showTimeInMenu, idx, false)"
                    >OK</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn color="red" text @click="$set(showTimeInMenu, idx, false)">Cancel</v-btn>
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
              <v-time-picker v-model="workDay.time_out" color="red" ampm-in-title scrollable></v-time-picker>
              <v-sheet width="100%">
                <v-row dense align="center" justify="space-around">
                  <v-col cols="2">
                    <v-btn
                      color="green"
                      small
                      rounded
                      @click="save(workDay); $set(showTimeOutMenu, idx, false)"
                    >OK</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn color="red" text @click="$set(showTimeOutMenu, idx, false)">Cancel</v-btn>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
          <v-col cols="2">
            <v-btn-toggle v-model="workDay.type" dense rounded mandatory @change="save(workDay)">
              <v-btn icon value="normal">
                <v-icon>mdi-calendar</v-icon>
              </v-btn>
              <v-btn icon value="holiday">
                <v-icon>mdi-flag-variant</v-icon>
              </v-btn>
              <v-btn icon value="pto">
                <v-icon>mdi-island</v-icon>
              </v-btn>
              <v-btn icon value="sick">
                <v-icon>mdi-hospital-box</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-col>
          <v-col cols="6" full-width>
            <v-text-field
              v-model="workDay.note"
              placeholder="Note"
              autofocus
              @change="save(workDay)"
            ></v-text-field>
          </v-col>
        </v-row>
        <Actions v-bind:actions="{remove: remove}" v-bind:item="workDay"></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import Tags from './Shared/Tags'

const DAYS_PER_WEEK = 7
const WEEKS_TO_SHOW = 5

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

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })
    },

    displayName: function (workDay) {
      var name = Format.formatDate(workDay.date * 1000, 'ddd (MMM Do, YYYY)')
      return (name)
    },

    hoursWorked: function (workDay) {
      var inTime = workDay.time_in.split(':')
      var dayStart = Moment(workDay.date * 1000).startOf('day').hours(inTime[0]).minutes(inTime[1])

      var outTime = workDay.time_out.split(':')
      var dayEnd = Moment(workDay.date * 1000).startOf('day').hours(outTime[0]).minutes(outTime[1])

      var duration = Moment.duration(dayEnd.diff(dayStart))

      return `${duration.hours()}h ${duration.minutes()}m`
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
      // Change number of items per page for search results
      this.perPage = 10
      var qs = `page=${this.page}&pp=${this.perPage}`

      var parts = this.searchText.split(':', 2)
      if (parts.length === 2) {
        qs += `&${parts[0].trim()}=${parts[1].trim()}`
      } else {
        qs += `&note=${this.searchText}`
      }

      this.$http.get(`http://127.0.0.1:4242/work_days/?${qs}`)
        .then(resp => {
          self.totalDays = resp.data.total
          self.workDays = resp.data.work_days
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    loadWeek: function () {
      var self = this
      this.perPage = DAYS_PER_WEEK
      var qs = `start=${this.currWeek.format('YYYY-MM-DD')}&days=${DAYS_PER_WEEK}`

      this.$http.get(`http://127.0.0.1:4242/work_days/range?${qs}`)
        .then(resp => {
          self.totalDays = WEEKS_TO_SHOW * DAYS_PER_WEEK
          self.workDays = resp.data.work_days
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    newDay: function (day = Moment().startOf('week').add(1, 'day')) {
      var workDay = {
        date: null,
        time_in: '09:00',
        time_out: '16:30',
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

    save: function (workDay, dryRun = false) {
      if (dryRun) {
        console.log(workDay)
      } else {
        this.$http.put(`http://127.0.0.1:4242/work_days/${workDay.id}`, workDay)
          .then(resp => {
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    remove: function (workDay) {
      var self = this

      var doDelete = confirm(`Delete "${this.displayName(workDay)}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/work_days/${workDay.id}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    rowColor: function (idx) {
      var workDay = this.workDays[idx]
      var color = Constants.COLORS.GREY

      if (workDay && Moment().isSame(Moment.unix(workDay.date), 'day')) {
        color = Constants.COLORS.ITEM_HIGHLIGHT
      } else if (idx % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
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
      format: Format,
      searchText: null,
      showTimeInMenu: [],
      showTimeOutMenu: []
    }
  }
}
</script>
