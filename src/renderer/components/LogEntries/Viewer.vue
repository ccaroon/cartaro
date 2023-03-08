<template>
  <v-dialog
    :value="value"
    persistent
    scrollable
    max-width="65%"
    max-height="100%"
  >
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>{{ logEntry.subject }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="edit()">
          <v-icon color="green" size="20">mdi-pencil</v-icon>
        </v-btn>
        <v-divider vertical inset></v-divider>
        <v-btn small icon @click="close()">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-subtitle class="pl-4 pb-1">
        <template v-if="logEntry.category === 'Ticket'">
          <span
            style="cursor: pointer"
            class="blue--text"
            @click="utils.openLink(logEntry.ticket_link)"
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
      <!-- eslint-disable vue/no-v-text-v-html-on-component -->
      <v-card-text
        v-html="$markdown.render(logEntry.content || '')"
        class="pt-3"
        :style="`height: ${window.innerHeight * 0.65}px`"
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
import format from '../../lib/format'
import utils from '../../lib/utils'

export default {
  name: 'log-entries-viewer',
  components: {},
  props: ['logEntry', 'value'],

  methods: {
    edit: function () {
      this.$emit('edit')
    },

    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return {
      format: format,
      utils: utils,
      window: window
    }
  }
}
</script>
