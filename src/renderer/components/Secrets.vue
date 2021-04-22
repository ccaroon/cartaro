<template>
  <v-container>
    <AppBar
      v-bind:name="'Secrets'"
      v-bind:numPages="Math.ceil(totalSecrets / perPage)"
      v-bind:refresh="refresh"
      v-bind:buttons="appBarButtons"
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
      <v-list-group
        v-for="(secretList, name, idx) in secrets"
        :key="name"
        :class="utils.rowColor(idx)"
        :prepend-icon="icons.superSearch(name, 'mdi-lock').code"
      >
        <template v-slot:activator>
          <v-list-item-title>{{ name }}</v-list-item-title>
        </template>
        <v-list-item
          v-for="(secret, idx) in secretList"
          :key="secret.id"
          :class="utils.rowColor(idx)"
          @click.stop
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
                <v-col cols="3" v-for="fld in secret.fieldNames()" :key="fld">
                  <v-icon
                    @click.stop="
                      utils.copyToClipboard(fld.toUpperCase(), secret.data[fld])
                    "
                    >{{ secret.icon(fld) }}</v-icon
                  >&nbsp;
                  <template v-if="isHidden[secret.id]">**********</template>
                  <template v-else>{{ secret.data[fld] }}</template>
                </v-col>
                <v-col>
                  <Tags
                    v-bind:tags="secret.tags"
                    v-bind:color="utils.rowColor(idx + 1)"
                  ></Tags>
                </v-col>
              </v-row>
            </v-list-item-subtitle>
          </v-list-item-content>
          <Actions
            v-bind:actions="{
              onEdit: (item) => {
                edit(item);
              },
              onArchiveDelete: (event, item) => {
                if (event.startsWith('post-')) {
                  refresh();
                }
              },
            }"
            v-bind:item="secret"
          ></Actions>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import Constants from '../lib/Constants'
import Format from '../lib/Format'
import Icon from '../lib/Icon'
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
      const self = this

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
      const self = this
      const query = {
        page: this.page,
        pp: this.perPage,
        sort_by: 'system',
        group_by: 'system'
      }

      if (this.searchText) {
        const parts = this.searchText.split(':', 2)
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

            for (const group of Object.values(self.secrets)) {
              group.forEach(secret => {
                secret.decrypt()
                this.isHidden[secret.id] = true
              })
            }
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

    closeEditor: function () {
      this.showEditor = false
      this.refresh()
    },

    closeViewer: function () {
      this.showViewer = false
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
      perPage: 30,
      totalSecrets: 0,
      showEditor: false,
      showViewer: false,
      format: Format,
      constants: Constants,
      icons: Icon,
      utils: Utils,
      searchText: null,
      appBarButtons: [
        { name: 'New', icon: 'mdi-lock-plus', action: this.newSecret }
      ]
    }
  }
}
</script>
