<template>
  <v-dialog v-model="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-card-title>
        <span class="headline">LogEntry Editor</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="logEntryForm">
          <v-container>
            <v-row dense>
              <v-col cols="2">
                <v-menu
                  ref="datePicker"
                  v-model="showDateMenu"
                  :close-on-content-click="true"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="loggedAt"
                      label="Log Date"
                      readonly
                      outlined
                      dense
                      hide-details
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="loggedAt"
                    no-title
                    scrollable
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col>
                <v-text-field
                  label="Subject"
                  v-model="logEntry.subject"
                  outlined
                  dense
                  hide-details
                  :rules="rules.subject"
                  >{{ logEntry.subject }}</v-text-field
                >
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-btn-toggle
                  v-model="logEntry.category"
                  dense
                  rounded
                  mandatory
                >
                  <v-btn value="Meeting">Meeting</v-btn>
                  <v-btn value="Ticket">Ticket</v-btn>
                  <v-btn value="Operational">Operational</v-btn>
                  <v-btn value="Other">Other</v-btn>
                </v-btn-toggle>
              </v-col>
              <v-col cols="6">
                <v-select
                  v-show="logEntry.category === 'Ticket'"
                  v-model="chosenTicket"
                  :hint="`${chosenTicket ? chosenTicket.link : ''}`"
                  :items="jiraTickets"
                  item-text="summary"
                  item-value="link"
                  label="Ticket"
                  persistent-hint
                  outlined
                  dense
                  clearable
                  return-object
                  :rules="rules.ticket"
                ></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  label="Content"
                  rows="17"
                  outlined
                  hide-details
                  v-model="logEntry.content"
                  :rules="rules.content"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-combobox
                  v-model="logEntry.tags"
                  :items="allTags"
                  label="Tags"
                  outlined
                  multiple
                  dense
                  hide-details
                >
                  <template
                    v-slot:selection="{ attrs, item, select, selected }"
                  >
                    <v-chip
                      v-bind="attrs"
                      :input-value="selected"
                      close
                      small
                      @click="select"
                      @click:close="removeTag(item)"
                      >{{ item }}</v-chip
                    >
                  </template>
                </v-combobox>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-alert v-show="errorMsg" dense color="error">{{
          this.errorMsg
        }}</v-alert>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">Save</v-btn>
        <v-btn color="red" text @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Moment from 'moment'
import Format from '../../lib/Format'
import Notification from '../../lib/Notification'

export default {
  name: 'logEntry-editor',
  components: { },
  props: ['logEntry', 'value'],

  mounted: function () {
    this.loadTags()
    this.loadTickets()
  },

  computed: {
    loggedAt: {
      get: function () {
        return Format.formatDate(this.logEntry.logged_at * 1000, 'YYYY-MM-DD')
      },

      set: function (newDate) {
        this.logEntry.logged_at = Moment(newDate, 'YYYY-MM-DD').unix()
      }
    }
  },

  methods: {
    loadTickets: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/jira/search`)
        .then(resp => {
          self.jiraTickets = resp.data.results
        })
        .catch(err => {
          Notification.error(err.toString())
        })
    },

    loadTags: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/tags/`)
        .then(resp => {
          self.allTags = resp.data.tags.map(tag => tag.name)
        })
        .catch(err => {
          Notification.error(err.toString())
        })
    },

    save: function () {
      var self = this

      if (this.$refs.logEntryForm.validate()) {
        var request = null
        if (this.logEntry.id) {
          request = this.$http.put(`http://127.0.0.1:4242/log_entries/${this.logEntry.id}`, this.logEntry)
        } else {
          request = this.$http.post('http://127.0.0.1:4242/log_entries/', this.logEntry)
        }

        request
          .then(resp => {
            self.close()
          })
          .catch(err => {
            self.errorMsg = err
          })
      } else {
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    cleanup: function () {
      this.errorMsg = null
      this.$refs.logEntryForm.resetValidation()
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
    },

    removeTag: function (tag) {
      var index = this.logEntry.tags.indexOf(tag)
      this.logEntry.tags.splice(index, 1)
    },

    findTicketByLink: function (link) {
      var foundTicket = this.jiraTickets.find(ticket =>
        ticket.link === link
      )

      return foundTicket
    }

  },

  watch: {
    logEntry: function () {
      // Init `chosenTicket`
      if (this.logEntry.ticket_link) {
        this.chosenTicket = this.findTicketByLink(this.logEntry.ticket_link)
        if (!this.chosenTicket) {
          // Add a "fake" placeholder ticket to the list of tickets
          this.chosenTicket = {
            link: this.logEntry.ticket_link,
            summary: this.logEntry.subject
          }
          this.jiraTickets.push(this.chosenTicket)
        }
      }
    },
    chosenTicket: function (newTicket) {
      if (newTicket) {
        this.logEntry.ticket_link = newTicket.link
        this.logEntry.subject = newTicket.summary
      } else {
        this.logEntry.ticket_link = null
        this.logEntry.subject = null
      }
    }
  },

  data () {
    return {
      showDateMenu: false,
      allTags: [],
      jiraTickets: [],
      chosenTicket: null,
      errorMsg: null,
      rules: {
        subject: [
          subject => !!subject || 'Subject is required'
        ],
        content: [
          content => !!content || 'Content is required'
        ],
        ticket: [
          ticket => this.logEntry.category === 'Ticket' ? !!ticket : true
        ]
      }
    }
  }
}
</script>
