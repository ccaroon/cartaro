<template>
  <v-container>
    <v-list dense>
      <v-list-item
        v-for="(holiday, idx) in holidays"
        :key="holiday.id"
        :class="utils.rowColor(idx)"
      >
        <v-list-item-avatar>
          <v-icon>{{ holiday.icon() }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ holiday.name }}</v-list-item-title>
          <v-list-item-subtitle>{{
            format.humanizeDate(holiday.date * 1000)
          }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-content>
          <v-list-item-title>
            {{ displayDate(holiday) }}
          </v-list-item-title>
        </v-list-item-content>

        <v-list-item-icon>
          <v-icon>mdi-calendar-icon</v-icon>
        </v-list-item-icon>
      </v-list-item>
    </v-list>
    <div class="text-center">
      <v-bottom-sheet v-model="showEditor">
        <v-card>
          <v-form ref="newEditForm">
            <v-row>
              <v-col>
                <v-text-field
                  v-model="holiday.name"
                  label="Name"
                  autofocus
                  prepend-icon="mdi-label"
                  require
                  :rules="rules.name"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-menu
                  ref="datePicker"
                  v-model="showDateMenu"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      label="Date"
                      prepend-icon="mdi-calendar-month"
                      readonly
                      :value="holiday.targetDate"
                      v-on="on"
                      required
                      :rules="rules.date"
                    ></v-text-field>
                  </template>
                  <v-sheet>
                    <v-row dense>
                      <v-col>
                        <v-date-picker
                          v-model="holiday.targetDate"
                          color="blue"
                          flat
                        ></v-date-picker>
                      </v-col>
                    </v-row>
                    <v-row dense align="center" justify="center">
                      <v-col>
                        <v-btn
                          rounded
                          color="green"
                          @click="showDateMenu = false"
                          >OK</v-btn
                        >
                        <v-btn
                          rounded
                          color="blue"
                          @click="
                            holiday.date = Date.now() / 1000;
                            initDate(holiday);
                          "
                          >Today</v-btn
                        >
                        <v-btn text color="red" @click="showDateMenu = false"
                          >Cancel</v-btn
                        >
                      </v-col>
                    </v-row>
                  </v-sheet>
                </v-menu>
              </v-col>

              <v-col cols="1" text-center>
                <v-btn fab color="success" small @click="save(holiday)">
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

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'

import Holiday from '../../models/Holiday'

// import Actions from './Shared/Actions'
// import AppBar from './Shared/AppBar'

export default {
  name: 'timeoff-holidays',
  components: { },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newHoliday()
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
      const startOfYear = Moment().startOf('year')
      const query = {
        page: this.page,
        pp: this.perPage,
        date: `gte:${startOfYear.unix()}`,
        sort_by: 'date'
      }

      Holiday.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalHolidays = total
            self.holidays = items

            self.holidays.forEach((hd) => {
              self.initDate(hd)
            })
          },
          onError: (err) => { Notification.error(`PTO.Holidays.load: ${err.toString()}`) }
        }
      })
    },

    edit: function (item) {
      this.holiday = item
      this.showEditor = true
    },

    newHoliday: function () {
      this.holiday = new Holiday({
        name: '',
        date: Moment().unix(),
        deleted_at: null
      })
      this.initDate(this.holiday)

      this.showEditor = true
    },

    // Init dates for use with date-picker / time-picker
    initDate: function (holiday) {
      this.$set(holiday, 'targetDate', Format.formatDate(
        holiday.date * 1000, Constants.FORMATS.dateOnly
      ))
    },

    displayDate: function (holiday) {
      return Format.formatDate(holiday.date * 1000)
    },

    save: function (holiday, validate = true) {
      const self = this
      holiday.date = Moment(`${holiday.targetDate}`, Constants.FORMATS.dateOnly).unix()

      let doSave = true
      if (validate) {
        doSave = this.$refs.newEditForm.validate()
      }

      if (doSave) {
        holiday.save({
          handlers: {
            onSuccess: () => {
              this.showEditor = false
              self.initDate(holiday)
              self.load()
            },
            onError: (err) => { Notification.error(`PTO.Holidays.save: ${err.toString()}`) }
          }
        })
      }
    }
  },

  data () {
    return {
      holiday: new Holiday({}),
      holidays: [],
      page: 1,
      perPage: 15,
      totalHolidays: 0,
      searchText: null,
      showEditor: false,
      showDateMenu: false,
      constants: Constants,
      format: Format,
      utils: Utils,
      rules: {
        name: [
          name => !!name || 'Name is required'
        ],
        date: [
          date => !!date || 'Date is required',
          date => (Moment(date, Constants.FORMATS.dateOnly, true).isValid()) || 'Format as ' + Constants.FORMATS.dateOnly
        ]
      }
    }
  }
}
</script>
