<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <v-dialog :value="value" persistent max-width="65%" max-height="95%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>Todo Editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
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
                  Completed {{ format.humanizeDate(todo.completed_at * 1000) }}
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
                <Markdown
                  :content="descBuffer"
                  height="25"
                  @update="(newContent) => (todo.description = newContent)"
                >
                </Markdown>
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
/* eslint-disable vue/no-mutating-props */

import Moment from 'moment'
import format from '../../lib/format'
import constants from '../../lib/constants'
import notification from '../../lib/notification'
import Tag from '../../models/Tag'

import Markdown from '../Shared/Markdown'

export default {
  name: 'todos-editor',
  components: { Markdown },
  props: ['todo', 'value'],

  updated: function () {
    if (this.todo.due_at) {
      this.dueDate = format.formatDate(this.todo.due_at * 1000, 'YYYY-MM-DD')
      this.dueTime = format.formatDate(this.todo.due_at * 1000, 'HH:mm')
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
      Tag.loadAll({
        onSuccess: (tags) => { this.allTags = tags },
        onError: (err) => notification.error(`TD.Editor.loadTags: ${err.toString()}`)
      })
    },

    save: function (markComplete = false) {
      const self = this

      if (this.$refs.todoForm.validate()) {
        // TODO: handle repeating todos
        // ...for now, just don't for repeating todos ...
        if (markComplete && this.todo.repeat === 0) {
          this.todo.is_complete = true
          this.todo.completed_at = Moment().unix()
        }

        this.todo.save({
          handlers: {
            onSuccess: (resp) => self.close(),
            onError: (err) => { this.errorMsg = err }
          }
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
      const index = this.todo.tags.indexOf(tag)
      this.todo.tags.splice(index, 1)
    }

  },

  watch: {
    dueDate: function (newDate) {
      if (newDate) {
        const dt = this.dueTime ? this.dueTime : '00:00'
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
    },
    todo: function () {
      if (!this.todo.description) {
        this.todo.description = ''
      }

      this.descBuffer = this.todo.description
    }
  },

  data () {
    return {
      descBuffer: this.todo.description || '',
      config: global.Cartaro.config,
      showDateMenu: false,
      showTimeMenu: false,
      dueDate: null,
      dueTime: null,
      allTags: [],
      errorMsg: null,
      constants: constants,
      format: format,
      rules: {
        title: [
          title => !!title || 'Title is required'
        ]
      }
    }
  }
}
</script>
