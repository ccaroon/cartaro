<template>
  <v-dialog v-model="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-card-title>
        <span class="headline">Todo Editor</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="todoForm">
          <v-container>
            <v-row dense>
              <v-col cols="9">
                <v-text-field
                  label="Title"
                  v-model="todo.title"
                  outlined
                  dense
                  hide-details
                  :rules="rules.title"
                >
                  {{ todo.title }}
                </v-text-field>
              </v-col>
              <v-col cols="3">
                <v-icon :color="todo.is_complete ? 'green' : ''"
                  >mdi-checkbox-{{
                    todo.is_complete ? "marked" : "blank"
                  }}</v-icon
                >
                <template v-if="todo.is_complete">
                  Completed {{ format.humanizeDate(todo.completed_at) }}
                  <br />
                  <v-icon>mdi-calendar-check</v-icon>
                  {{ format.formatDateTime(todo.completed_at * 1000) }}
                </template>
                <template v-else>Not Yet Complete</template>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-btn-toggle v-model="priority" borderless mandatory>
                  <v-btn icon value="1"
                    ><v-icon large :color="constants.COLORS.PRIORITY_1"
                      >mdi-numeric-1-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="2"
                    ><v-icon large :color="constants.COLORS.PRIORITY_2"
                      >mdi-numeric-2-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="3"
                    ><v-icon large :color="constants.COLORS.PRIORITY_3"
                      >mdi-numeric-3-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="4"
                    ><v-icon large :color="constants.COLORS.PRIORITY_4"
                      >mdi-numeric-4-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="5"
                    ><v-icon large :color="constants.COLORS.PRIORITY_5"
                      >mdi-numeric-5-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="6"
                    ><v-icon large :color="constants.COLORS.PRIORITY_6"
                      >mdi-numeric-6-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="7"
                    ><v-icon large :color="constants.COLORS.PRIORITY_7"
                      >mdi-numeric-7-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="8"
                    ><v-icon large :color="constants.COLORS.PRIORITY_8"
                      >mdi-numeric-8-circle</v-icon
                    ></v-btn
                  >
                  <v-btn icon value="9"
                    ><v-icon large :color="constants.COLORS.PRIORITY_9"
                      >mdi-numeric-9-circle</v-icon
                    ></v-btn
                  >
                </v-btn-toggle>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  label="Description"
                  rows="5"
                  outlined
                  hide-details
                  v-model="todo.description"
                  :rules="rules.description"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-combobox
                  v-model="todo.tags"
                  :items="allTags"
                  label="Tags"
                  outlined
                  multiple
                  dense
                  hide-details
                >
                  <template
                    v-slot:selection="{ attrs, item, select, selected }"
                  >
                    <v-chip
                      v-bind="attrs"
                      :input-value="selected"
                      close
                      small
                      @click="select"
                      @click:close="removeTag(item)"
                      >{{ item }}</v-chip
                    >
                  </template>
                </v-combobox>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <v-menu
                  ref="datePicker"
                  v-model="showDateMenu"
                  :close-on-content-click="true"
                  transition="scale-transition"
                  offset-y
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="dueDate"
                      label="Due Date"
                      readonly
                      outlined
                      dense
                      hide-details
                      clearable
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="dueDate"
                    no-title
                    scrollable
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="3">
                <v-menu
                  ref="timeInPicker"
                  v-model="showTimeMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="dueTime"
                      label="Due Time"
                      readonly
                      outlined
                      dense
                      hide-details
                      clearable
                      :disabled="!todo.due_at"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-model="dueTime"
                    ampm-in-title
                    landscape
                    scrollable
                  ></v-time-picker>
                </v-menu>
              </v-col>
              <v-col>
                <v-card>
                  <v-card-title>Repeat - Every {{ repeat }} Days</v-card-title>
                  <v-card-actions>
                    <v-slider
                      v-model="repeat"
                      max="365"
                      label="Days"
                      thumb-size="24"
                      thumb-label="always"
                      :disabled="!todo.due_at"
                    >
                      <template v-slot:prepend>
                        <v-icon color="red" @click="decRepeat">
                          mdi-minus-circle
                        </v-icon>
                      </template>
                      <template v-slot:append>
                        <v-icon color="green" @click="incRepeat">
                          mdi-plus-circle
                        </v-icon>
                      </template>
                    </v-slider>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="blue"
          @click="save(true)"
          :disabled="todo.is_complete || todo.repeat > 0"
          >Mark Complete</v-btn
        >
        <v-spacer></v-spacer>
        <v-alert v-show="errorMsg" dense color="error">{{
          this.errorMsg
        }}</v-alert>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">Save</v-btn>
        <v-btn color="red" text @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Moment from 'moment'
