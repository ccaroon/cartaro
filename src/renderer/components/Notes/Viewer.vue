<template>
  <v-dialog v-model="value" persistent scrollable max-width="75%">
    <v-card>
      <v-card-title>
        {{ note.title }}
        &nbsp;
        <v-divider vertical inset></v-divider>&nbsp;
        <v-icon :color="note.is_favorite ? 'yellow' : ''">mdi-star</v-icon>
        <v-divider vertical inset></v-divider>&nbsp;
        <v-chip small label class="mr-1" v-for="(tag,idx) in note.tags" :key="idx">{{ tag }}</v-chip>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text
        v-html="md.render(note.content || '')"
        class="body-1 pt-3"
        style="height: 750px;"
      ></v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import MarkdownIt from 'markdown-it'
import MDEmoji from 'markdown-it-emoji'

export default {
  name: 'notes-viewer',
  components: {},
  props: ['note', 'value'],

  methods: {
    close: function () {
      this.$emit('close')
    }
  },

  data () {
    return {
      // TODO: move to Vue instance like $http
      md: new MarkdownIt().use(MDEmoji)
    }
  }
}
</script>
