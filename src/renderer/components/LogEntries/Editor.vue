<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <v-dialog :value="value" persistent max-width="65%" max-height="100%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>LogEntry Editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="view()">
          <v-icon color="green" size="20">mdi-eye</v-icon>
        </v-btn>
        <v-divider vertical inset></v-divider>
        <v-btn small icon @click="close()">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
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
                <Markdown
                  :content="buffer"
                  height="55"
                  @update="(newContent) => (logEntry.content = newContent)"
                  @save="saveBuffer"
                ></Markdown>
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
/* eslint-disable vue/no-mutating-props */

import Moment from 'moment'
import format from '../../lib/format'
import notification from '../../lib/notification'

import JiraTicket from '../../models/JiraTicket'
import Tag from '../../models/Tag'

import Markdown from '../Shared/Markdown'

export default {
  name: 'log-entries-editor',
  components: { Markdown },
  props: ['logEntry', 'value'],

  mounted: function () {
    this.loadTags()
    this.loadTickets()
  },

  computed: {
    loggedAt: {
      get: function () {
        return format.formatDate(this.logEntry.logged_at * 1000, 'YYYY-MM-DD')
      },

      set: function (newDate) {
        this.logEntry.logged_at = Moment(newDate, 'YYYY-MM-DD').unix()
      }
    }
  },

  methods: {
    loadTickets: function () {
      const self = this

      JiraTicket.fetch({}, '/search', {
        handlers: {
          onSuccess: (tickets) => {
            self.jiraTickets = tickets
          },
          onError: (err) => { notification.error(`LE.Editor.loadTickets: ${err.toString()}`) }
        }
      })
    },

    loadTags: function () {
      Tag.loadAll({
        onSuccess: (tags) => { this.allTags = tags },
        onError: (err) => notification.error(`LE.Editor.loadTags: ${err.toString()}`)
      })
    },

    saveBuffer: function () {
      this.save(false)
    },

    save: function (close = true) {
      const self = this

      if (this.$refs.logEntryForm.validate()) {
        this.logEntry.save({
          handlers: {
            onSuccess: () => {
              if (close) {
                self.close()
              }
            },
            onError: (err) => { self.errorMsg = err }
          }
        })
      } else {
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    cleanup: function () {
      this.errorMsg = null
      this.$refs.logEntryForm.resetValidation()
    },

    view: function () {
      this.save(false)
      this.cleanup()
      this.$emit('view')
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
    },

    removeTag: function (tag) {
      const index = this.logEntry.tags.indexOf(tag)
      this.logEntry.tags.splice(index, 1)
    },

    findTicketByLink: function (link) {
      const foundTicket = this.jiraTickets.find(ticket =>
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
          this.chosenTicket = new JiraTicket({
            link: this.logEntry.ticket_link,
            summary: this.logEntry.subject
          })
          this.jiraTickets.push(this.chosenTicket)
        }
      }

      if (!this.logEntry.content) {
        this.logEntry.content = ''
      }
      this.buffer = this.logEntry.content
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
      buffer: this.logEntry.content || '',
      allTags: [],
      config: global.Cartaro.config,
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
