<template>
  <div>
    <NoteEditor
      v-model="showEditor"
      v-bind:note="note"
      v-on:close="closeEditor"
    ></NoteEditor>
    <NoteViewer
      v-model="showViewer"
      v-bind:note="note"
      v-on:close="showViewer = false"
    ></NoteViewer>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY"
        >Notes
        <v-btn icon x-small @click="newNote"><v-icon>mdi-plus</v-icon></v-btn>
      </v-card-title>

      <v-virtual-scroll :items="notes" item-height="45" height="180">
        <template v-slot:default="{ index, item }">
          <v-list-item
            :class="utils.rowColor(index)"
            @click="viewNote(item)"
            dense
          >
            <v-list-item-icon>
              <v-icon @click.stop="editNote(item)"
                >mdi-file-edit-outline</v-icon
              >
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ format.formatDateTime(item.created_at * 1000) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-card>
  </div>
</template>
<script>
// import Moment from 'moment'

import NoteEditor from '../Notes/Editor'
import NoteViewer from '../Notes/Viewer'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Utils from '../../lib/Utils'

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
      this.editNote({})
    },

    editNote: function (note) {
      this.note = note
      this.showEditor = true
    },

    closeEditor: function () {
      this.showEditor = false
      this.loadNotes()
    },

    loadNotes: function () {
      var self = this
      var qs = `op=and&is_favorite=true&deleted_at=null&sort_by=created_at:desc`

      this.$http.get(`http://127.0.0.1:4242/notes/?${qs}`)
        .then(resp => {
          self.notes = resp.data.notes
        })
        .catch(err => {
          self.$emit('error', 'error', `Notes: ${err.response.status} - ${err.response.data.error.substring(0, 120)}`)
        })
    }
  },

  data () {
    return {
      notes: [],
      note: {},
      showEditor: false,
      showViewer: false,
      constants: Constants,
      format: Format,
      utils: Utils
    }
  }
}
</script>
