<template>
  <v-container>
    <AppBar v-bind:name="'Todos'" v-bind:numPages="Math.ceil(totalTodos / perPage)" v-bind:refresh="refresh"
      v-bind:buttons="appBarButtons"></AppBar>
    <TodoEditor v-model="showEditor" v-bind:todo="todo" v-on:close="closeEditor"></TodoEditor>
    <TodoViewer v-model="showViewer" v-bind:todo="todo" v-on:close="closeViewer"></TodoViewer>
    <v-list dense>
      <v-list-item v-for="(todo, idx) in todos" :key="todo.id" :class="todo.color(idx)" @click.stop>
        <v-list-item-avatar>
          <v-icon :color="todo.is_complete ? 'green' : todo.priorityColor()" @click="toggleCompleted(todo)">
            mdi-numeric-{{ todo.priority }}-box{{
            todo.is_complete ? "" : "-outline"
            }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(todo)">
          <v-list-item-title :class="todo.isDeleted() ? 'text-decoration-line-through' : ''">
            {{ todo.title }}
          </v-list-item-title>
          <v-list-item-subtitle>
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
            <Tags v-bind:tags="todo.tags" v-bind:color="utils.rowColor(idx + 1)"></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>

        <Actions v-bind:actions="{
          onEdit: (item) => {
            edit(item);
          },
          onArchiveDelete: (event, item) => {
            if (event.startsWith('post-')) {
              refresh();
            }
          },
        }" v-bind:item="todo"></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>
<script>
import Mousetrap from 'mousetrap'

import Todo from '../models/Todo'

import format from '../lib/format'
import notification from '../lib/notification'
import utils from '../lib/utils'

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
      const self = this

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
      const self = this
      const query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'due_at,priority,is_complete'
      }

      if (this.searchText) {
        const parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          query[parts[0].trim()] = parts[1].trim()
        } else {
          query.title = this.searchText
        }
      } else {
        query.is_complete = false
      }

      Todo.fetch(query, '/', {
        handlers: {
          onSuccess: (todos, totalCount) => {
            self.totalTodos = totalCount
            self.todos = todos
          },
          onError: (err) => {
            notification.error(`TD.Main.load: ${err.toString()}`)
          }
        }
      })
    },

    toggleCompleted: async function (todo) {
      await todo.toggleCompleted()
      todo.save({
        handlers: {
          onSuccess: (resp) => { this.refresh() },
          onError: (err) => {
            notification.error(`TD.Main.toggleCompleted: ${err.toString()}`)
          }
        }
      })
    },

    view: function (todo) {
      this.todo = todo
      this.showViewer = true
    },

    newTodo: function () {
      const todo = new Todo({
        priority: 1,
        repeat: 0
      })
      this.edit(todo)
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
    }
  },

  data () {
    const itemHeight = 65

    return {
      todo: new Todo({}),
      todos: [],
      page: 1,
      perPage: Math.round(window.innerHeight / itemHeight) - 1,
      totalTodos: 0,
      format: format,
      utils: utils,
      searchText: null,
      showViewer: false,
      showEditor: false,
      appBarButtons: [
        { name: 'New', icon: 'mdi-file-check-outline', action: this.newTodo }
      ]
    }
  }
}
</script>
