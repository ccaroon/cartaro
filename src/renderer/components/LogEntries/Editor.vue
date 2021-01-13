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
              <v-col cols="3">
                <v-text-field
                  v-show="logEntry.category === 'Ticket'"
                  label="Ticket"
                  v-model="logEntry.ticket_link"
                  outlined
                  dense
                  hide-details
                  :rules="rules.ticket"
                ></v-text-field>
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

// TODO: Don't hardcode Jira Location -- Get from Configs (when they get implemented)
const jiraBrowseURL = 'https://jira.cengage.com/browse/'

export default {
  name: 'logEntry-editor',
  components: { },
  props: ['logEntry', 'value'],

  mounted: function () {
    this.loadTags()
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
    loadTags: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/tags/`)
        .then(resp => {
          self.allTags = resp.data.tags.map(tag => tag.name)
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    fixTicket: function () {
      if (this.logEntry.category === 'Ticket') {
        var ticket = this.logEntry.ticket_link.replace(jiraBrowseURL, '')
        this.logEntry.ticket_link = `${jiraBrowseURL}${ticket}`
      } else {
        this.logEntry.ticket_link = null
      }
    },

    save: function () {
      var self = this

      if (this.$refs.logEntryForm.validate()) {
        this.fixTicket()

        this.$http.post('http://127.0.0.1:4242/log_entries/', this.logEntry)
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
    }

  },

  data () {
    return {
      showDateMenu: false,
      allTags: [],
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
