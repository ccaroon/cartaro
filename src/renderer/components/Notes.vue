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
    <v-row justify="center">
      <v-col cols="auto">
        <v-icon size="256">mdi-note</v-icon>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import NotesNewEdit from './Notes/NewEdit'

export default {
  name: 'notes-main',
  components: { NotesNewEdit },
  mounted: function () {
  },

  methods: {
    // create: function () {
    //   this.showNewEdit = true
    // }
  },

  data () {
    return {
      showNewEdit: false
    }
  }
}
</script>
