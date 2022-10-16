<template>
  <div>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >PTO {{ currYear }}
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ pto.length }})</span
        >
        <v-btn icon x-small @click="refresh()"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
        <v-btn icon x-small @click="newPTO()"><v-icon>mdi-plus</v-icon></v-btn>

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

      <v-virtual-scroll :items="pto" item-height="50" :height="listHeight">
        <template v-slot:default="{ index, item }">
          <v-list-item dense :class="rowColor(item, index)">
            <v-list-item-avatar>
              <template v-if="item.accrual">
                <v-tooltip top>
                  <template v-slot:activator="{ on }">
                    <v-badge color="green" offset-x="10" offset-y="10" dot>
                      <v-icon left v-on="on"> {{ displayIcon(item) }} </v-icon>
                    </v-badge>
                  </template>
                  <span>{{ displayAccrual(item) }}</span>
                </v-tooltip>
              </template>
              <template v-else>
                <v-icon left> {{ displayIcon(item) }} </v-icon>
              </template>
            </v-list-item-avatar>
            <v-row dense no-gutters>
              <v-col cols="2">
                <v-list-item-content>
                  <v-list-item-title
                    :class="
                      item.isDeleted() ? 'text-decoration-line-through' : ''
                    "
                    >{{ item.type }}</v-list-item-title
                  >
                  <v-list-item-subtitle
                    :class="
                      item.isDeleted() ? 'text-decoration-line-through' : ''
                    "
                    >{{ displayBalance(item) }}</v-list-item-subtitle
                  >
                </v-list-item-content>
              </v-col>
              <v-col cols="9">
                <v-list-item-content>
                  <v-progress-linear
                    striped
                    rounded
                    :color="displayColor(item)"
                    height="25"
                    :value="progressValue(item)"
                  >
                    <template v-slot:default="{}">
                      {{ item.used }} / {{ item.available() }} hrs
                    </template>
                  </v-progress-linear>
                </v-list-item-content>
              </v-col>
              <v-col cols="1"></v-col>
            </v-row>
            <v-list-item-action>
              <v-row no-gutters>
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
    <PTOEditor
      v-model="showEditor"
      v-bind:pto="currentPTO"
      v-on:close="closeEditor"
    ></PTOEditor>
  </div>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Actions from '../Shared/Actions'

import constants from '../../lib/constants'
import Icon from '../../lib/Icon'
import notification from '../../lib/notification'
import utils from '../../lib/utils'

import PTO from '../../models/PTO'
import WorkDay from '../../models/WorkDay'
import PTOEditor from './PTOEditor.vue'

export default {
  name: 'timeoff-personal',
  components: { Actions, PTOEditor },

  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+t', 'command+t'], () => {
        self.newPTO()
        return false
      })
    },

    rowColor: function (pto, index) {
      return utils.rowColor(index)
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
        year: this.currYear,
        sort_by: 'type'
      }

      PTO.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalPTO = total
            self.pto = items
          },
          onError: (err) => { notification.error(`PTO.Personal.load: ${err.toString()}`) }
        }
      })
    },

    newPTO: function () {
      this.currentPTO = new PTO({
        year: Moment().year(),
        starting_balance: 0.0,
        accrual: { rate: null, period: null }
      })
      this.showEditor = true
    },

    edit: function (pto) {
      this.currentPTO = pto
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    gotoYear: function (offset) {
      if (offset === 0) {
        this.currYear = Moment().year()
      } else {
        this.currYear += offset
      }

      this.refresh()
    },

    duplicate: function (pto) {
      const dup = new PTO(pto)
      dup.id = null
      dup.created_at = null
      dup.year = pto.year + 1

      dup.exists(['type', 'year'], {
        handlers: {
          onSuccess: (exists) => {
            if (!exists) {
              dup.save({
                handlers: {
                  onSuccess: (_) => {
                    notification.info(`'${pto.type}' for ${pto.year} duplicated to '${dup.type}' for ${dup.year}`)
                  }
                }
              })
            } else {
              notification.warn(`'${dup.type}' for ${dup.year} already exists`)
            }
          },
          onError: (err) => {
            notification.error(`PTO.Personal.duplicate: ${err.toString()}`)
          }
        }
      })
    },

    progressValue: function (pto) {
      let percent = 0

      if (pto.available() > 0.0) {
        percent = (pto.used / pto.available()) * 100
      }

      return percent
    },

    displayIcon: function (pto) {
      let icon = pto.icon()
      if (pto.isDeleted()) {
        icon = Icon.get('deleted')
      }
      return icon
    },

    displayColor: function (pto) {
      let color = WorkDay.color(pto.type.toLowerCase())

      if (pto.isDeleted()) {
        color = 'grey'
      }

      return color
    },

    displayAccrual: function (pto) {
      let accrual = 'Does Not Accrue'
      if (pto.accrual) {
        accrual = `${pto.accrual.rate} hrs / ${pto.accrual.period} month`
      }

      return accrual
    },

    displayBalance: function (pto) {
      const asDays = pto.balance() / WorkDay.HOURS_PER_DAY
      return `${Math.round(asDays)} days (${pto.balance()}h)`
    }
  },

  data () {
    return {
      page: 1,
      perPage: 25,
      totalPTO: 0,
      pto: [],
      listHeight: Math.round(window.innerHeight * 0.25),
      currentPTO: new PTO({ accrual: null }),
      currYear: Moment().year(),
      searchText: null,
      showEditor: false,
      constants: constants,
      icon: Icon
    }
  }
}
</script>
