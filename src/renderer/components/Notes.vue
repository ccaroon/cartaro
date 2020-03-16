<template>
  <v-container>
    <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - Notes</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn icon @click.stop="showNewEdit = true">
          <v-icon>mdi-file-document</v-icon>
        </v-btn>
        <v-text-field dense solo clearable placeholder="Search..." prepend-inner-icon="mdi-magnify"></v-text-field>
      </v-toolbar-items>
      <!-- <v-spacer></v-spacer> -->
    </v-app-bar>
    <NotesNewEdit v-model="showNewEdit"></NotesNewEdit>
    <v-list dense>
      <v-list-item v-for="note in notes" :key="note.id" @click>
        <v-list-item-avatar>
          <v-icon color="yellow">mdi-star</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-text>{{ note.title }}</v-list-item-text>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import NotesNewEdit from './Notes/NewEdit'

export default {
  name: 'notes-main',
  components: { NotesNewEdit },
  mounted: function () {
    this.load()
  },

  methods: {
    load: function () {
      var self = this
      // TODO: Pagination
      // TODO: Don't load `content`
      this.$http.get('http://127.0.0.1:4242/notes/')
        .then(resp => {
          self.notes = resp.data
          console.log(self.notes)
        })
        .catch(err => {
          self.errorMsg = err
        })
    }
  },

  data () {
    return {
      notes: [],
      showNewEdit: false
    }
  }
}
</script>
