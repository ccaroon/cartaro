<template>
  <div>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Holidays {{ currYear }}
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ holidays.length }})</span
        >
        <v-btn icon x-small @click="refresh()"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
        <v-btn icon x-small @click="newHoliday()"
          ><v-icon>mdi-plus</v-icon></v-btn
        >
        <v-divider vertical></v-divider>
        <v-btn icon x-small @click="gotoYear(-1)"
          ><v-icon>mdi-chevron-left</v-icon></v-btn
        >
        <v-btn icon x-small @click="gotoYear(0)"
          ><v-icon>mdi-calendar-today</v-icon></v-btn
        >
        <v-btn icon x-small @click="gotoYear(+1)"
          ><v-icon>mdi-chevron-right</v-icon></v-btn
        >
      </v-card-title>

      <v-virtual-scroll :items="holidays" item-height="55" height="400">
        <template v-slot:default="{ index, item }">
          <v-list-item dense :class="utils.rowColor(index)">
            <v-list-item-avatar>
              <v-icon>{{ item.icon() }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                :class="item.isDeleted() ? 'text-decoration-line-through' : ''"
                >{{ item.name }}</v-list-item-title
              >
              <v-list-item-subtitle>{{
                format.humanizeDate(item.date * 1000)
              }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-content>
              <v-list-item-title
                :class="item.isDeleted() ? 'text-decoration-line-through' : ''"
              >
                {{ displayDate(item) }}
              </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-row no-gutters>
                <v-col class="mr-1">
                  <v-btn
                    icon
                    outlined
                    @click="addToCalendar(item)"
                    :disabled="item.isDeleted()"
                  >
                    <v-icon>mdi-calendar-plus</v-icon>
                  </v-btn>
                </v-col>
                <v-col class="mr-1">
                  <v-btn
                    icon
                    outlined
                    @click="duplicate(item)"
                    :disabled="item.isDeleted()"
                  >
                    <v-icon>mdi-content-duplicate</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-list-item-action>
            <Actions
              v-bind:actions="{
                onEdit: (item) => {
                  edit(item);
                },
                onArchiveDelete: (event, item) => {
                  if (event.startsWith('post-')) {
                    refresh();
                  }
                },
              }"
              v-bind:item="item"
            ></Actions>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
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
  </div>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'

import Holiday from '../../models/Holiday'

import Actions from '../Shared/Actions'

export default {
  name: 'timeoff-holidays',
  components: { Actions },
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
      const start = Moment(this.currYear, 'YYYY').startOf('year')
      const end = Moment(this.currYear, 'YYYY').endOf('year')

      const query = {
        page: this.page,
        pp: this.perPage,
        date: `btw:${start.unix()}:${end.unix()}`,
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

    addToCalendar: function (holiday) {
      alert(`Add To Calender: ${holiday.name}`)
    },

    gotoYear: function (offset) {
      if (offset === 0) {
        this.currYear = Moment().year()
      } else {
        this.currYear += offset
      }

      this.refresh()
    },

    duplicate: function (holiday) {
      const dup = holiday.duplicate()
      this.save(dup, false, `${holiday.name} duplicated to ${this.displayDate(dup)}`)
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
      return Format.formatDate(holiday.date * 1000, 'ddd MMM DD, YYYY')
    },

    save: function (holiday, validate = true, successMsg = null) {
      const self = this

      if (holiday.targetDate) {
        holiday.date = Moment(`${holiday.targetDate}`, Constants.FORMATS.dateOnly).unix()
      }

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

              if (successMsg) {
                Notification.success(successMsg)
              }
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
      currYear: Moment().year(),
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
