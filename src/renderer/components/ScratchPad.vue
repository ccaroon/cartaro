<template>
  <v-container class="black">
    <AppBar
      v-bind:name="'Scratch Pad'"
      v-bind:numPages="0"
      v-bind:newItem="null"
      v-bind:refresh="null"
      v-bind:hideSearch="true"
    ></AppBar>
    <v-tabs v-model="activeTab" fixed-tabs dark>
      <v-tab v-for="i in Array(numTabs).keys()" :key="i">
        <v-icon color="light-green accent-3">mdi-numeric-{{ i }}-circle</v-icon>
      </v-tab>
      <v-tabs-items v-model="activeTab">
        <v-tab-item v-for="i in Array(numTabs).keys()" :key="i">
          <Markdown
            :content="activeContent"
            @update="contentUpdate"
            theme="yonce"
          ></Markdown>
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
  </v-container>
</template>
<script>
import AppBar from './Shared/AppBar'
import LocalForage from 'localforage'
import Markdown from './Shared/Markdown'

export default {
  name: 'scratch-pad',
  components: { AppBar, Markdown },
  mounted: function () {
    this.loadTab(this.activeTab)
  },

  beforeDestroy: function () {
    this.saveTab(this.activeTab)
  },

  methods: {
    tabKey: function (tabNum) {
      return `scratch-pad-tab-${tabNum}`
    },

    loadTab: function (tabNum) {
      const self = this
      const storageKey = this.tabKey(tabNum)
      LocalForage.getItem(storageKey)
        .then((value) => {
          self.activeContent = value
        })
        .catch((err) => {
          Notification.error(`ScratchPad.loadTab(${tabNum}): ${err.toString()}`)
        })
    },

    saveTab: function (tabNum, postSave = null) {
      const storageKey = this.tabKey(tabNum)
      LocalForage.setItem(storageKey, this.activeContent)
        .then(() => {
          if (postSave) {
            postSave()
          }
        })
        .catch((err) => {
          Notification.error(`ScratchPad.saveTab(${tabNum}): ${err.toString()}`)
        })
    },

    contentUpdate: function (newContent) {
      this.activeContent = newContent
    }
  },

  watch: {
    activeTab: function (newTab, oldTab) {
      const self = this
      this.saveTab(oldTab, () => {
        self.loadTab(newTab)
      })
    }
  },

  data () {
    return {
      activeTab: 0,
      numTabs: 5,
      activeContent: ''
    }
  }
}
</script>
<style lang="css" scoped>
/* >>> -means- that this style should effect child components */
>>> .CodeMirror {
  border: 1px solid rgb(52, 253, 34);
  height: 850px;
}
</style>
