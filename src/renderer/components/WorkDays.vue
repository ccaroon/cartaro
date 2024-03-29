<template>
  <v-container fluid>
    <AppBar
      v-bind:name="'Work Days'"
      v-bind:buttons="appBarButtons"
      @refresh="refresh"
    ></AppBar>

    <v-sheet tile class="d-flex">
      <v-row>
        <v-col offset="4" cols="1" align="end">
          <v-btn icon @click="$refs.calendar.prev()">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn icon @click="goToToday()">
            <v-icon>mdi-calendar-today</v-icon>
          </v-btn>
          <v-btn icon @click="$refs.calendar.next()">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="3" align="start">
          <span class="text-h4">{{
            format.formatDate(calDate, "MMMM YYYY")
          }}</span>
        </v-col>
      </v-row>
    </v-sheet>
    <v-sheet :height="calHeight">
      <v-calendar
        ref="calendar"
        v-model="calDate"
        color="grey"
        event-text-color="black"
        :event-more="false"
        :events="events"
        @click:event="showEditor"
        @click:date="addDay"
      >
      </v-calendar>
      <v-menu
        v-model="editorOpen"
        :close-on-content-click="false"
        :activator="eventElement"
      >
        <v-card>
          <v-toolbar :color="selectedWorkDay.color('accent')" dense>
            <v-btn-toggle
              v-model="selectedWorkDay.type"
              dense
              borderless
              :background-color="selectedWorkDay.color('accent')"
              mandatory
              @change="changeType(selectedWorkDay)"
            >
              <v-btn icon small value="normal">
                <v-icon>{{ icons.get("workday") }}</v-icon>
              </v-btn>
              <v-btn icon small value="holiday">
                <v-icon>{{ icons.get("holiday") }}</v-icon>
              </v-btn>
              <v-btn icon small value="vacation">
                <v-icon>{{ icons.get("vacation") }}</v-icon>
              </v-btn>
              <v-btn icon small value="sick">
                <v-icon>{{ icons.get("sick") }}</v-icon>
              </v-btn>
            </v-btn-toggle>
            <v-spacer></v-spacer>
            <v-toolbar-title>{{
              format.formatDate(selectedWorkDay.date * 1000)
            }}</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-menu
              ref="timeInPicker"
              v-model="showTimeInMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-x
              min-width="290px"
              max-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-btn fab x-small color="green" v-on="on">{{
                  selectedWorkDay.time_in
                }}</v-btn>
              </template>
              <v-time-picker
                v-model="selectedWorkDay.time_in"
                color="green"
                ampm-in-title
                scrollable
              >
                <v-btn
                  color="green"
                  small
                  rounded
                  @click="
                    save(selectedWorkDay);
                    showTimeInMenu = false;
                  "
                  >OK</v-btn
                >
                <v-btn color="red" text @click="showTimeInMenu = false"
                  >Cancel</v-btn
                >
              </v-time-picker>
            </v-menu>
            <v-menu
              ref="timeOutPicker"
              v-model="showTimeOutMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-x
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on }">
                <v-btn fab x-small color="red" v-on="on">{{
                  selectedWorkDay.time_out
                }}</v-btn>
              </template>
              <v-time-picker
                v-model="selectedWorkDay.time_out"
                color="red"
                ampm-in-title
                scrollable
              >
                <v-btn
                  color="green"
                  small
                  rounded
                  @click="
                    save(selectedWorkDay);
                    showTimeOutMenu = false;
                  "
                  >OK</v-btn
                >
                <v-btn color="red" text @click="showTimeOutMenu = false"
                  >Cancel</v-btn
                >
              </v-time-picker>
            </v-menu>
          </v-toolbar>
          <v-card-text>
            <v-text-field
              v-model="selectedWorkDay.note"
              placeholder="Note"
              @change="save(selectedWorkDay)"
            >
            </v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              color="red"
              @click="
                remove(selectedWorkDay);
                editorOpen = false;
              "
            >
              Delete
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="green" @click="editorOpen = false"> Close </v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-sheet>

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

import format from '../lib/format'
import Icon from '../lib/Icon'
import notification from '../lib/notification'

import AppBar from './Shared/AppBar'

