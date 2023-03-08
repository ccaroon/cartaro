<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <v-dialog :value="value" persistent max-width="65%" max-height="100%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>Note Editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="toggleFullscreen()">
          <v-icon color="blue" size="20"
            >mdi-{{
              this.isFullscreen ? "window-maximize" : "overscan"
            }}</v-icon
          >
        </v-btn>
        <v-btn small icon @click="view()">
          <v-icon color="green" size="20">mdi-eye</v-icon>
        </v-btn>
        <v-divider vertical inset></v-divider>
        <v-btn small icon @click="close()">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-text>
        <v-form ref="noteForm">
          <v-container>
            <v-row v-show="!this.isFullscreen">
              <v-col cols="10">
                <v-text-field
                  label="Title"
                  v-model="note.title"
                  outlined
                  hide-details
                  dense
                  :rules="rules.title"
                  >{{ note.title }}</v-text-field
                >
              </v-col>
              <v-col cols="2">
                <v-checkbox
                  v-model="note.is_favorite"
                  label="Favorite"
                  dense
                ></v-checkbox>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <Markdown
                  :content="buffer"
                  :height="this.isFullscreen ? 77 : 65"
                  @update="(newContent) => (note.content = newContent)"
                  @save="saveBuffer"
                ></Markdown>
              </v-col>
            </v-row>
            <v-row v-show="!this.isFullscreen">
              <v-col>
                <v-combobox
                  v-model="note.tags"
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
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-alert dense color="error" v-show="errorMsg"
          >{{ this.errorMsg }}
        </v-alert>
        <v-spacer></v-spacer>
        <span v-show="!this.isFullscreen">
          <v-btn color="success" @click="save()">Save</v-btn>
          <v-btn color="red" text @click="close()">Close</v-btn>
        </span>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
/* eslint-disable vue/no-mutating-props */
import notification from '../../lib/notification'
import Markdown from '../Shared/Markdown'

import Tag from '../../models/Tag'

export default {
  name: 'notes-editor',
  components: { Markdown },
  props: ['note', 'value'],

  mounted: function () {
    this.loadTags()
  },

  methods: {
    loadTags: function () {
      Tag.loadAll({
        onSuccess: (tags) => { this.allTags = tags },
        onError: (err) => notification.error(`NT.Editor.loadTags: ${err.toString()}`)
      })
    },

    saveBuffer: function () {
      this.save(false)
    },

    save: function (close = true) {
      const self = this

      if (this.$refs.noteForm.validate()) {
        this.errorMsg = null
        this.note.save({
          handlers: {
            onSuccess: () => {
              if (close) {
                self.close()
              }
            },
            onError: (err) => { notification.error(`NT.Editor.save: ${err.toString()}`) }
          }
        })
      } else {
        this.isFullscreen = false
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    cleanup: function () {
      this.errorMsg = null
      this.$refs.noteForm.resetValidation()
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
      this.isFullscreen = false
    },

    view: function () {
      this.save(false)
      this.cleanup()
      this.$emit('view')
    },

    toggleFullscreen: function () {
      this.isFullscreen = !this.isFullscreen
    },

    removeTag: function (tag) {
      const index = this.note.tags.indexOf(tag)
      this.note.tags.splice(index, 1)
    }

  },

  watch: {
    note: function () {
      if (!this.note.content) {
        this.note.content = ''
      }
      this.buffer = this.note.content
    }
  },

  data () {
    return {
      allTags: [],
      buffer: this.note.content || '',
      config: global.Cartaro.config,
      errorMsg: null,
      isFullscreen: false,
      rules: {
        title: [
          title => !!title || 'Title is required'
        ],
        content: [
          content => !!content || 'Content is required'
        ]
      }
    }
  }
}
</script>
