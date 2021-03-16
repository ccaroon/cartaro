<template>
  <v-container>
    <AppBar
      v-bind:name="'Secrets'"
      v-bind:numPages="Math.ceil(totalSecrets / perPage)"
      v-bind:newItem="newSecret"
      v-bind:newIcon="'mdi-lock-plus'"
      v-bind:refresh="refresh"
    ></AppBar>
    <SecretEditor
      v-model="showEditor"
      v-bind:secret="secret"
      v-on:close="closeEditor"
    ></SecretEditor>
    <SecretViewer
      v-model="showViewer"
      v-bind:secret="secret"
      v-bind:isHidden="isHidden[secret.id]"
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
            :color="isHidden[secret.id] ? 'red' : 'green'"
            @click="$set(isHidden, secret.id, !isHidden[secret.id])"
            >mdi-{{ isHidden[secret.id] ? "lock" : "lock-open" }}</v-icon
          >
        </v-list-item-avatar>
        <v-list-item-content @click="view(secret)">
          <v-list-item-title
            :class="secret.isDeleted() ? 'text-decoration-line-through' : ''"
          >
            {{ secret.name }} |
            <span class="text-caption text--secondary"
              >{{ secret.system }} / {{ secret.sub_system }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-row dense no-gutters>
              <v-col cols="3" v-for="(val, fld) in secret.decrypt()" :key="fld">
                <v-icon
                  @click.stop="utils.copyToClipboard(fld.toUpperCase(), val)"
                  >mdi-{{ constants.ICONS.secrets[fld] }}</v-icon
                >&nbsp;
                <template v-if="isHidden[secret.id]">**********</template>
                <template v-else>{{ val }}</template>
              </v-col>
              <v-col>
                <Tags
                  v-bind:tags="secret.tags"
                  v-bind:color="rowColor(idx + 1)"
                ></Tags>
              </v-col>
            </v-row>
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
import Format from '../lib/Format'
import Notification from '../lib/Notification'
import Utils from '../lib/Utils'

import Secret from '../models/Secret'

import Actions from './Shared/Actions'
import AppBar from './Shared/AppBar'
import SecretEditor from './Secrets/Editor'
import SecretViewer from './Secrets/Viewer'
import Tags from './Shared/Tags'

export default {
  name: 'secrets-main',
  components: { Actions, AppBar, SecretViewer, SecretEditor, Tags },
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
      var query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'system'
      }

      if (this.searchText) {
        var parts = this.searchText.split(':', 2)
        if (parts.length === 2) {
          query[parts[0].trim()] = parts[1].trim()
        } else {
          query.name = this.searchText
          query.system = this.searchText
          query.sub_system = this.searchText
          query.note = this.searchText
        }
      }

      Secret.fetch(query, '/', {
        handlers: {
          onSuccess: (items, total) => {
            self.totalSecrets = total
            self.secrets = items

            self.secrets.forEach(secret => {
              this.isHidden[secret.id] = true
            })
          },
          onError: (err) => { Notification.error(`SE.Main.load: ${err.toString()}`) }
        }
      })
    },

    view: function (secret) {
      this.secret = secret
      this.showViewer = true
    },

    newSecret: function () {
      this.edit(new Secret({
        type: Secret.TYPE_USERNAME_PASSWORD,
        data: {
          username: '',
          password: ''
        }
      }))
    },

    edit: function (secret) {
      this.secret = secret
      this.showEditor = true
    },

    remove: function (secret) {
      var self = this
      var safe = 1
      var msg = `Archive "${secret.system}/${secret.sub_system}/${secret.name}"?`

      if (secret.isDeleted()) {
        safe = 0
        msg = `Delete "${secret.system}/${secret.sub_system}/${secret.name}"?`
      }

      var doDelete = confirm(msg)
      if (doDelete) {
        secret.delete({
          safe: safe,
          handlers: {
            onSuccess: () => { self.load() },
            onError: (err) => { Notification.error(`SE.Main.remove: ${err.toString()}`) }
          }
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
      secret: new Secret({}),
      secrets: [],
      // Using an Array and indexing by secret.id b/c Object was not
      // trigging UI updates on changes
      isHidden: [],
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
