<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-app-bar dense flat>
        <v-icon :color="note.is_favorite ? 'yellow' : ''">{{
          note.icon()
        }}</v-icon>
        <v-toolbar-title>{{ note.title }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-text
        v-html="$markdown.render(note.content || '')"
        class="pt-3"
        style="height: 750px"
      ></v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-chip
          small
          label
          class="pa-1 mr-1"
          v-for="(tag, idx) in note.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'note-viewer',
  components: {},
  props: ['note', 'value'],

  methods: {
    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return { }
  }
}
</script>
