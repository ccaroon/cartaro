<template>
  <v-container>
    <AppBar
      v-bind:name="'Todos'"
      v-bind:numPages="Math.ceil(totalTodos / perPage)"
      v-bind:newItem="newTodo"
      v-bind:newIcon="'mdi-file-check-outline'"
      v-bind:refresh="refresh"
    ></AppBar>
    <TodoEditor
      v-model="showEditor"
      v-bind:todo="todo"
      v-bind:priorityColor="priorityColor"
      v-on:close="closeEditor"
    ></TodoEditor>
    <TodoViewer
      v-model="showViewer"
      v-bind:todo="todo"
      v-bind:priorityColor="priorityColor"
      v-on:close="closeViewer"
    ></TodoViewer>
    <v-list dense>
      <v-list-item
        v-for="(todo, idx) in todos"
        :key="todo.id"
        :class="rowColor(idx, todo)"
        @click
      >
        <v-list-item-avatar>
          <v-icon :color="priorityColor(todo.priority)"
            >mdi-numeric-{{ todo.priority }}-circle</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-avatar>
          <v-icon
            :color="todo.is_complete ? 'green' : ''"
            @click="toggleCompleted(todo)"
            >mdi-checkbox-{{ todo.is_complete ? "marked" : "blank" }}</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-content @click="view(todo)">
          <v-list-item-title>
            {{ todo.title }}
          </v-list-item-title>
          <v-list-item-subtitle>
            <template v-if="todo.is_complete">
              Completed {{ format.humanizeDate(todo.completed_at) }} ({{
                format.formatDateTime(todo.completed_at * 1000)
              }})
            </template>
            <template v-else>
              <span v-if="todo.due_at"
                >Due {{ format.humanizeDate(todo.due_at) }} ({{
                  format.formatDateTime(todo.due_at * 1000)
                }})</span
              >
              <span v-else>No Due Date</span>
            </template>
            <v-divider vertical inset></v-divider>
            <template v-if="todo.repeat > 0">
              <v-icon>mdi-calendar-refresh</v-icon>
              Every {{ format.humanizeDays(todo.repeat) }}
            </template>
            <Tags
              v-bind:tags="todo.tags"
              v-bind:color="rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
          <!-- description -->
        </v-list-item-content>

        <Actions
          v-bind:actions="{ edit: edit, remove: remove }"
          v-bind:item="todo"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import Moment from 'moment'
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import TodoEditor from './Todos/Editor'
import TodoViewer from './Todos/Viewer'
import Tags from './Shared/Tags'

export default {
  name: 'todos-main',
  components: { Actions, AppBar, TodoEditor, TodoViewer, Tags },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newTodo()
        return false
      })
    },

    refresh: function (page = null, searchText = '') {
      if (page !== null) {
        this.page = page
      }

      if (searchText !== '') {
        this.searchText = searchText
      }

      this.load()
    },

    load: function () {
      var self = this
      var qs = `page=${this.page}&pp=${this.perPage}&sort_by=is_complete,priority,due_at`

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          qs += `&${parts[0].trim()}=${parts[1].trim()}`
        } else {
          qs += `&title=${this.searchText}`
        }
      } else {
        qs += '&is_complete=false'
      }

      this.$http.get(`http://127.0.0.1:4242/todos/?${qs}`)
        .then(resp => {
          self.totalTodos = resp.data.total
          self.todos = resp.data.todos

          // self.todos.forEach((cd) => {
          //   self.initDate(cd)
          // })
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
          // console.log(err)
        })
    },

    view: function (todo) {
      this.todo = todo
      this.showViewer = true
    },

    newTodo: function () {
      this.edit({
        priority: 1,
        repeat: 0
      })
    },

    edit: function (todo) {
      this.todo = todo
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeViewer: function () {
      this.showViewer = false
    },

    markUncomplete: function (todo) {
      if (todo.repeat > 0) {
        alert('Cannot Mark Repeatable Todos as Uncompleted.')
      } else {
        todo.is_complete = false
        todo.completed_at = null
        this.save(todo)
      }
    },

    markComplete: function (todo) {
      var self = this
      var promise = Promise.resolve(true)

      if (todo.repeat > 0) {
        // clone original todo
        var newTodo = Object.assign({}, todo)
        delete newTodo.id
        newTodo.due_at = Moment(todo.due_at * 1000).add(todo.repeat, 'days').unix()
        promise = Promise.resolve(self.save(newTodo, false))
      }

      promise.then(dontCare => {
        todo.is_complete = true
        todo.completed_at = Moment().unix()
        self.save(todo)
      }).catch(err => {
        console.log(err)
      })
    },

    toggleCompleted: function (todo) {
      if (todo.is_complete) {
        this.markUncomplete(todo)
      } else {
        this.markComplete(todo)
      }
    },

    priorityColor: function (priority) {
      var key = `PRIORITY_${priority}`
      return Constants.COLORS[key]
    },

    dateDisplay: function (todo) {
      var asString = 'No Due Date'

      if (todo.due_at != null) {
        asString = Format.formatDateTime(todo.due_at * 1000)
      }
      return asString
    },

    // // Init dates for use with date-picker / time-picker
    // initDate: function (todo) {
    //   this.$set(todo, 'dueAt', Format.formatDate(todo.due_at * 1000, 'YYYY-MM-DD'))
    // },

    clearDueDate: function (todo) {
      todo.due_at = null
      this.save(todo)
    },

    save: function (todo, resolve = true) {
      var self = this

      var request = null
      if (todo.id) {
        request = this.$http.put(`http://127.0.0.1:4242/todos/${todo.id}`, todo)
      } else {
        request = this.$http.post('http://127.0.0.1:4242/todos/', todo)
      }

      if (resolve) {
        request
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }

      return request
    },

    remove: function (todo) {
      var self = this

      var doDelete = confirm(`Delete "${todo.title}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/todos/${todo.id}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    rowColor: function (idx, todo) {
      var colors = {
        default: [Constants.COLORS.GREY, Constants.COLORS.GREY_ALT],
        dueSoon: ['yellow lighten-2', 'yellow lighten-4'],
        overdue: ['red lighten-2', 'red lighten-4']
      }
      var colorKey = 'default'
      var color = null

      if (todo) {
        const now = Moment()
        const due = Moment.unix(todo.due_at)

        if (!todo.is_complete && todo.due_at) {
          if (due < now) {
            colorKey = 'overdue'
          } else if (due < now.add(7, 'days')) {
            colorKey = 'dueSoon'
          }
        }
      }

      color = colors[colorKey][0]
      if (idx % 2 === 0) {
        color = colors[colorKey][1]
      }

      return color
    }
  },

  data () {
    return {
      todo: {},
      todos: [],
      page: 1,
      perPage: 15,
      totalTodos: 0,
      format: Format,
      searchText: null,
      showViewer: false,
      showEditor: false
    }
  }
}
</script>
