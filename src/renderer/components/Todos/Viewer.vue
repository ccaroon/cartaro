<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-app-bar dense flat>
        <v-icon :color="todo.priorityColor()">mdi-numeric-{{ todo.priority }}-circle</v-icon>
        <v-toolbar-title>{{ todo.title }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-subtitle class="pl-4 pb-1">
        <v-icon :color="todo.is_complete ? 'green' : ''">mdi-checkbox-{{ todo.is_complete ? "marked" : "blank" }}
        </v-icon>
        <template v-if="todo.is_complete">
          Completed {{ format.humanizeDate(todo.completed_at * 1000) }} ({{
          format.formatDateTime(todo.completed_at * 1000)
          }})
        </template>
        <template v-else>
          <span v-if="todo.due_at">Due {{ format.humanizeDate(todo.due_at * 1000) }} ({{
          format.formatDateTime(todo.due_at * 1000)
          }})</span>
          <span v-else>No Due Date</span>
        </template>
        <v-divider vertical inset></v-divider>
        <template v-if="todo.repeat > 0">
          <v-icon>mdi-calendar-refresh</v-icon>
          Every {{ format.humanizeDays(todo.repeat) }}
        </template>
      </v-card-subtitle>
      <v-divider></v-divider>
      <!-- eslint-disable vue/no-v-text-v-html-on-component -->
      <v-card-text v-html="$markdown.render(todo.description || '')" class="pt-3" style="height: 250px"></v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-chip small label class="pa-1 mr-1" v-for="(tag, idx) in todo.tags" :key="idx">{{ tag }}</v-chip>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Format from '../../lib/Format'

export default {
  name: 'todo-viewer',
  components: {},
  props: ['todo', 'value'],

  methods: {
    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return {
      format: Format
    }
  }
}
</script>
