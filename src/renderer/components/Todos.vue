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
        <v-list-item-content>
          <v-list-item-title>
            <v-text-field
              v-model="todo.title"
              placeholder="Title"
              dense
              single-line
              autofocus
              @change="save(todo)"
            ></v-text-field>
          </v-list-item-title>
          <v-list-item-subtitle>{{ humanize(todo) }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-row dense align="center">
          <v-col cols="4">
            <v-menu
              ref="dueDatePicker"
              v-model="showDueDateMenu[idx]"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  label="Due"
                  prepend-icon="mdi-calendar-clock"
                  readonly
                  :value="dateDisplay(todo, 'due')"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-sheet width="100%">
                <v-row dense align="end">
                  <v-col cols="6">
                    <v-date-picker
                      v-model="todo.dueDate"
                      color="green"
                      flat
                      scrollable
                    ></v-date-picker>
                  </v-col>
                  <v-col cols="6">
                    <v-time-picker
                      v-model="todo.dueTime"
                      color="green"
                      flat
                      scrollable
                    ></v-time-picker>
                  </v-col>
                </v-row>
                <v-row dense align="center" justify="center">
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="green"
                      @click="
                        save(todo);
                        $set(showDueDateMenu, idx, false);
                      "
                      >OK</v-btn
                    >
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      rounded
                      color="blue"
                      @click="
                        todo.dueDate = format.formatDate(
                          Date.now(),
                          'YYYY-MM-DD'
                        )
                      "
                      >Today</v-btn
                    >
                  </v-col>
                  <v-col cols="3">
                    <v-btn
                      text
                      color="red"
                      @click="
                        initDate(todo);
                        $set(showDueDateMenu, idx, false);
                      "
                      >Cancel</v-btn
                    >
                  </v-col>
                </v-row>
              </v-sheet>
            </v-menu>
          </v-col>
        </v-row>
        <Actions
          v-bind:actions="{ remove: remove }"
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

export default {
  name: 'todos-main',
  components: { Actions, AppBar },
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
      var qs = `page=${this.page}&pp=${this.perPage}&sort_by=due_at`

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
