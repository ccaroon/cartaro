<template>
  <v-container>
    <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - Notes</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn icon @click.stop="edit({})">
          <v-icon>mdi-file-document</v-icon>
        </v-btn>
        <v-text-field dense solo clearable placeholder="Search..." prepend-inner-icon="mdi-magnify"></v-text-field>
      </v-toolbar-items>
      <!-- <v-spacer></v-spacer> -->
    </v-app-bar>
    <NotesEditor v-model="showEditor" v-bind:note="note" v-on:close="closeEditor"></NotesEditor>
    <NotesViewer v-model="showViewer" v-bind:note="note" v-on:close="closeViewer"></NotesViewer>
    <v-list dense>
      <v-list-item v-for="(note,idx) in notes" :key="note.id" :class="rowColor(idx)" @click>
        <v-list-item-avatar>
          <v-icon :color="note.is_favorite ? 'yellow' : ''">mdi-star</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(note)">
          <v-list-item-title class="subtitle-1">{{ note.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ note.created_at ? format.formatDateTime(note.created_at*1000) : '--'}}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon outlined @click="edit(note)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-item-action>
        <v-list-item-action>
          <v-btn icon outlined @click="remove(note)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import Constants from '../lib/Constants'
import Format from '../lib/Format'

import NotesEditor from './Notes/Editor'
import NotesViewer from './Notes/Viewer'

export default {
  name: 'notes-main',
  components: { NotesEditor, NotesViewer },
  mounted: function () {
    this.load()
  },

  methods: {
    load: function () {
      var self = this

      this.$http.get('http://127.0.0.1:4242/notes/')
        .then(resp => {
          self.notes = resp.data
        })
        .catch(err => {
          self.errorMsg = err
        })
    },

    view: function (note) {
      this.note = note
      this.showViewer = true
    },

    edit: function (note) {
      this.note = note
      this.showEditor = true
    },

    remove: function (note) {
      var self = this

      var doDelete = confirm(`Delete "${note.title}"?`)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/notes/${note.id}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            self.errorMsg = err
          })
      }
    },

    closeEditor: function () {
      this.showEditor = false
      this.load()
    },

    closeViewer: function () {
      this.showViewer = false
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
      note: {},
      notes: [],
      showEditor: false,
      showViewer: false,
      format: Format
    }
  }
}
</script>
