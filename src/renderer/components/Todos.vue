<template>
  <v-container>
    <AppBar
      v-bind:name="'Todos'"
      v-bind:numPages="Math.ceil(totalTodos / perPage)"
      v-bind:newItem="newTodo"
      v-bind:newIcon="'mdi-file-check-outline'"
      v-bind:refresh="refresh"
    ></AppBar>
    <v-list dense>
      <v-list-item
        v-for="(todo, idx) in todos"
        :key="todo.id"
        :class="rowColor(idx)"
      >
        <v-list-item-avatar>
          <v-icon :color="priorityColor(todo.priority)"
            >mdi-numeric-{{ todo.priority }}-circle</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-avatar>
          <v-icon :color="todo.is_complete ? 'green' : ''"
            >mdi-checkbox-{{ todo.is_complete ? "marked" : "blank" }}</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>
            {{ todo.title }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ humanize(todo) }}
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
import Tags from './Shared/Tags'

export default {
  name: 'todos-main',
  components: { Actions, AppBar, Tags },
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
      }

      this.$http.get(`http://127.0.0.1:4242/todos/?${qs}`)
        .then(resp => {
          self.totalTodos = resp.data.total
          self.todos = resp.data.todos

          self.todos.forEach((cd) => {
            self.initDate(cd)
          })
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    newTodo: function () {
      alert('newTodo')
      //   var todo = {
      //     name: '** NEW COUNTDOWN **',
      //     // Set Date to something early so it appears at the top of the list
      //     start_at: Moment('1971-01-01').unix(),
      //     end_at: null
      //   }

      //   this.$http.post(`http://127.0.0.1:4242/todos/`, todo)
      //     .then(resp => {
      //       this.load()
      //     })
      //     .catch(err => {
      //       console.log(`Error creating CountDown: ${err}`)
      //     })
    },

    edit: function (todo) {
      alert(`Edit: ${todo.title}`)
    },

    priorityColor: function (priority) {
      var colors = ['black',
        'red',
        'orange',
        'yellow darken-1',
        'green',
        'blue',
        'indigo',
        'violet',
        'grey',
        'black'
      ]
      return colors[priority]
    },

    dateDisplay: function (todo) {
      var asString = 'N/A'

      if (todo.due_at != null) {
        asString = Format.formatDateTime(todo.due_at * 1000)
      }
      return asString
    },

    humanize: function (todo) {
      var now = Moment()
      var value = 'n/a'
      const due = Moment.unix(todo.due_at)

      if (todo.due_at != null) {
        value = due.from(now)
      }
      return value
    },

    // Init dates for use with date-picker / time-picker
    initDate: function (todo) {
      this.$set(todo, 'dueAt', Format.formatDate(todo.due_at * 1000, 'YYYY-MM-DD'))
    },

    clearDueDate: function (todo) {
      todo.due_at = null
      this.save(todo)
    },

    save: function (todo) {
      var self = this
      todo.due_at = Moment(`${todo.dueDate} ${todo.dueTime}`, 'YYYY-MM-DD HH:mm:ss').unix()

      this.$http.put(`http://127.0.0.1:4242/todos/${todo.id}`, todo)
        .then(resp => {
          self.load()
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
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

    rowColor: function (idx) {
      var color = Constants.COLORS.GREY

      if (idx % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
      }

      return color
    }
  },

  data () {
    return {
      todos: [],
      page: 1,
      perPage: 11,
      totalTodos: 0,
      format: Format,
      searchText: null,
      showDueDateMenu: [],
      showDueTimeMenu: []
    }
  }
}
</script>
