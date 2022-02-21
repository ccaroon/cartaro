<template>
  <div>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >PTO Balances {{ currYear }}
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

      <v-virtual-scroll :items="pto" item-height="55" height="300">
        <template v-slot:default="{ index, item }">
          <v-list-item dense :class="rowColor(item, index)">
            <v-list-item-avatar>
              <v-icon v-if="item.isDeleted()" color="red">{{
                icon.get("deleted")
              }}</v-icon>
              <v-icon v-else>{{ item.icon() }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                :class="item.isDeleted() ? 'text-decoration-line-through' : ''"
                >{{ item.type }}</v-list-item-title
              >
              <v-list-item-subtitle>{{
                displayAccrual(item)
              }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-content>
              <v-list-item-title
                :class="item.isDeleted() ? 'text-decoration-line-through' : ''"
              >
                Balance
              </v-list-item-title>
              <v-list-item-subtitle
                :class="item.isDeleted() ? 'text-decoration-line-through' : ''"
              >
                {{ displayBalance(item) }}
              </v-list-item-subtitle>
            </v-list-item-content>
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
  </div>
</template>
<script>
import Moment from 'moment'

import Actions from '../Shared/Actions'

import Constants from '../../lib/Constants'
import Icon from '../../lib/Icon'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'

import PTO from '../../models/PTO'

export default {
  name: 'timeoff-personal',
  components: { Actions },

  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      // const self = this

      // TODO: keep this?
      // Mousetrap.bind(['ctrl+N', 'command+N'], () => {
      //   self.newPTO()
      //   return false
      // })
    },

    rowColor: function (pto, index) {
      return Utils.rowColor(index)
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
          onError: (err) => { Notification.error(`PTO.Personal.load: ${err.toString()}`) }
        }
      })
    },

    newPTO: function () {

    },

    edit: function () {

    },

    duplicate: function () {

    },

    gotoYear: function (offset) {
      if (offset === 0) {
        this.currYear = Moment().year()
      } else {
        this.currYear += offset
      }

      this.refresh()
    },

    displayAccrual: function (pto) {
      let accrual = 'Does Not Accrue'
      if (pto.accrual) {
        accrual = `${pto.accrual.rate} hours / ${pto.accrual.period} month`
      }

      return accrual
    },

    displayBalance: function (pto) {
      return `${pto.used()} / ${pto.available()}`
    }
  },

  data () {
    return {
      page: 1,
      perPage: 10,
      totalPTO: 0,
      pto: [],
      currYear: Moment().year(),
      searchText: null,
      constants: Constants,
      icon: Icon
    }
  }
}
</script>
