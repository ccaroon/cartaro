<template>
  <v-app-bar app dense fixed dark clipped-left>
    <v-app-bar-nav-icon @click="showNotice">
      <v-icon :color="iconColor">{{ icon }}</v-icon>
    </v-app-bar-nav-icon>
    <v-toolbar-title>Ĉartaro - {{ name }}</v-toolbar-title>
    <v-divider class="mx-4" vertical></v-divider>
    <v-row no-gutters align="center">
      <v-col cols="2">
        <v-toolbar-items>
          <template v-for="(button, idx) in buttons">
            <v-divider
              v-if="button.name === '|'"
              vertical
              :key="idx"
            ></v-divider>
            <v-btn
              v-else
              :title="button.name"
              icon
              :key="idx"
              @click.stop="handleButton(button)"
            >
              <v-icon :color="button.color || 'white'">{{
                buttonIcon(button)
              }}</v-icon>
            </v-btn>
          </template>
        </v-toolbar-items>
      </v-col>
      <v-col cols="6">
        <v-toolbar-items>
          <v-pagination
            v-if="numPages"
            v-model="page"
            :length="numPages"
            total-visible="7"
            @input="refresh"
          ></v-pagination>
        </v-toolbar-items>
      </v-col>
      <v-col cols="4">
        <v-toolbar-items>
          <v-text-field
            ref="searchBox"
            v-if="!hideSearch"
            v-model="searchText"
            dense
            clearable
            placeholder="Search..."
            prepend-inner-icon="mdi-magnify"
            @click:clear="clearSearch()"
            @keyup.enter="search()"
            @keyup.esc="clearSearch()"
          ></v-text-field>
        </v-toolbar-items>
      </v-col>
    </v-row>
    <template v-if="endSlot">
      <v-spacer></v-spacer>
      {{ endSlot }}
    </template>
  </v-app-bar>
</template>
<script>
import Mousetrap from 'mousetrap'
import pkgJson from '../../../../package.json'

import notification from '../../lib/notification'

export default {
  name: 'shared-app-bar',
  components: {},
  props: ['name', 'numPages', 'hideSearch', 'buttons', 'endSlot'],

  mounted: function () {
    this.bindShortcutKeys()
  },

  methods: {

    refresh: function () {
      this.$emit('refresh', { page: this.page, searchText: this.searchText })
    },

    search: function () {
      if (this.searchText) {
        this.page = 1
        this.refresh()
      }
    },

    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })

      Mousetrap.bind('left', () => {
        self.page--
        if (self.page < 1) {
          self.page = 1
        }
        this.refresh()
      })
      Mousetrap.bind('right', () => {
        self.page++

        if (self.page > self.numPages) {
          self.page = self.numPages
        }
        this.refresh()
      })
    },

    handleButton: function (button) {
      if (button.type === 'toggle') {
        button.state++
        if (button.state >= button.icons.length) {
          button.state = 0
        }
      }
      button.action()
    },

    buttonIcon: function (button) {
      let icon = null

      if (button.type === 'toggle') {
        icon = button.icons[button.state]
      } else {
        icon = button.icon
      }
      return icon
    },

    showNotice: function () {
      notification.info(`Cartaro - ${this.name}`)
    },

    clearSearch: function () {
      if (this.searchText) {
        this.page = 1
        this.searchText = null
        this.refresh()
      }

      this.$refs.searchBox.blur()
    }
  },

  data () {
    return {
      page: 1,
      icon: pkgJson.icon,
      iconColor: process.env.NODE_ENV === 'development' ? 'red' : '',
      searchText: null,
      env: process.env.NODE_ENV
    }
  }
}
</script>
