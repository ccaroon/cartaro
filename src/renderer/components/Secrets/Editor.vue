<template>
  <!-- eslint-disable vue/no-mutating-props -->
  <v-dialog :value="value" persistent max-width="75%" max-height="90%">
    <v-card>
      <v-app-bar dense flat>
        <v-toolbar-title>Secret Editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn small icon @click="close()">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-app-bar>
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
                  <v-btn value="blot">BLOT</v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
            <v-row v-for="fld in secret.fieldNames()" :key="fld">
              <v-col>
                <template v-if="secretType === 'blot'">
                  <span class="text-h6">Content</span>
                  <Markdown
                    :content="blotBuffer"
                    height="25"
                    @update="(newContent) => (secret.data[fld] = newContent)"
                  ></Markdown>
                </template>
                <template v-else>
                  <v-text-field
                    :label="fld"
                    :prepend-icon="secret.icon(fld).code"
                    v-model.lazy="secret.data[fld]"
                    outlined
                    dense
                    hide-details
                    :rules="rules.secretData"
                  ></v-text-field>
                </template>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <span class="text-h6">Notes</span>
                <Markdown
                  :content="noteBuffer"
                  height="25"
                  @update="(newContent) => (secret.note = newContent)"
                ></Markdown>
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
/* eslint-disable vue/no-mutating-props */
import constants from '../../lib/constants'
import notification from '../../lib/notification'
import Markdown from '../Shared/Markdown'
import Tag from '../../models/Tag'

export default {
  name: 'secrets-editor',
  components: { Markdown },
  props: ['secret', 'value'],

  mounted: function () {
    this.loadTags()
  },

  computed: {
    secretType: {
      get: function () {
        return this.secret.type
      },
      set: function (newVal) {
        this.secretTypeVal = newVal
        this.secret.changeType(newVal)
      }
    }
  },

  methods: {
    loadTags: function () {
      Tag.loadAll({
        onSuccess: (tags) => { this.allTags = tags },
        onError: (err) => notification.error(`SE.Editor.loadTags: ${err.toString()}`)
      })
    },

    validateSecretData: function () {
      let OK = true
      this.secret.values(val => {
        if (!val) {
          OK = false
        }
      })

      return OK
    },

    save: function () {
      const self = this

      if (this.$refs.secretForm.validate()) {
        this.secret.__encrypted = false

        this.secret.save({
          handlers: {
            onSuccess: () => { self.close() },
            onError: (err) => { notification.error(`SE.Editor.save: ${err.toString()}`) }
          }
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
      const index = this.secret.tags.indexOf(tag)
      this.secret.tags.splice(index, 1)
    }

  },

  watch: {
    secret: function () {
      this.secretTypeVal = this.secret.type
      this.secret.decrypt()

      if (!this.secret.note) {
        this.secret.note = ''
      }

      this.noteBuffer = this.secret.note
      this.blotBuffer = this.secret.data.blot || ''
    }
  },

  data () {
    return {
      allTags: [],
      noteBuffer: this.secret.note || '',
      blotBuffer: '',
      constants: constants,
      config: global.Cartaro.config,
      errorMsg: null,
      secretTypeVal: null,
      rules: {
        name: [
          name => !!name || 'Name is required'
        ],
        system: [
          system => !!system || 'System is required'
        ],
        secretData: [
          secretData => !!this.validateSecretData(secretData) || 'Secret Data is required'
        ]
      }
    }
  }
}
</script>
