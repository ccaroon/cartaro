<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-card-title>
        {{ logEntry.subject }}
        <v-spacer></v-spacer>
        <v-chip
          small
          label
          class="mr-1"
          v-for="(tag, idx) in logEntry.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
      </v-card-title>
      <v-card-subtitle>
        <template v-if="logEntry.category === 'Ticket'">
          <span
            style="cursor: pointer"
            class="blue--text"
            @click="utils.openLink('Jira', logEntry.ticket_link)"
          >
            {{ logEntry.category }}
            <v-icon x-small color="blue">mdi-open-in-new</v-icon>
          </span>
        </template>
        <template v-else>{{ logEntry.category }}</template>
        |
        {{
          logEntry.logged_at
            ? format.formatDate(logEntry.logged_at * 1000)
            : "--"
        }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text
        v-html="$markdown.render(logEntry.content || '')"
        class="body-1 pt-3"
        style="height: 500px"
      ></v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import Format from '../../lib/Format'
import Utils from '../../lib/Utils'

export default {
  name: 'logEntry-viewer',
  components: {},
  props: ['logEntry', 'value'],

  methods: {
    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return {
      format: Format,
      utils: Utils
    }
  }
}
</script>
