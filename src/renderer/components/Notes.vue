<template>
  <v-container>
    <AppBar
      v-bind:name="'Notes'"
      v-bind:numPages="Math.ceil(totalNotes / perPage)"
      @refresh="refresh"
      v-bind:buttons="appBarButtons"
    ></AppBar>
    <NoteEditor
      v-model="showEditor"
      v-bind:note="note"
      v-on:close="closeEditor"
      v-on:view="closeAndView"
    ></NoteEditor>
    <NoteViewer
      v-model="showViewer"
      v-bind:note="note"
      v-on:close="closeViewer"
      v-on:edit="closeAndEdit"
    ></NoteViewer>
    <v-list dense>
      <v-list-item
        v-for="(note, idx) in notes"
        :key="note.id"
        :class="utils.rowColor(idx)"
        @click.stop
      >
        <v-list-item-avatar>
          <v-icon :color="note.is_favorite ? 'yellow' : ''">{{
            note.icon()
          }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content @click="view(note)">
          <v-list-item-title
            :class="
              note.isDeleted()
                ? 'subtitle-1 text-decoration-line-through'
                : 'subtitle-1'
            "
            >{{ note.title }}</v-list-item-title
          >
          <v-list-item-subtitle>
            {{
              note.created_at
                ? format.formatDateTime(note.created_at * 1000)
                : "--"
            }}
            <Tags
              v-bind:tags="note.tags"
              v-bind:color="utils.rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{
            onEdit: (item) => {
              edit(item);
            },
            onArchiveDelete: (event, item) => {
              if (event.startsWith('post-')) {
                refresh();
              }
            },
          }"
          v-bind:item="note"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import format from '../lib/format'
import notification from '../lib/notification'
import utils from '../lib/utils'

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
      const self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newNote()
        return false
      })
    },

    refresh: function (opts = {}) {
      if (opts.page) {
        this.page = opts.page
      }

      if (opts.searchText !== '') {
        this.searchText = opts.searchText
      }

      this.load()
    },

    load: function () {
      const self = this
      const query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'created_at'
      }

      if (this.searchText) {
        const parts = this.searchText.split(':', 2)
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
          onError: (err) => { notification.error(`NT.Main.load: ${err.toString()}`) }
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

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeAndView: function () {
      this.showEditor = false
      this.view(this.note)
    },

    closeViewer: function () {
      this.showViewer = false
    },

    closeAndEdit: function () {
      this.closeViewer()
      this.edit(this.note)
    }

  },

  data () {
    const itemHeight = 65

    return {
      note: new Note({}),
      notes: [],
      page: 1,
      perPage: Math.round(window.innerHeight / itemHeight) - 1,
      totalNotes: 0,
      showEditor: false,
      showViewer: false,
      format: format,
      utils: utils,
      searchText: null,
      appBarButtons: [
        { name: 'New', icon: 'mdi-file-plus', action: this.newNote }
      ]
    }
  }
}
</script>
