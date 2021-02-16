<template>
  <v-app-bar app dense fixed dark clipped-left>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <v-toolbar-title>Ĉartaro - {{ name }}</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-row no-gutters align="center">
      <v-col cols="1">
        <v-toolbar-items>
          <v-btn icon @click.stop="newItem()">
            <v-icon>{{ newIcon || "mdi-file-plus" }}</v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-col>
      <v-col cols="8">
        <v-toolbar-items>
          <v-pagination
            v-model="page"
            :length="numPages"
            total-visible="10"
            @input="refresh"
          ></v-pagination>
        </v-toolbar-items>
      </v-col>
      <v-col>
        <v-toolbar-items>
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
        </v-toolbar-items>
      </v-col>
    </v-row>
  </v-app-bar>
</template>
<script>
import Mousetrap from 'mousetrap'

export default {
  name: 'shared-app-bar',
  components: {},
  props: ['name', 'numPages', 'newItem', 'newIcon', 'refresh'],

  mounted: function () {
    this.bindShortcutKeys()
  },

  methods: {
    search: function () {
      if (this.searchText) {
        this.page = 1
        this.refresh(this.page, this.searchText)
      }
    },

    bindShortcutKeys: function () {
      var self = this

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        self.$refs.searchBox.focus()
        return false
      })
    },

    clearSearch: function () {
      if (this.searchText) {
        this.page = 1
        this.searchText = null
        this.refresh(this.page, this.searchText)
      }

      this.$refs.searchBox.blur()
    }
  },

  data () {
    return {
      page: 1,
      searchText: null
    }
  }
}
</script>