import Format from '../../lib/Format'
import Constants from '../../lib/Constants'

export default {
  name: 'todo-editor',
  components: { },
  props: ['todo', 'value'],

  updated: function () {
    if (this.todo.due_at) {
      this.dueDate = Format.formatDate(this.todo.due_at * 1000, 'YYYY-MM-DD')
      this.dueTime = Format.formatDate(this.todo.due_at * 1000, 'HH:mm')
    } else {
      this.dueDate = null
      this.dueTime = null
    }
  },

  mounted: function () {
    this.loadTags()
  },

  computed: {
    priority: {
      get: function () {
        return Number(this.todo.priority).toString()
      },
      set: function (newPri) {
        this.todo.priority = parseInt(newPri)
      }
    },
    repeat: {
      get: function () {
        return Number(this.todo.repeat).toString()
      },
      set: function (newPri) {
        this.todo.repeat = parseInt(newPri)
      }
    }
  },

  methods: {
    loadTags: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/tags/`)
        .then(resp => {
          self.allTags = resp.data.tags.map(tag => tag.name)
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    save: function (markComplete = false) {
      var self = this

      if (this.$refs.todoForm.validate()) {
        // TODO: handle repeating todos
        // ...for now, just don't for repeating todos ...
        if (markComplete && this.todo.repeat === 0) {
          this.todo.is_complete = true
          this.todo.completed_at = Moment().unix()
        }

        var request = null
        if (this.todo.id) {
          request = this.$http.put(`http://127.0.0.1:4242/todos/${this.todo.id}`, this.todo)
        } else {
          request = this.$http.post('http://127.0.0.1:4242/todos/', this.todo)
        }

        request
          .then(resp => {
            self.close()
          })
          .catch(err => {
            self.errorMsg = err
          })
      } else {
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    decRepeat: function () {
      this.todo.repeat--
    },

    incRepeat: function () {
      this.todo.repeat++
    },

    cleanup: function () {
      this.errorMsg = null
      this.$refs.todoForm.resetValidation()
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
    },

    removeTag: function (tag) {
      var index = this.todo.tags.indexOf(tag)
      this.todo.tags.splice(index, 1)
    }

  },

  watch: {
    dueDate: function (newDate) {
      if (newDate) {
        var dt = this.dueTime ? this.dueTime : '00:00'
        this.todo.due_at = Moment(`${newDate} ${dt}`, 'YYYY-MM-DD HH:mm').unix()
      } else {
        this.todo.repeat = 0
        this.todo.due_at = null
      }
    },
    dueTime: function (newTime) {
      if (newTime) {
        this.todo.due_at = Moment(`${this.dueDate} ${newTime}`, 'YYYY-MM-DD HH:mm').unix()
      } else {
        this.todo.due_at = Moment(`${this.dueDate} 00:00`, 'YYYY-MM-DD HH:mm').unix()
      }
    }
  },

  data () {
    return {
      showDateMenu: false,
      showTimeMenu: false,
      dueDate: null,
      dueTime: null,
      allTags: [],
      errorMsg: null,
      constants: Constants,
      format: Format,
      rules: {
        title: [
          title => !!title || 'Title is required'
        ]
      }
    }
  }
}
</script>
