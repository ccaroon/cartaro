<template>
  <v-container class="black">
    <AppBar
      v-bind:name="'Scratch Pad'"
      v-bind:buttons="appBarButtons"
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
    const self = this
    this.loadTab(this.activeTab, (content) => {
      self.contentUpdate(content)
    })
  },

  beforeDestroy: function () {
    this.saveTab(this.activeTab, this.activeContent)
  },

  methods: {
    tabKey: function (tabNum) {
      return `scratch-pad-tab-${tabNum}`
    },

    loadTab: function (tabNum, postLoad) {
      const storageKey = this.tabKey(tabNum)
      LocalForage.getItem(storageKey)
        .then((value) => {
          postLoad(value)
        })
        .catch((err) => {
          Notification.error(`ScratchPad.loadTab(${tabNum}): ${err.toString()}`)
        })
    },

    saveTab: function (tabNum, content, postSave = null) {
      const storageKey = this.tabKey(tabNum)
      LocalForage.setItem(storageKey, content)
        .then(() => {
          if (postSave) {
            postSave()
          }
        })
        .catch((err) => {
          Notification.error(`ScratchPad.saveTab(${tabNum}): ${err.toString()}`)
        })
    },

    saveActiveTab: function () {
      this.saveTab(this.activeTab, this.activeContent)
    },

    clearAll: function () {
      for (let i = 0; i < this.numTabs; i++) {
        this.saveTab(i, '')
      }
      this.contentUpdate('')
    },

    contentUpdate: function (newContent) {
      this.activeContent = newContent
    }
  },

  watch: {
    activeTab: function (newTab, oldTab) {
      const self = this
      this.saveTab(oldTab, this.activeContent, () => {
        self.loadTab(newTab, (content) => {
          this.activeContent = content
        })
      })
    }
  },

  data () {
    return {
      activeTab: 0,
      numTabs: 5,
      activeContent: '',
      appBarButtons: [
        { text: 'Save', icon: 'mdi-content-save', action: this.saveActiveTab },
        { text: 'Erase All', icon: 'mdi-nuke', action: this.clearAll }
      ]
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
