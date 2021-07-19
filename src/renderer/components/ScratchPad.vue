<template>
  <v-container class="black">
    <AppBar
      v-bind:name="'Scratch Pad'"
      v-bind:buttons="appBarButtons"
      v-bind:hideSearch="true"
    ></AppBar>
    <v-tabs v-model="activeTab" fixed-tabs dark>
      <v-tab v-for="i in Array(numTabs).keys()" :key="i">
        <v-icon :color="tabColor(i)">mdi-numeric-{{ i + 1 }}-circle</v-icon>
      </v-tab>
      <v-tabs-items v-model="activeTab">
        <v-tab-item v-for="i in Array(numTabs).keys()" :key="i">
          <Markdown
            :content="activeContent"
            @update="contentUpdate"
            v-bind:keyMap="keyMap"
            theme="lesser-dark"
          ></Markdown>
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
  </v-container>
</template>
<script>
import Mousetrap from 'mousetrap'

import AppBar from './Shared/AppBar'
import Format from '../lib/Format'
import LocalForage from 'localforage'
import Markdown from './Shared/Markdown'
import Note from '../models/Note'
import Notification from '../lib/Notification'

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
    tabColor: function (tabNum) {
      let color = 'light-green accent-3'
      if (tabNum === this.activeTab && this.dirty) {
        color = 'red accent-3'
      }
      return color
    },

    tabKey: function (tabNum) {
      return `scratch-pad-tab-${tabNum}`
    },

    setActiveTab: function (tabNum) {
      this.activeTab = tabNum
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
      const self = this
      const storageKey = this.tabKey(tabNum)

      LocalForage.setItem(storageKey, content)
        .then(() => {
          self.dirty = false
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

    convertTabToNote: function () {
      const dtStamp = Format.formatDateTime(new Date(), 'MMM DD, YYYY HH:mm:ss')
      const title = `ScratchPad #${this.activeTab + 1} - ${dtStamp}`
      const note = new Note({
        title: title,
        content: this.activeContent
      })

      note.save({
        handlers: {
          onSuccess: () => {
            Notification.success(`Converted Tab #${this.activeTab + 1} to ${title}`, 4000)
            this.contentUpdate('')
          },
          onError: (err) => { Notification.error(`SP.Editor.convertTabToNote: ${err.toString()}`) }
        }
      })
    },

    erase: function () {
      this.saveTab(this.activeTab, '')
      this.contentUpdate('')
    },

    eraseAll: function () {
      for (let i = 0; i < this.numTabs; i++) {
        this.saveTab(i, '')
      }
      this.contentUpdate('')
    },

    contentUpdate: function (newContent) {
      if (newContent !== this.activeContent) {
        this.dirty = true
        this.activeContent = newContent
      }
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
    const self = this

    const data = {
      activeTab: 0,
      numTabs: 5,
      activeContent: '',
      dirty: false,
      keyMap: {
        'Cmd-S': () => { this.saveActiveTab() },
        'Ctrl-S': () => { this.saveActiveTab() }
      },
      appBarButtons: [
        { name: 'Save', icon: 'mdi-content-save', action: this.saveActiveTab },
        { name: 'Erase', icon: 'mdi-eraser', color: 'pink lighten-3', action: this.erase },
        { name: 'Export', icon: 'mdi-application-export', action: this.convertTabToNote },
        { name: '|' },
        { name: 'Erase All', icon: 'mdi-nuke', color: 'red darken-3', action: this.eraseAll }
      ]
    }

    for (let i = 0; i < data.numTabs; i++) {
      // For when CodeMirror is focused
      data.keyMap[`Cmd-${i + 1}`] = () => { this.setActiveTab(i) }
      data.keyMap[`Ctrl-${i + 1}`] = () => { this.setActiveTab(i) }

      // For when this component is focused
      Mousetrap.bind([`ctrl+${i + 1}`, `command+${i + 1}`], () => {
        self.setActiveTab(i)
        return false
      })
    }

    return data
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
