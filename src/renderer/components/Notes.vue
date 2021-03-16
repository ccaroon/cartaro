<template>
  <v-container>
    <AppBar
      v-bind:name="'Notes'"
      v-bind:numPages="Math.ceil(totalNotes / perPage)"
      v-bind:newItem="newNote"
      v-bind:refresh="refresh"
    ></AppBar>
    <NoteEditor
      v-model="showEditor"
      v-bind:note="note"
      v-on:close="closeEditor"
    ></NoteEditor>
    <NoteViewer
      v-model="showViewer"
      v-bind:note="note"
      v-on:close="closeViewer"
    ></NoteViewer>
    <v-list dense>
      <v-list-item
        v-for="(note, idx) in notes"
        :key="note.id"
        :class="rowColor(idx)"
        @click
      >
        <v-list-item-avatar>
          <v-icon :color="note.is_favorite ? 'yellow' : ''">mdi-star</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(note)">
          <v-list-item-title class="subtitle-1" v-if="!note.isDeleted()">{{
            note.title
          }}</v-list-item-title>
          <v-list-item-title class="subtitle-1" v-else>
            <del>{{ note.title }}</del>
          </v-list-item-title>
          <v-list-item-subtitle>
            {{
              note.created_at
                ? format.formatDateTime(note.created_at * 1000)
                : "--"
            }}
            <Tags
              v-bind:tags="note.tags"
              v-bind:color="rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{ edit: edit, remove: remove }"
          v-bind:item="note"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'
import Notification from '../lib/Notification'

import Note from '../models/Note'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import NoteEditor from './Notes/Editor'
import NoteViewer from './Notes/Viewer'
import Tags from './Shared/Tags'

export default {
  name: 'notes-main',
  components: { Actions, AppBar, NoteEditor, NoteViewer, Tags },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newNote()
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
      var query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'created_at'
      }

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          query[parts[0].trim()] = parts[1].trim()
        } else {
          query.title = this.searchText
          query.content = this.searchText
        }
      }

      Note.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalNotes = total
            self.notes = items
          },
          onError: (err) => { Notification.error(`NT.Main.load: ${err.toString()}`) }
        }
      })
    },

    view: function (note) {
      this.note = note
      this.showViewer = true
    },

    newNote: function () {
      this.edit(new Note({}))
    },

    edit: function (note) {
      this.note = note
      this.showEditor = true
    },

    remove: function (note) {
      var self = this
      var safe = 1
      var msg = `Archive "${note.title}"?`

      if (note.isDeleted()) {
        safe = 0
        msg = `Delete "${note.title}"?`
      }

      var doDelete = confirm(msg)
      if (doDelete) {
        note.delete({
          safe: safe,
          handlers: {
            onSuccess: () => { self.load() },
            onError: (err) => { Notification.error(`NT.Main.remove: ${err.toString()}`) }
          }
        })
      }
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
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
      note: new Note({}),
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
