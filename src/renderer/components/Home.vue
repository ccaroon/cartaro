<template>
  <v-container>
    <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - Home</v-toolbar-title>
      <v-spacer></v-spacer>
      {{ format.formatDate(Date.now(), "dddd MMM Do, YYYY") }}
      <v-spacer></v-spacer>
      <v-text-field
        ref="searchBox"
        v-model="searchText"
        dense
        clearable
        placeholder="Search..."
        prepend-inner-icon="mdi-magnify"
        @click:clear="clearSearch"
        @keyup.enter="search()"
        @keyup.esc="clearSearch()"
      ></v-text-field>
    </v-app-bar>
    <v-row>
      <v-col>
        <Tickets></Tickets>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <Countdowns></Countdowns>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Mousetrap from 'mousetrap'

import Countdowns from './Home/Countdowns'
import Tickets from './Home/Tickets'

import Format from '../lib/Format'

export default {
  name: 'home',
  components: { Countdowns, Tickets },

  mounted: function () {
    this.bindShortcutKeys()
  },

  methods: {
    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })
    },

    search: function () {
    },

    clearSearch: function () {
      if (this.searchText) {
        this.searchText = null
      }

      this.$refs.searchBox.blur()
    }
  },

  data () {
    return {
      searchText: null,
      format: Format
    }
  }
}
</script>
