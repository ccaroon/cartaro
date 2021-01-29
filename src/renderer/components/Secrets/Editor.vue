<template>
  <v-dialog v-model="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-card-title>
        <span class="headline">Secret Editor</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="secretForm">
          <v-container>
            <v-row>
              <v-col>
                <v-text-field
                  label="Name"
                  v-model="secret.name"
                  outlined
                  dense
                  hide-details
                  :rules="rules.name"
                  >{{ secret.name }}</v-text-field
                >
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  label="System"
                  v-model="secret.system"
                  outlined
                  dense
                  hide-details
                  :rules="rules.system"
                  >{{ secret.system }}</v-text-field
                >
              </v-col>
              <v-col cols="6">
                <v-text-field
                  label="Sub-System"
                  v-model="secret.sub_system"
                  outlined
                  dense
                  hide-details
                  >{{ secret.sub_system }}</v-text-field
                >
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-btn-toggle v-model="secretType" dense rounded mandatory>
                  <v-btn value="username-password">Username/Password</v-btn>
                  <v-btn value="token">Token</v-btn>
                  <v-btn value="key-secret">Key/Secret</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
            <v-row v-for="(val, fld) in decrypt(secret, secretData)" :key="fld">
              <v-col>
                <v-text-field
                  :label="fld"
                  :prepend-icon="'mdi-' + constants.ICONS.secrets[fld]"
                  v-model="secretData[fld]"
                  outlined
                  dense
                  hide-details
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  label="Notes"
                  rows="5"
                  outlined
                  hide-details
                  v-model="secret.note"
                ></v-textarea>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-combobox
                  v-model="secret.tags"
                  :items="allTags"
                  label="Tags"
                  outlined
                  multiple
                  dense
                  hide-details
                >
                  <template
                    v-slot:selection="{ attrs, item, select, selected }"
                  >
                    <v-chip
                      v-bind="attrs"
                      :input-value="selected"
                      close
                      small
                      @click="select"
                      @click:close="removeTag(item)"
                      >{{ item }}</v-chip
                    >
                  </template>
                </v-combobox>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-alert v-show="errorMsg" dense color="error">{{
          this.errorMsg
        }}</v-alert>
        <v-spacer></v-spacer>
        <v-btn color="success" @click="save()">Save</v-btn>
        <v-btn color="red" text @click="close()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
// import Format from '../../lib/Format'
import Constants from '../../lib/Constants'

export default {
  name: 'secret-editor',
  components: { },
  props: ['secret', 'decrypt', 'value'],

  mounted: function () {
    this.loadTags()
  },

  methods: {
    loadTags: function () {
      var self = this

      this.$http.get(`http://127.0.0.1:4242/tags/`)
        .then(resp => {
          self.allTags = resp.data.tags.map(tag => tag.name)
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    changeType: function (newType, oldType) {
      if (oldType && newType) {
        this.secret.type = newType
        this.secretData = {}
      }
    },

    save: function () {
      var self = this

      if (this.$refs.secretForm.validate()) {
        this.secret.__encrypted = false
        this.secret.data = this.secretData

        this.$http.post('http://127.0.0.1:4242/secrets/', this.secret)
          .then(resp => {
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
      this.errorMsg = null
      this.$refs.secretForm.resetValidation()
    },

    close: function () {
      this.cleanup()
      this.$emit('close')
    },

    removeTag: function (tag) {
      var index = this.secret.tags.indexOf(tag)
      this.secret.tags.splice(index, 1)
    }

  },

  watch: {
    secretType: 'changeType'
  },

  data () {
    return {
      allTags: [],
      constants: Constants,
      errorMsg: null,
      secretType: null,
      secretData: {},
      rules: {
        name: [
          name => !!name || 'Name is required'
        ],
        system: [
          system => !!system || 'System is required'
        ]
      }
    }
  }
}
</script>
