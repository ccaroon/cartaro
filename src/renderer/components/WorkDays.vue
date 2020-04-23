<template>
  <v-container>
    <AppBar
      v-bind:name="'Work Days'"
      v-bind:numPages="Math.ceil(totalWeeks/perPage)"
      v-bind:newItem="newEntry"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list dense>
      <v-list-item
        v-for="(workDay,idx) in workDays"
        :key="workDay.id"
        :class="rowColor(idx)"
        @click
      >
        <v-list-item-content @click="view(workDay)">
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
        <v-row dense>
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
            </v-menu>
          </v-col>
          <v-col cols="6">{{ workDay.note }}</v-col>
          <v-col cols="2">{{ workDay.type }}</v-col>
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
import WorkDayWeek from './WorkDays/Week'
import Tags from './Shared/Tags'

export default {
  name: 'workDays-main',
  components: { Actions, AppBar, WorkDayWeek, Tags },
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
      var self = this
      // var qs = `page=${this.page}&pp=${this.perPage}`
      var qs = `start=${this.currWeek.format('YYYY-MM-DD')}&days=7`

      //   if (this.searchText) {
      //     var parts = this.searchText.split(':', 2)
      //     if (parts.length === 2) {
      //       qs += `&${parts[0].trim()}=${parts[1].trim()}`
      //     } else {
      //       qs += `&subject=${this.searchText}&content=${this.searchText}`
      //     }
      //   }

      this.$http.get(`http://127.0.0.1:4242/work_days/range?${qs}`)
        .then(resp => {
          // self.totalWeeks = resp.data.total
          self.workDays = resp.data.work_days
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    // view: function (workDay) {
    //   this.workDay = workDay
    //   this.showViewer = true
    // },

    newEntry: function () {
      this.edit({
        logged_at: Moment().unix()
      })
    },

    // edit: function (workDay) {
    //   this.workDay = workDay
    //   this.showEditor = true
    // },

    remove: function (workDay) {
      var self = this

      var doDelete = confirm(`Delete "${this.displayName(workDay)}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/work_days/${workDay.id}?safe=1`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    // closeEditor: function () {
    //   this.showEditor = false
    //   this.refresh()
    // },

    // closeViewer: function () {
    //   this.showViewer = false
    // },

    rowColor: function (idx) {
      var color = Constants.COLORS.GREY

      if (idx % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
      }
      return color
    }
  },

  data () {
    return {
      currWeek: Moment().startOf('week'),
      workDay: {},
      workDays: [], // a Week
      page: 1,
      perPage: 1,
      totalWeeks: 4,
      //   showEditor: false,
      //   showViewer: false,
      format: Format,
      searchText: null,
      showTimeInMenu: [],
      showTimeOutMenu: []
    }
  }
}
</script>