import WorkDay from '../models/WorkDay'

const DAYS_PER_MONTH = 31

export default {
  name: 'work-days-main',
  components: { AppBar },
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

    displayWorkDates: function () {
      let dateStr = ''
      const start = format.formatDate(this.weekStart, 'MMM DD, YYYY')
      const end = format.formatDate(this.weekEnd, 'MMM DD, YYYY')

      dateStr = `${start} to ${end}`

      return dateStr
    },

    displayYearWeek: function () {
      return `Week ${format.formatDate(new Date(), 'WW')}`
    },

    goToToday: function () {
      this.calDate = format.formatDate(new Date(), 'YYYY-MM-DD')
    },

    totalHours: function () {
      let total = 0
      this.workDays.forEach(workDay => {
        const day = Moment(workDay.date * 1000)
        if (day.isBetween(this.weekStart, this.weekEnd)) {
          const duration = workDay.hoursWorked()
          total += duration.asHours()
        }
      })

      return total.toFixed(1)
    },

    refresh: function (opts = {}) {
      this.load()
    },

    load: function () {
      this.loadMonth()
    },

    addDay: function (dateEvent) {
      const self = this
      this.newDay(Moment(dateEvent.date), 'EDIT ME')
        .then(() => {
          self.refresh()
        })
        .catch((err) => {
          notification.error(`WD.Main.addDay: ${err.toString()}`)
        })
    },

    showEditor: function (event) {
      this.selectedWorkDay = event.event.workDay
      this.eventElement = event.nativeEvent.target
      // Dunno. Makes it open attached to the correct element
      requestAnimationFrame(() => requestAnimationFrame(() => { this.editorOpen = true }))
    },

    createEvents: function (days) {
      const events = []
      days.forEach((day) => {
        let name = day.typeCode(true)
        if (day.note) {
          name += ` ${day.note}`
        }

        events.push({
          name,
          start: day.start().toDate(),
          end: day.end().toDate(),
          color: day.color('accent'),
          timed: !day.allDay(),
          workDay: day
        })
      })

      return events
    },

    loadMonth: function () {
      const self = this
      const query = {
        pp: DAYS_PER_MONTH,
        start: format.formatDate(Moment(this.calDate).startOf('month'), 'YYYY-MM-DD'),
        days: DAYS_PER_MONTH
      }

      WorkDay.fetch(query, '/range', {
        handlers: {
          onSuccess: function (days, totalCount) {
            self.workDays = days
            self.events = self.createEvents(days)
          },
          onError: (err) => {
            notification.error(`WD.Main.loadMonth: ${err.toString()}`)
          }
        }
      })
    },

    newDay: function (day = Moment().startOf('week').add(1, 'day'), note = null) {
      const workDay = new WorkDay({
        date: day.unix(),
        time_in: WorkDay.DEFAULT_IN,
        time_out: WorkDay.DEFAULT_OUT,
        note,
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
          onSuccess: () => {
            this.refresh()
          },
          onError: (err) => notification.error(`WD.Main.save: ${err.toString()}`)
        }
      })
    },

    remove: function (workDay) {
      const self = this

      workDay.delete({
        safe: 0,
        handlers: {
          onSuccess: () => {
            self.refresh()
          },
          onError: (err) => { notification.error(`WD.Main.delete: ${err.toString()}`) }
        }
      })
    }
  },

  watch: {
    calDate: function (newDate, oldDate) {
      if (!Moment(oldDate).isSame(newDate, 'month')) {
        this.refresh()
      }
    }
  },

  data () {
    return {
      calDate: format.formatDate(new Date(), 'YYYY-MM-DD'),
      weekStart: Moment().startOf('week'),
      weekEnd: Moment().endOf('week'),
      events: [],
      editorOpen: false,
      selectedWorkDay: new WorkDay({ type: WorkDay.TYPE_NORMAL }),
      eventElement: null,
      workDays: [],
      format: format,
      icons: Icon,
      showTimeInMenu: false,
      showTimeOutMenu: false,
      calHeight: Math.round(window.innerHeight * 0.85),
      appBarButtons: [
        { name: 'New Week', icon: 'mdi-calendar-plus', action: this.newWeek }
      ]
    }
  }
}
</script>
