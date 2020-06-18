<template>
  <v-container>
    <AppBar
      v-bind:name="'Countdowns'"
      v-bind:numPages="Math.ceil(totalCountDowns/perPage)"
      v-bind:newItem="newCountDown"
      v-bind:newIcon="'mdi-file-clock'"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list dense>
      <v-list-item v-for="(countDown,idx) in countDowns" :key="countDown.id" :class="rowColor(idx)">
        <v-list-item-content>
          <v-list-item-title>
            <v-text-field
              v-model="countDown.name"
              placeholder="Name"
              dense
              single-line
              autofocus
              @change="save(countDown)"
            ></v-text-field>
          </v-list-item-title>
          <v-list-item-subtitle>{{ humanize(countDown) }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-row dense align="center">
          <v-col cols="4">
            <v-menu
              ref="startDatePicker"
              v-model="showStartDateMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  label="Start"
                  prepend-icon="mdi-calendar-clock"
                  readonly
                  :value="dateDisplay(countDown, 'start')"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-sheet width="100%">
                <v-row dense align="end">
                  <v-col cols="6">
                    <v-date-picker v-model="countDown.startDate" color="green" flat scrollable></v-date-picker>
                  </v-col>
                  <v-col cols="6">
                    <v-time-picker v-model="countDown.startTime" color="green" flat scrollable></v-time-picker>
                  </v-col>
                </v-row>
                <v-row dense align="center" justify="center">
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="green"
                      @click="save(countDown); $set(showStartDateMenu, idx, false)"
                    >OK</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="blue"
                      @click="countDown.startDate = format.formatDate(Date.now(), 'YYYY-MM-DD')"
                    >Today</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      text
                      color="red"
                      @click="initDate(countDown); $set(showStartDateMenu, idx, false)"
                    >Cancel</v-btn>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
          <v-col cols="4">
            <v-menu
              ref="endDatePicker"
              v-model="showEndDateMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  label="End"
                  prepend-icon="mdi-calendar-clock"
                  readonly
                  clearable
                  @click:clear="clearEndDate(countDown)"
                  :value="dateDisplay(countDown, 'end')"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-sheet width="100%">
                <v-row dense align="end">
                  <v-col cols="6">
                    <v-date-picker v-model="countDown.endDate" color="red" flat scrollable></v-date-picker>
                  </v-col>
                  <v-col cols="6">
                    <v-time-picker v-model="countDown.endTime" color="red" flat scrollable></v-time-picker>
                  </v-col>
                </v-row>
                <v-row dense align="center" justify="center">
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="green"
                      @click="save(countDown); $set(showEndDateMenu, idx, false)"
                    >OK</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="blue"
                      @click="countDown.endDate = format.formatDate(Date.now(), 'YYYY-MM-DD')"
                    >Today</v-btn>
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      text
                      color="red"
                      @click="initDate(countDown); $set(showEndDateMenu, idx, false)"
                    >Cancel</v-btn>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
        </v-row>
        <Actions v-bind:actions="{remove: remove}" v-bind:item="countDown"></Actions>
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

export default {
  name: 'countDowns-main',
  components: { Actions, AppBar },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newCountDown()
        return false
      })

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })
    },

    refresh: function (page = null, searchText = '') {
      if (page !== null) {
        this.page = page
      }

      if (searchText !== '') {
        this.searchText = searchText
      }

      this.load()
    },

    load: function () {
      var self = this
      var qs = `page=${this.page}&pp=${this.perPage}&sort_by=start_at`

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          qs += `&${parts[0].trim()}=${parts[1].trim()}`
        } else {
          qs += `&name=${this.searchText}`
        }
      }

      this.$http.get(`http://127.0.0.1:4242/count_downs/?${qs}`)
        .then(resp => {
          self.totalCountDowns = resp.data.total
          self.countDowns = resp.data.count_downs

          self.countDowns.forEach((cd) => {
            self.initDate(cd)
          })
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    newCountDown: function () {
      var countDown = {
        name: '** NEW COUNTDOWN **',
        // Set Date to something early so it appears at the top of the list
        start_at: Moment('1971-01-01').unix(),
        end_at: null
      }

      this.$http.post(`http://127.0.0.1:4242/count_downs/`, countDown)
        .then(resp => {
          this.load()
        })
        .catch(err => {
          console.log(`Error creating CountDown: ${err}`)
        })
    },

    dateDisplay: function (countDown, type) {
      var asString = ''
      var dateAttr = `${type}Date`
      var timeAttr = `${type}Time`

      if (countDown[dateAttr] && countDown[timeAttr]) {
        asString = countDown[dateAttr] + ' @ ' + countDown[timeAttr]
      }

      return asString
    },

    humanize: function (countDown) {
      var now = Moment()
      var value = null

      if (countDown.start_at && !countDown.end_at) {
        const start = Moment.unix(countDown.start_at)

        // * Start Only: BEFORE Event -> Count Down | AFTER Event -> Count Up
        value = start.from(now)
      } else if (countDown.start_at && countDown.end_at) {
        const start = Moment.unix(countDown.start_at)
        const end = Moment.unix(countDown.end_at)

        // * Start & End: BEFORE -> Count Down | DURING -> Count Up | AFTER -> Show Duration
        if (now.isBefore(start)) {
          // 'BEFORE --> Count DOWN'
          value = `Starts ${start.from(now)}`
        } else if (now.isBetween(start, end)) {
          // 'DURING --> Count Up'
          value = `Ends ${end.from(now)}`
        } else {
          // 'AFTER --> DURATION'
          value = start.from(end, true)
        }
      }

      return value
    },

    // Init dates for use with date-picker / time-picker
    initDate: function (countDown) {
      this.$set(countDown, 'startDate', Format.formatDate(countDown.start_at * 1000, 'YYYY-MM-DD'))
      this.$set(countDown, 'startTime', Format.formatDate(countDown.start_at * 1000, 'HH:mm'))

      var endDate = null
      var endTime = null
      if (countDown.end_at) {
        endDate = Format.formatDate(countDown.end_at * 1000, 'YYYY-MM-DD')
        endTime = Format.formatDate(countDown.end_at * 1000, 'HH:mm')
      }

      this.$set(countDown, 'endDate', endDate)
      this.$set(countDown, 'endTime', endTime)
    },

    clearEndDate: function (countDown) {
      countDown.endDate = null
      countDown.endTime = null

      this.save(countDown)
    },

    save: function (countDown) {
      var self = this
      countDown.start_at = Moment(`${countDown.startDate} ${countDown.startTime}`, 'YYYY-MM-DD HH:mm:ss').unix()

      if (countDown.endDate && countDown.endTime) {
        countDown.end_at = Moment(`${countDown.endDate} ${countDown.endTime}`, 'YYYY-MM-DD HH:mm:ss').unix()
      } else {
        countDown.end_at = null
      }

      this.$http.put(`http://127.0.0.1:4242/count_downs/${countDown.id}`, countDown)
        .then(resp => {
          self.load()
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    remove: function (countDown) {
      var self = this

      var doDelete = confirm(`Delete "${countDown.name}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/count_downs/${countDown.id}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

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
      countDowns: [],
      page: 1,
      perPage: 11,
      totalCountDowns: 0,
      format: Format,
      searchText: null,
      showStartDateMenu: [],
      showStartTimeMenu: [],
      showEndDateMenu: [],
      showEndTimeMenu: []
    }
  }
}
</script>
<style lang="sass" scoped>
// ** Not Working **
// I want to make the time-picker heading height shorter
// Cannot get any SASS for time-picker to work here.
// *****************
// $time-picker-title-color: #00f
// $time-picker-title-btn-height: 25px !default
</style>
