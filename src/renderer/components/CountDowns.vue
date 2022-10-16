<template>
  <v-container>
    <AppBar v-bind:name="'Countdowns'" v-bind:numPages="Math.ceil(totalCountDowns / perPage)" v-bind:refresh="refresh"
      v-bind:buttons="appBarButtons"></AppBar>
    <v-list dense>
      <v-list-item v-for="(countDown, idx) in countDowns" :key="countDown.id" :class="utils.rowColor(idx)">
        <v-list-item-avatar v-if="!countDown.isDeleted()">
          <v-btn icon @click="toggleFavorite(countDown)">
            <v-icon :color="countDown.is_favorite ? 'yellow' : ''">{{
            countDown.icon()
            }}</v-icon>
          </v-btn>
        </v-list-item-avatar>
        <v-list-item-avatar v-else>
          <v-icon color="red">{{ icon.get("deleted") }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title :class="countDown.isDeleted() ? 'text-decoration-line-through' : ''">{{ countDown.name }}
          </v-list-item-title>
          <v-list-item-subtitle>{{
          countDown.humanize()
          }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-content>
          <v-list-item-title> Start </v-list-item-title>
          <v-list-item-subtitle>{{
          dateDisplay(countDown, "start")
          }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-content>
          <template v-if="countDown.end_at">
            <v-list-item-title> End </v-list-item-title>
            <v-list-item-subtitle>
              {{ dateDisplay(countDown, "end") }}
            </v-list-item-subtitle>
          </template>
        </v-list-item-content>

        <Actions v-bind:actions="{
          onEdit: (item) => {
            edit(item);
          },
          onArchiveDelete: (event, item) => {
            if (event.startsWith('post-')) {
              refresh();
            }
          },
        }" v-bind:item="countDown"></Actions>
      </v-list-item>
    </v-list>
    <div class="text-center">
      <v-bottom-sheet v-model="showEditor">
        <v-card>
          <v-form ref="newEditForm">
            <v-row>
              <v-col>
                <v-text-field v-model="countDown.name" label="Name" autofocus prepend-icon="mdi-label" require
                  :rules="rules.name"></v-text-field>
              </v-col>
              <v-col>
                <v-menu ref="startDatePicker" v-model="showStartDateMenu" :close-on-content-click="false"
                  :nudge-right="40" transition="scale-transition" offset-y>
                  <template v-slot:activator="{ on }">
                    <v-text-field label="Start" prepend-icon="mdi-calendar-clock" readonly
                      :value="dateDisplay(countDown, 'start')" v-on="on" required :rules="rules.date"></v-text-field>
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
                        <v-btn rounded color="green" @click="showStartDateMenu = false">OK</v-btn>
                      </v-col>
                      <v-col cols="3">
                        <v-btn rounded color="blue" @click="
                          countDown.start_at = Date.now() / 1000;
                          initDate(countDown);
                        ">Today</v-btn>
                      </v-col>
                      <v-col cols="3">
                        <v-btn text color="red" @click="showStartDateMenu = false">Cancel</v-btn>
                      </v-col>
                    </v-row>
                  </v-sheet>
                </v-menu>
              </v-col>
              <v-col>
                <v-menu ref="endDatePicker" v-model="showEndDateMenu" :close-on-content-click="false" :nudge-right="40"
                  transition="scale-transition" offset-y>
                  <template v-slot:activator="{ on }">
                    <v-text-field label="End" prepend-icon="mdi-calendar-clock" readonly clearable
                      @click:clear="clearEndDate(countDown)" :value="dateDisplay(countDown, 'end')" v-on="on">
                    </v-text-field>
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
                        <v-btn rounded color="green" @click="showEndDateMenu = false">OK</v-btn>
                      </v-col>
                      <v-col cols="3">
                        <v-btn rounded color="blue" @click="
                          countDown.end_at = Date.now() / 1000;
                          initDate(countDown);
                        ">Today</v-btn>
                      </v-col>
                      <v-col cols="3">
                        <v-btn text color="red" @click="showEndDateMenu = false">Cancel</v-btn>
                      </v-col>
                    </v-row>
                  </v-sheet>
                </v-menu>
              </v-col>
              <v-col cols="1" text-center>
                <v-btn fab color="success" small @click="save(countDown)">
                  <v-icon>mdi-content-save</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-bottom-sheet>
    </div>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import constants from '../lib/constants'
import format from '../lib/format'
import Icon from '../lib/Icon'
import notification from '../lib/notification'
import utils from '../lib/utils'

import Countdown from '../models/Countdown'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'

export default {
  name: 'countdowns-main',
  components: { Actions, AppBar },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newCountDown()
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
      const self = this
      const query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'start_at'
      }

      if (this.searchText) {
        const parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          query[parts[0].trim()] = parts[1].trim()
        } else {
          query.name = this.searchText
        }
      }

      Countdown.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalCountDowns = total
            self.countDowns = items

            self.countDowns.forEach((cd) => {
              self.initDate(cd)
            })
          },
          onError: (err) => { notification.error(`CD.Main.load: ${err.toString()}`) }
        }
      })
    },

    edit: function (item) {
      this.countDown = item
      this.showEditor = true
    },

    newCountDown: function () {
      this.countDown = new Countdown({
        name: '',
        start_at: Moment().unix(),
        end_at: null,
        deleted_at: null
      })
      this.initDate(this.countDown)

      this.showEditor = true
    },

    dateDisplay: function (countDown, type) {
      let asString = ''
      const dateAttr = `${type}Date`
      const timeAttr = `${type}Time`

      if (countDown[dateAttr] && countDown[timeAttr]) {
        asString = countDown[dateAttr] + ' @ ' + countDown[timeAttr]
      }

      return asString
    },

    // Init dates for use with date-picker / time-picker
    initDate: function (countDown) {
      this.$set(countDown, 'startDate', format.formatDate(countDown.start_at * 1000, 'YYYY-MM-DD'))
      this.$set(countDown, 'startTime', format.formatDate(countDown.start_at * 1000, 'HH:mm'))

      let endDate = null
      let endTime = null
      if (countDown.end_at) {
        endDate = format.formatDate(countDown.end_at * 1000, 'YYYY-MM-DD')
        endTime = format.formatDate(countDown.end_at * 1000, 'HH:mm')
      }

      this.$set(countDown, 'endDate', endDate)
      this.$set(countDown, 'endTime', endTime)
    },

    clearEndDate: function (countDown) {
      countDown.endDate = null
      countDown.endTime = null
    },

    toggleFavorite: function (countDown) {
      countDown.toggleFavorite()
      this.save(countDown, false)
    },

    save: function (countDown, validate = true) {
      const self = this
      countDown.start_at = Moment(`${countDown.startDate} ${countDown.startTime}`, 'YYYY-MM-DD HH:mm:ss').unix()

      if (countDown.endDate && countDown.endTime) {
        countDown.end_at = Moment(`${countDown.endDate} ${countDown.endTime}`, 'YYYY-MM-DD HH:mm:ss').unix()
      } else {
        countDown.end_at = null
      }

      let doSave = true
      if (validate) {
        doSave = this.$refs.newEditForm.validate()
      }

      if (doSave) {
        countDown.save({
          handlers: {
            onSuccess: () => {
              this.showEditor = false
              self.load()
            },
            onError: (err) => { notification.error(`CD.Main.save: ${err.toString()}`) }
          }
        })
      }
    }
  },

  data () {
    const itemHeight = 65

    return {
      countDown: new Countdown({}),
      countDowns: [],
      page: 1,
      perPage: Math.round(window.innerHeight / itemHeight) - 1,
      totalCountDowns: 0,
      format: format,
      icon: Icon,
      utils: utils,
      searchText: null,
      showEditor: false,
      showStartDateMenu: false,
      showStartTimeMenu: false,
      showEndDateMenu: false,
      showEndTimeMenu: false,
      appBarButtons: [
        { name: 'New', icon: 'mdi-alarm-plus', action: this.newCountDown }
      ],
      rules: {
        name: [
          name => !!name || 'Name is required'
        ],
        date: [
          date => !!date || 'Date is required',
          date => (Moment(date, constants.FORMATS.countDownDate, true).isValid()) || 'format as ' + constants.FORMATS.countDownDate
        ]
      }
    }
  }
}
</script>
