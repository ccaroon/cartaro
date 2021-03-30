<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-card-title>
        {{ note.title }}
        &nbsp;
        <v-divider vertical inset></v-divider>&nbsp;
        <v-icon :color="note.is_favorite ? 'yellow' : ''">mdi-star</v-icon>
        <v-spacer></v-spacer>
        <v-chip
          small
          label
          class="mr-1"
          v-for="(tag, idx) in note.tags"
          :key="idx"
          >{{ tag }}</v-chip
        >
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text
        v-html="$markdown.render(note.content || '')"
        class="body-1 pt-3"
        style="height: 750px"
      ></v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="close()">Close</v-btn>
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
