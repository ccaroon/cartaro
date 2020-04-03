<template>
  <v-container>
    <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - Notes</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-row no-gutters align="center">
        <v-col cols="1">
          <v-toolbar-items>
            <v-btn icon @click.stop="edit({})">
              <v-icon>mdi-file-document</v-icon>
            </v-btn>
          </v-toolbar-items>
        </v-col>
        <v-col cols="8">
          <v-toolbar-items>
            <v-pagination
              v-model="page"
              :length="Math.ceil(totalNotes/perPage)"
              total-visible="10"
              @input="load"
            ></v-pagination>
          </v-toolbar-items>
        </v-col>
        <v-col>
          <v-toolbar-items>
            <v-text-field
              v-model="searchText"
              dense
              clearable
              placeholder="Search..."
              prepend-inner-icon="mdi-magnify"
              @click:clear="clearSearch"
              @keyup.enter="search()"
            ></v-text-field>
          </v-toolbar-items>
        </v-col>
      </v-row>
    </v-app-bar>
    <NotesEditor v-model="showEditor" v-bind:note="note" v-on:close="closeEditor"></NotesEditor>
    <NotesViewer v-model="showViewer" v-bind:note="note" v-on:close="closeViewer"></NotesViewer>
    <v-list dense>
      <v-list-item v-for="(note,idx) in notes" :key="note.id" :class="rowColor(idx)" @click>
        <v-list-item-avatar>
          <v-icon :color="note.is_favorite ? 'yellow' : ''">mdi-star</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(note)">
          <v-list-item-title class="subtitle-1" v-if="note.deleted_at === null">{{ note.title }}</v-list-item-title>
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ note.title }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ note.created_at ? format.formatDateTime(note.created_at*1000) : '--'}}
            <v-chip
              x-small
              label
              class="mr-1 float-right"
              :color="rowColor(idx+1)"
              v-for="(tag,tgIdx) in note.tags"
              :key="tgIdx"
            >{{ tag }}</v-chip>
          </v-list-item-subtitle>
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
      var qs = `page=${self.page}&pp=${self.perPage}`

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          qs += `&${parts[0].trim()}=${parts[1].trim()}`
        } else {
          qs += `&title=${this.searchText}&content=${this.searchText}`
        }
      }

      this.$http.get(`http://127.0.0.1:4242/notes/?${qs}`)
        .then(resp => {
          self.totalNotes = resp.data.total
          self.notes = resp.data.notes
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
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
        this.$http.delete(`http://127.0.0.1:4242/notes/${note.id}?safe=1`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
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
    },

    search: function () {
      if (this.searchText) {
        this.page = 1
        this.load()
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.page = 1
        this.searchText = null
        this.load()
      }
    }
  },

  data () {
    return {
      note: {},
      notes: [],
      page: 1,
      perPage: 15,
      totalNotes: 0,
      showEditor: false,
      showViewer: false,
      format: Format,
      searchText: null
    }
  }
}
</script>
