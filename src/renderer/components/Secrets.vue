<template>
  <v-container>
    <AppBar
      v-bind:name="'Secrets'"
      v-bind:numPages="Math.ceil(totalSecrets / perPage)"
      v-bind:newItem="newSecret"
      v-bind:refresh="refresh"
    ></AppBar>
    <!-- <SecretEditor
      v-model="showEditor"
      v-bind:secret="secret"
      v-on:close="closeEditor"
    ></SecretEditor> -->
    <SecretViewer
      v-model="showViewer"
      v-bind:secret="secret"
      v-bind:decrypt="decryptSecretData"
      v-on:close="closeViewer"
    ></SecretViewer>
    <v-list dense>
      <v-list-item
        v-for="(secret, idx) in secrets"
        :key="secret.id"
        :class="rowColor(idx)"
        @click
      >
        <v-list-item-avatar>
          <v-icon
            :color="secret.__encrypted ? 'red' : 'green'"
            @click="secret.__encrypted = !secret.__encrypted"
            >mdi-{{ secret.__encrypted ? "lock" : "lock-open" }}</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-content @click="view(secret)">
          <v-list-item-title
            :class="
              secret.deleted_at !== null ? 'text-decoration-line-through' : ''
            "
          >
            {{ secret.name }} |
            <span class="text-caption text--secondary"
              >{{ secret.system }} / {{ secret.sub_system }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-row dense no-gutters>
              <v-col
                cols="3"
                v-for="(val, fld) in decryptSecretData(secret)"
                :key="fld"
              >
                <v-icon
                  @click.stop="utils.copyToClipboard(fld.toUpperCase(), val)"
                  >mdi-{{ constants.ICONS.secrets[fld] }}</v-icon
                >&nbsp;
                <template v-if="secret.__encrypted">**********</template>
                <template v-else>{{ val }}</template>
              </v-col>
            </v-row>
            <Tags
              v-bind:tags="secret.tags"
              v-bind:color="rowColor(idx + 1)"
            ></Tags>
          </v-list-item-subtitle>
        </v-list-item-content>
        <Actions
          v-bind:actions="{ edit: edit, remove: remove }"
          v-bind:item="secret"
        ></Actions>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Crypto from '../lib/Crypto'
import Format from '../lib/Format'
import Utils from '../lib/Utils'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
// import SecretEditor from './Secrets/Editor'
import SecretViewer from './Secrets/Viewer'
import Tags from './Shared/Tags'

export default {
  name: 'secrets-main',
  components: { Actions, AppBar, SecretViewer, Tags },
  mounted: function () {
    this.bindShortcutKeys()
    this.load()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        self.newSecret()
        return false
      })
    },

    refresh: function (page = null, searchText = '') {
      if (page !== null) {
        this.page = page
      }

      if (searchText !== '') {
        this.searchText = searchText
      }

      this.load()
    },

    load: function () {
      var self = this
      var qs = `page=${this.page}&pp=${this.perPage}&sort_by=system`

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          qs += `&${parts[0].trim()}=${parts[1].trim()}`
        } else {
          qs += `&name=${this.searchText}&system=${this.searchText}&sub_system=${this.searchText}&note=${this.searchText}`
        }
      }

      this.$http.get(`http://127.0.0.1:4242/secrets/?${qs}`)
        .then(resp => {
          self.totalSecrets = resp.data.total
          self.secrets = resp.data.secrets
        })
        .catch(err => {
          console.log(`${err.response.status} - ${err.response.data.error}`)
        })
    },

    decryptSecretData: function (secret) {
      var clearText = {}

      if (secret && secret.type) {
        var fields = secret.type.split('-')

        fields.forEach(fld => {
          clearText[fld] = Crypto.decrypt(secret.data[fld])
        })
      }

      return clearText
    },

    view: function (secret) {
      this.secret = secret
      this.showViewer = true
    },

    newSecret: function () {
      this.edit({})
    },

    edit: function (secret) {
      this.secret = secret
      this.showEditor = true
    },

    remove: function (secret) {
      var self = this
      var safe = 1
      var msg = `Delete "${secret.system}/${secret.sub_system}/${secret.name}"?`

      if (secret.deleted_at !== null) {
        safe = 0
        msg = `DELETE "${secret.system}/${secret.sub_system}/${secret.name}"?`
      }
      var doDelete = confirm(msg)

      if (doDelete) {
        this.$http.delete(`http://127.0.0.1:4242/secrets/${secret.id}?safe=${safe}`)
          .then(resp => {
            self.load()
          })
          .catch(err => {
            console.log(`${err.response.status} - ${err.response.data.error}`)
          })
      }
    },

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeViewer: function () {
      this.showViewer = false
    },

    rowColor: function (idx) {
      var color = Constants.COLORS.GREY

      if (idx % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
      }
      return color
    }
  },

  data () {
    return {
      secret: {},
      secrets: [],
      page: 1,
      perPage: 14,
      totalSecrets: 0,
      showEditor: false,
      showViewer: false,
      format: Format,
      constants: Constants,
      utils: Utils,
      searchText: null
    }
  }
}
</script>
