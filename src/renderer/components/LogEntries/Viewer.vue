<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>{{ logEntry.subject }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-subtitle class="pl-4 pb-1">
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
        class="pt-3"
        style="height: 500px"
      ></v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-chip
          small
          label
          class="pa-1 mr-1"
          v-for="(tag, idx) in logEntry.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
        <v-spacer></v-spacer>
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
