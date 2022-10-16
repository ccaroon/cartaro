<template>
  <v-dialog :value="value" persistent scrollable max-width="75%">
    <v-card>
      <v-app-bar dense flat>
        <v-icon :color="note.is_favorite ? 'yellow' : ''">{{
        note.icon()
        }}</v-icon>
        <v-toolbar-title>{{ note.title }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="edit()">
          <v-icon color="green" size="20">mdi-pencil</v-icon>
        </v-btn>
        <v-divider vertical inset></v-divider>
        <v-btn small icon @click="close()">
          <v-icon color="red">mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
      <!-- eslint-disable vue/no-v-text-v-html-on-component -->
      <v-card-text v-html="$markdown.render(note.content || '')" class="pt-3" style="height: 750px"></v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-chip small label class="pa-1 mr-1" v-for="(tag, idx) in note.tags" :key="idx">{{ tag }}</v-chip>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'notes-viewer',
  components: {},
  props: ['note', 'value'],

  methods: {
    close: function () {
      this.$emit('close')
    },

    edit: function () {
      this.$emit('edit')
    }
  },

  data () {
    return {}
  }
}
</script>
