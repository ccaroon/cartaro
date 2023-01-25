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
    <v-list dense v-show="activeView === 'list'">
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
    <v-container v-show="activeView === 'card'">
      <v-row>
        <v-col cols="4" v-for="(note, idx) in notes" :key="note.id">
          <v-card>
            <v-card-title
              :class="
                note.isDeleted()
                  ? constants.COLORS.DELETED
                  : utils.rowColor(idx, note.is_favorite)
              "
              @click="view(note)"
            >
              <v-icon left>{{ note.icon() }}</v-icon>
              <span
                :class="note.isDeleted() ? 'text-decoration-line-through' : ''"
                >{{ utils.truncateString(note.title, 30) }}</span
              >
            </v-card-title>
            <v-card-subtitle>
              <Tags
                :tags="note.tags"
                color="grey lighten-1"
                :tagClassOverride="'mr-1 pa-1'"
              ></Tags>
            </v-card-subtitle>
            <!-- eslint-disable vue/no-v-text-v-html-on-component -->
            <v-card-text
              v-html="$markdown.render(utils.summarizeText(note.content, 5))"
              class="pt-1 text-truncate"
              style="height: 150px"
            ></v-card-text>
            <v-card-actions>
              <v-btn icon outlined
                ><v-icon :color="note.is_favorite ? 'yellow' : ''"
                  >mdi-star</v-icon
                ></v-btn
              >
              <v-spacer></v-spacer>
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
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import constants from '../lib/constants'
import format from '../lib/format'
import notification from '../lib/notification'
import utils from '../lib/utils'

import Note from '../models/Note'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import NoteEditor from './Notes/Editor'
import NoteViewer from './Notes/Viewer'
import Tags from './Shared/Tags'

const LIST_ITEM_HEIGHT = 65
const VIEW_LIST = 'list'

const CARD_ITEM_HEIGHT = 130
const VIEW_CARD = 'card'

const COLORS = [
  constants.COLORS.GREY, constants.COLORS.GREY_ALT,
  constants.COLORS.ITEM_HIGHLIGHT, constants.COLORS.ITEM_HIGHLIGHT_ALT
]
// ['light-green accent-3', 'light-green accent-2', 'yellow accent-2']

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

    randomColor: function () {
      const index = Math.floor(Math.random() * COLORS.length)
      return COLORS[index]
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
        sort_by: 'created_at:desc'
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

    toggleView: function () {
      if (this.activeView === VIEW_LIST) {
        this.perPage = Math.round(window.innerHeight / CARD_ITEM_HEIGHT) - 1
        this.activeView = VIEW_CARD
      } else if (this.activeView === VIEW_CARD) {
        this.perPage = Math.round(window.innerHeight / LIST_ITEM_HEIGHT) - 1
        this.activeView = VIEW_LIST
      }
      this.refresh()
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
    return {
      note: new Note({}),
      notes: [],
      activeView: VIEW_CARD,
      page: 1,
      perPage: Math.round(window.innerHeight / CARD_ITEM_HEIGHT) - 1,
      totalNotes: 0,
      showEditor: false,
      showViewer: false,
      constants: constants,
      format: format,
      utils: utils,
      searchText: null,
      appBarButtons: [
        { name: 'New', icon: 'mdi-file-plus', action: this.newNote },
        {
          name: 'ToggleView',
          type: 'toggle',
          state: 0,
          icons: ['mdi-list-box', 'mdi-card-text'],
          action: this.toggleView
        }
      ]
    }
  }
}
</script>
