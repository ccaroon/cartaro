<template>
  <div>
    <TodoEditor
      v-model="showEditor"
      v-bind:todo="todo"
      v-on:close="closeEditor"
    ></TodoEditor>

    <TodoViewer
      v-model="showViewer"
      v-bind:todo="todo"
      v-on:close="closeViewer"
    ></TodoViewer>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Todos
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ todos.length }})</span
        >
        <v-btn icon x-small @click="refresh()"
          ><v-icon>mdi-refresh</v-icon></v-btn
        >
        <v-btn icon x-small @click="newTodo()"><v-icon>mdi-plus</v-icon></v-btn>
      </v-card-title>

      <v-virtual-scroll :items="todos" item-height="45" :height="listHeight">
        <template v-slot:default="{ index, item }">
          <v-list-item :class="item.color(index)" dense @click="view(item)">
            <v-list-item-icon class="mr-3">
              <v-icon
                :color="item.priorityColor()"
                @click.stop="toggleCompleted(item)"
                >mdi-numeric-{{ item.priority }}-box-outline</v-icon
              >
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
                <v-icon size="small" v-if="item.description"
                  >mdi-note-outline</v-icon
                >
              </v-list-item-title>
              <v-list-item-subtitle>
                <span v-if="item.due_at"
                  >Due {{ format.humanizeDate(item.due_at * 1000) }}</span
                >
                <span v-else>No Due Date</span>
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-icon>
              <v-btn x-small icon outlined>
                <v-icon small @click.stop="edit(item)">mdi-pencil</v-icon>
              </v-btn>
              &nbsp;
              <v-btn x-small icon outlined>
                <v-icon small @click.stop="snooze(item)"
                  >mdi-alarm-snooze</v-icon
                >
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
import Moment from 'moment'

import constants from '../../lib/constants'
import format from '../../lib/format'
import notification from '../../lib/notification'
import utils from '../../lib/utils'

import TodoEditor from '../Todos/Editor'
import TodoViewer from '../Todos/Viewer'

import Todo from '../../models/Todo'

// TODO: make these configurable
const DUE_WITHIN = 5
const SNOOZE_AMT = 86400

export default {
  name: 'home-todos',
  components: { TodoEditor, TodoViewer },

  mounted: function () {
    this.load()
  },

  methods: {
    refresh: function (opts = {}) {
      this.load()
    },

    load: function () {
      const self = this
      const daysAhead = Moment().add(DUE_WITHIN, 'days')

      // Todos that are:
      // * not completed
      //       AND
      // * overdue or due within the next X days
      const query = {
        due_at: `lte:${daysAhead.unix()}`,
        is_complete: false,
        op: 'and',
        sort_by: 'due_at,priority'
      }

      Todo.fetch(query, '/', {
        handlers: {
          onSuccess: (todos, totalCount) => {
            self.todos = todos
          },
          onError: (err) => {
            notification.error(`HM.Todos.load: ${err}`)
          }
        }
      })
    },

    toggleCompleted: async function (todo) {
      await todo.toggleCompleted()
      todo.save({
        handlers: {
          onSuccess: (resp) => { this.load() }
        }
      })
    },

    newTodo: function () {
      const todo = new Todo({
        priority: 1,
        repeat: 0
      })
      this.edit(todo)
    },

    snooze: function (todo) {
      todo.due_at = todo.due_at + SNOOZE_AMT
      todo.save({
        handlers: {
          onSuccess: (resp) => { this.refresh() }
        }
      })
    },

    view: function (todo) {
      this.todo = todo
      this.showViewer = true
    },

    closeViewer: function () {
      this.showViewer = false
      // this.load()
    },

    edit: function (todo) {
      this.todo = todo
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.load()
    }
  },

  data () {
    return {
      todo: new Todo({}),
      todos: [],
      listHeight: Math.round(window.innerHeight * 0.25),
      showEditor: false,
      showViewer: false,
      constants: constants,
      format: format,
      utils: utils
    }
  }
}
</script>
