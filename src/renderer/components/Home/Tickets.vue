<template>
  <v-sheet>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Tickets
        <v-btn icon x-small @click="loadTickets"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
      </v-card-title>

      <v-virtual-scroll :items="tickets" item-height="40" height="180">
        <template v-slot:default="{ index, item }">
          <v-list-item :class="utils.rowColor(index)" dense>
            <v-list-item-icon>
              <v-icon :color="iconColor(item)"
                >mdi-{{
                  constants.ICONS.tickets[item.type.toLowerCase()]
                }}</v-icon
              >
              <span
                style="cursor: pointer"
                class="blue--text"
                @click="utils.openLink('Jira', item.link)"
              >
                {{ item.key }}
                <v-icon x-small color="blue">mdi-open-in-new</v-icon>
              </span>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                :class="
                  item.status === 'Closed' ? 'text-decoration-line-through' : ''
                "
              >
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

export default {
  name: 'home-tickets',
  components: {},

  mounted: function () {
    this.loadTickets()
  },

  methods: {
    loadTickets: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/jira/search`)
        .then(resp => {
          self.tickets = resp.data.results
        })
        .catch(err => {
          Notification.error(`HM.Tickts.loadTickets: ${err}`)
        })
    },

    iconColor: function (ticket) {
      var color = 'blue'
      if (ticket.status === 'In Progress') {
        color = 'green'
      } else if (ticket.status === 'Closed') {
        color = 'red'
      }

      return color
    }
  },

  data () {
    return {
      tickets: [],
      constants: Constants,
      utils: Utils
    }
  }
}
</script>
