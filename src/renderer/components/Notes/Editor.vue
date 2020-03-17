<template>
  <v-dialog v-model="value" persistent max-width="75%" max-height="75%">
    <v-card>
      <v-card-title>
        <span class="headline">Note Editor</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="noteForm">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Title"
                  v-model="note.title"
                  outlined
                  :rules="rules.title"
                >{{ note.title }}</v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-textarea label="Content" outlined v-model="note.content" :rules="rules.content"></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="3">
                <v-checkbox v-model="note.is_favorite" label="Favorite"></v-checkbox>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-alert v-show="errorMsg" dense color="error">{{ this.errorMsg }}</v-alert>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">Save</v-btn>
        <v-btn color="red" text @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'notes-editor',
  components: { },
  props: ['note', 'value'],

  methods: {
    save: function () {
      var self = this

      if (this.$refs.noteForm.validate()) {
        this.$http.post('http://127.0.0.1:4242/notes/', this.note)
          .then(resp => {
            var id = resp.data.id
            console.log(id)

            self.cleanup()
            self.close()
          })
          .catch(err => {
            self.errorMsg = err
          })
      } else {
        this.errorMsg = 'Please fill in the required fields.'
      }
    },

    cleanup: function () {
      // this.note = {}
      this.errorMsg = null
    },

    close: function () {
      // this.$emit('input', false)
      this.$emit('close')
    }
  },

  data () {
    return {
      // note: {
      //   // title: null,
      //   // content: null,
      //   // isFavorite: false
      // },
      errorMsg: null,
      rules: {
        title: [
          title => !!title || 'Title is required'
        ],
        content: [
          content => !!content || 'Content is required'
        ]
      }
    }
  }
}
</script>
