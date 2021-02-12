<template>
  <v-sheet>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Tickets
        <v-btn icon x-small @click="loadTickets"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
      </v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item
            v-for="(ticket, idx) in tickets"
            :key="ticket.key"
            :class="utils.rowColor(idx)"
            dense
          >
            <v-list-item-icon>
              <v-icon :color="iconColor(ticket)"
                >mdi-{{
                  constants.ICONS.tickets[ticket.type.toLowerCase()]
                }}</v-icon
              >
              <span
                style="cursor: pointer"
                class="blue--text"
                @click="utils.openLink('Jira', ticket.link)"
              >
                {{ ticket.key }}
                <v-icon x-small color="blue">mdi-open-in-new</v-icon>
              </span>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                :class="
                  ticket.status === 'Closed'
                    ? 'text-decoration-line-through'
                    : ''
                "
              >
                {{ ticket.summary }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-sheet>
</template>
<script>
import Utils from '../../lib/Utils'
import Constants from '../../lib/Constants'

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
          console.log(`${err.response.status} - ${err.response.data.error}`)
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
