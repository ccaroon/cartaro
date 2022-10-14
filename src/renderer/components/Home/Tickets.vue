<template>
  <v-sheet>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Tickets
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ tickets.length }})</span
        >
        <v-btn icon x-small @click="loadTickets()"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
      </v-card-title>

      <v-virtual-scroll :items="tickets" item-height="40" :height="listHeight">
        <template v-slot:default="{ index, item }">
          <v-list-item :class="utils.rowColor(index)" dense>
            <v-list-item-icon>
              <v-icon :color="item.color()">{{ item.icon() }}</v-icon>
              <span
                style="cursor: pointer"
                class="blue--text"
                @click="utils.openLink(item.link)"
              >
                {{ item.key }}
                <v-icon x-small color="blue">mdi-open-in-new</v-icon>
              </span>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title :class="textWeight(item)">
                {{ item.summary }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </v-sheet>
</template>
<script>
import Constants from '../../lib/Constants'
import Notification from '../../lib/Notification'
import Utils from '../../lib/Utils'
import JiraTicket from '../../models/JiraTicket'

export default {
  name: 'home-tickets',
  components: {},

  mounted: function () {
    this.loadTickets()
  },

  methods: {
    loadTickets: function () {
      const self = this

      JiraTicket.fetch({}, '/search', {
        handlers: {
          onSuccess: (items) => {
            self.tickets = items
          },
          onError: (err) => { Notification.error(`HM.Tickts.loadTickets: ${err}`) }
        }
      })
    },

    textWeight: function (ticket) {
      let textClass = 'text--primary'

      if (ticket.status === 'Closed') {
        textClass = 'text-decoration-line-through'
      } else if (ticket.status === 'Blocked') {
        textClass = 'text--disabled'
      }
      return textClass
    }
  },

  data () {
    return {
      tickets: [],
      listHeight: Math.round(window.innerHeight * 0.25),
      constants: Constants,
      utils: Utils
    }
  }
}
</script>
