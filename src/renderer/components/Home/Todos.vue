<template>
  <div>
    <TodoEditor
      v-model="showEditor"
      v-bind:todo="todo"
      v-on:close="closeEditor"
    ></TodoEditor>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Todo
        <v-btn icon x-small @click="newTodo"><v-icon>mdi-plus</v-icon></v-btn>
      </v-card-title>

      <v-virtual-scroll :items="todos" item-height="45" height="180">
        <template v-slot:default="{ index, item }">
          <v-list-item :class="item.color(index)" dense @click="edit(item)">
            <v-list-item-icon>
              <v-icon :color="item.priorityColor()"
                >mdi-numeric-{{ item.priority }}-circle</v-icon
              >
              &nbsp; &nbsp;
              <v-icon
                :color="item.is_complete ? 'green' : ''"
                @click.stop="toggleCompleted(item)"
                >mdi-checkbox-{{
                  item.is_complete ? "marked" : "blank"
                }}</v-icon
              >
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <span v-if="item.due_at"
                  >Due {{ format.humanizeDate(item.due_at) }} ({{
                    format.formatDateTime(item.due_at * 1000)
                  }})</span
                >
                <span v-else>No Due Date</span>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Utils from '../../lib/Utils'

import TodoEditor from '../Todos/Editor'

import { Todo, fetchTodos } from '../../models/Todo'

export default {
  name: 'home-todos',
  components: { TodoEditor },

  mounted: function () {
    this.load()
  },

  methods: {
    load: function () {
      var self = this
      const query = {
        sort_by: 'due_at,priority',
        is_complete: false
      }

      fetchTodos(query, {
        onSuccess: (todos, totalCount) => {
          self.todos = todos
        },
        onError: (err) => {
          self.$emit('error', 'error', `Todos: ${err.response.status} - ${err.response.data.error.substring(0, 120)}`)
        }
      })
    },

    toggleCompleted: function (todo) {
      todo.toggleCompleted()
      todo.save({
        onSuccess: (resp) => { this.load() }
      })
    },

    newTodo: function () {
      var todo = new Todo({
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
      this.load()
    }
  },

  data () {
    return {
      todo: new Todo({}),
      todos: [],
      showEditor: false,
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
