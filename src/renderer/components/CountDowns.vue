<template>
  <v-container>
    <AppBar
      v-bind:name="'Countdowns'"
      v-bind:numPages="Math.ceil(totalCountDowns/perPage)"
      v-bind:newItem="newCountDown"
      v-bind:newIcon="'mdi-update'"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list dense>
      <v-list-item v-for="(countDown,idx) in countDowns" :key="countDown.id" :class="rowColor(idx)">
        <v-list-item-content>
          <v-list-item-title
            class="subtitle-1"
            v-if="countDown.deleted_at === null"
          >{{ countDown.name }}</v-list-item-title>
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ countDown.name }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>{{ countDown.duration }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-row dense align="center" justify="space-around">
          <v-col cols="3">
            <v-menu
              ref="startDatePicker"
              v-model="showStartDateMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
              @click="initDate('start_at', countDown)"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="dateModels['start_at'][countDown.id]"
                  label="Start"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateModels['start_at'][countDown.id]"
                color="green"
                ampm-in-title
                scrollable
              ></v-date-picker>
              <v-row dense align="center" justify="space-around">
                <v-col cols="2">
                  <v-btn
                    color="green"
                    small
                    rounded
                    @click="saveDate('start_at', countDown); $set(showStartDateMenu, idx, false)"
                  >OK</v-btn>
                </v-col>
                <v-col cols="3">
                  <v-btn color="red" text @click="$set(showStartDateMenu, idx, false)">Cancel</v-btn>
                </v-col>
              </v-row>
            </v-menu>
          </v-col>
          <v-col cols="3">
            <v-menu
              ref="endDatePicker"
              v-model="showEndDateMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  v-model="countDown.end_at"
                  label="End"
                  prepend-icon="mdi-clock-outline"
                  readonly
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="countDown.end_at" color="red" ampm-in-title scrollable></v-date-picker>
              <v-row dense align="center" justify="space-around">
                <v-col cols="2">
                  <v-btn
                    color="green"
                    small
                    rounded
                    @click="save(countDown); $set(showEndDateMenu, idx, false)"
                  >OK</v-btn>
                </v-col>
                <v-col cols="3">
                  <v-btn color="red" text @click="$set(showEndDateMenu, idx, false)">Cancel</v-btn>
                </v-col>
              </v-row>
            </v-menu>
          </v-col>
          <v-col>Space For Rent</v-col>
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

  // computed: {
  //   loggedAt: {
  //     get: function () {
  //       return Format.formatDate(this.logEntry.logged_at * 1000, 'YYYY-MM-DD')
  //     },

  //     set: function (newDate) {
  //       this.logEntry.logged_at = Moment(newDate, 'YYYY-MM-DD').unix().utc()
  //     }
  //   }
  // },

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
      var qs = `page=${this.page}&pp=${this.perPage}`

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
            self.initDate('start_at', cd)
            self.initDate('end_at', cd)
          })
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    newCountDown: function () {
      alert('New CountDown')
    },

    initDate: function (type, countDown) {
      this.$set(this.dateModels[type], countDown.id, Format.formatDate(countDown[type] * 1000, 'YYYY-MM-DD'))
      // this.dateModels[type][index] = Format.formatDate(countDown[type] * 1000, 'YYYY-MM-DD')
    },

    saveDate: function (type, countDown) {
      countDown[type] = Moment(this.dateModels[type][countDown.id], 'YYYY-MM-DD').unix()

      console.log(`T: ${type} | I: ${countDown.id} | V: ${countDown[type]}`)

      this.save(countDown)
    },

    save: function (countDown) {
      console.log(countDown)

      this.$http.put(`http://127.0.0.1:4242/count_downs/${countDown.id}`, countDown)
        .then(resp => {})
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
      countDown: {},
      countDowns: [],
      page: 1,
      perPage: 15,
      totalCountDowns: 0,
      format: Format,
      searchText: null,
      dateModels: { start_at: [], end_at: [] },
      showStartDateMenu: [],
      showEndDateMenu: []
    }
  }
}
</script>
