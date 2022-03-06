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
        <v-btn icon x-small @click="duplicateYear()"
          ><v-icon>mdi-content-duplicate</v-icon></v-btn
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

      <v-virtual-scroll :items="holidays" item-height="55" height="450">
        <template v-slot:default="{ index, item }">
          <v-list-item dense :class="rowColor(item, index)">
            <v-list-item-avatar>
              <v-icon v-if="item.isPast()" color="green">{{
                icon.get("marked off")
              }}</v-icon>
              <v-icon v-else-if="item.isDeleted()" color="red">{{
                icon.get("deleted")
              }}</v-icon>
              <v-icon v-else>{{ item.icon() }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                :class="
                  item.isDeleted() || item.isPast()
                    ? 'text-decoration-line-through'
                    : ''
                "
                >{{ item.name }}</v-list-item-title
              >
              <v-list-item-subtitle>{{
                format.humanizeDate(item.date * 1000)
              }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-content>
              <v-list-item-title
                :class="
                  item.isDeleted() || item.isPast()
                    ? 'text-decoration-line-through'
                    : ''
                "
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
import Icon from '../../lib/Icon'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'

import Holiday from '../../models/Holiday'
import WorkDay from '../../models/WorkDay'

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

      Mousetrap.bind(['ctrl+h', 'command+h'], () => {
        self.newHoliday()
        return false
      })
    },

    rowColor: function (holiday, index) {
      return Utils.rowColor(index, holiday.thisMonth())
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
      const workDay = new WorkDay({
        type: 'holiday',
        date: holiday.date,
        time_in: '00:00',
        time_out: '00:00',
        note: holiday.name
      })

      const query = {
        pp: 5,
        op: 'and',
        date: holiday.date,
        note: holiday.name
      }

      // TODO: re-write to use workday.exists()
      // Check to see if entry already exists
      WorkDay.fetch(query, '/', {
        handlers: {
          onSuccess: function (_, totalCount) {
            if (totalCount > 0) {
              Notification.warn(`'${holiday.name}' already exists on WorkDay Calendar.`)
            } else {
              // If not, add it
              workDay.save({
                handlers: {
                  onSuccess: (_) => {
                    Notification.info(`'${holiday.name}' added to WorkDay Calendar.`)
                  },
                  onError: (err) => {
                    Notification.error(`PTO.Holidays.addToCalendar#save: ${err.toString()}`)
                  }
                }
              })
            }
          },
          onError: (err) => {
            Notification.error(`PTO.Holidays.addToCalendar#fetch: ${err.toString()}`)
          }
        }
      })
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

      dup.exists(['date', 'name'], {
        handlers: {
          onSuccess: (exists) => {
            if (!exists) {
              this.save(dup, false, `${holiday.name} duplicated to ${this.displayDate(dup)}`)
            } else {
              Notification.warn(`'${holiday.name}' already exists for ${this.displayDate(dup)}`)
            }
          },
          onError: (err) => {
            Notification.error(`PTO.Holidays.duplicate: ${err.toString()}`)
          }
        }
      })
    },

    duplicateYear: function () {
      // const self = this

      alert('Not Yet Implemented!')
      // TODO: saves to fast. need to wrap in promises
      // this.holidays.forEach((holiday) => {
      //   self.duplicate(holiday)
      // })
    },

    edit: function (item) {
      this.holiday = item
      this.showEditor = true
    },

    newHoliday: function () {
      this.holiday = new Holiday({
        name: '',
        date: Moment().startOf('day').unix(),
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
        holiday.date = Moment(`${holiday.targetDate}`, Constants.FORMATS.dateOnly).startOf('day').unix()
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

              // If new holiday, auto-add to WD calendar
              if (!holiday.id) {
                self.addToCalendar(holiday)
              }

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
      perPage: 50,
      totalHolidays: 0,
      searchText: null,
      showEditor: false,
      showDateMenu: false,
      constants: Constants,
      format: Format,
      icon: Icon,
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
