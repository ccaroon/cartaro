<template>
  <v-dialog v-model="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-card-title>
        <span class="headline">Note Editor</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="noteForm">
          <v-container>
            <v-row>
              <v-col cols="10">
                <v-text-field
                  label="Title"
                  v-model="note.title"
                  outlined
                  hide-details
                  :rules="rules.title"
                  >{{ note.title }}</v-text-field
                >
              </v-col>
              <v-col cols="2">
                <v-checkbox
                  v-model="note.is_favorite"
                  label="Favorite"
                ></v-checkbox>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <Markdown
                  :content="note.content"
                  @update="(newContent) => (note.content = newContent)"
                ></Markdown>
              </v-col>
            </v-row>
            <v-row>
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
import Notification from '../../lib/Notification'
import Markdown from '../Shared/Markdown'

export default {
  name: 'note-editor',
  components: { Markdown },
  props: ['note', 'value'],

  mounted: function () {
    this.loadTags()
  },

  methods: {
    loadTags: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/tags/`)
        .then(resp => {
          self.allTags = resp.data.tags.map(tag => tag.name)
        })
        .catch(err => {
          Notification.error(`NT.Editor.loadTags: ${err.toString()}`)
        })
    },

    save: function () {
      var self = this

      if (this.$refs.noteForm.validate()) {
        var request = null

        if (this.note.id) {
          request = this.$http.put(`http://127.0.0.1:4242/notes/${this.note.id}`, this.note)
        } else {
          request = this.$http.post('http://127.0.0.1:4242/notes/', this.note)
        }

        request
          .then(resp => {
            self.close()
          })
          .catch(err => {
            Notification.error(`NT.Editor.save: ${err.toString()}`)
          })
      } else {
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
    },

    removeTag: function (tag) {
      var index = this.note.tags.indexOf(tag)
      this.note.tags.splice(index, 1)
    }

  },

  watch: {
    note: function () {
      if (!this.note.content) {
        this.note.content = ''
      }
    }
  },

  data () {
    return {
      allTags: [],
      errorMsg: null,
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
