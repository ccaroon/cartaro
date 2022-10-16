<template>
  <div>
    <NoteEditor
      v-model="showEditor"
      v-bind:note="note"
      v-on:close="closeEditor"
      v-on:view="closeAndView"
    ></NoteEditor>
    <NoteViewer
      v-model="showViewer"
      v-bind:note="note"
      v-on:close="showViewer = false"
      v-on:edit="closeAndEdit"
    ></NoteViewer>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Notes
        <span class="text-subtitle-1 grey--text text--darken-1"
          >({{ notes.length }})</span
        >
        <v-btn icon x-small @click="newNote()"><v-icon>mdi-plus</v-icon></v-btn>
      </v-card-title>

      <v-virtual-scroll :items="notes" item-height="45" :height="listHeight">
        <template v-slot:default="{ index, item }">
          <v-list-item
            :class="utils.rowColor(index)"
            @click="viewNote(item)"
            dense
          >
            <v-list-item-icon class="mr-3">
              <v-icon>{{ item.icon() }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ format.formatDateTime(item.created_at * 1000) }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-icon>
              <v-btn x-small icon outlined>
                <v-icon small @click.stop="editNote(item)">mdi-pencil</v-icon>
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
import NoteEditor from '../Notes/Editor'
import NoteViewer from '../Notes/Viewer'

import Note from '../../models/Note'

import constants from '../../lib/constants'
import format from '../../lib/format'
import notification from '../../lib/notification'
import utils from '../../lib/utils'

export default {
  name: 'home-notes',
  components: { NoteEditor, NoteViewer },

  mounted: function () {
    this.loadNotes()
  },

  methods: {

    viewNote: function (note) {
      this.note = note
      this.showViewer = true
    },

    newNote: function () {
      this.editNote(new Note({}))
    },

    editNote: function (note) {
      this.note = note
      this.showEditor = true
    },

    closeAndEdit: function () {
      this.showViewer = false
      this.editNote(this.note)
    },

    closeAndView: function () {
      this.showEditor = false
      this.viewNote(this.note)
    },

    closeEditor: function () {
      this.showEditor = false
      this.loadNotes()
    },

    loadNotes: function () {
      const self = this
      const query = {
        op: 'and',
        is_favorite: true,
        deleted_at: null,
        sort_by: 'created_at:desc'
      }

      Note.fetch(query, '/', {
        handlers: {
          onSuccess: (items) => {
            self.notes = items
          },
          onError: (err) => { notification.error(`HM.Notes.loadNotes: ${err}`) }
        }
      })
    }
  },

  data () {
    return {
      notes: [],
      listHeight: Math.round(window.innerHeight * 0.25),
      note: new Note({}),
      showEditor: false,
      showViewer: false,
      constants: constants,
      format: format,
      utils: utils
    }
  }
}
</script>
