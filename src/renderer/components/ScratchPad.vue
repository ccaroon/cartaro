<template>
  <v-container fluid class="black">
    <AppBar v-bind:name="'Scratch Pad'" v-bind:buttons="appBarButtons" v-bind:hideSearch="true"></AppBar>
    <v-tabs v-model="activePadNum" fixed-tabs dark>
      <v-tab v-for="(pad, idx) in scratchPads" :key="idx">
        <v-icon :color="tabColor(idx)">{{
        pad.icon(`mdi-numeric-${idx + 1}-box`)
        }}</v-icon>
      </v-tab>
      <v-tabs-items v-model="activePadNum">
        <v-tab-item v-for="(pad, idx) in scratchPads" :key="idx">
          <Markdown :content="pad.content" @update="contentUpdate" v-bind:keyMap="keyMap"
            :theme="config.get('markdown:scratch-pad')"></Markdown>
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
  </v-container>
</template>
<script>
import Mousetrap from 'mousetrap'

import AppBar from './Shared/AppBar'
import Config from '../../Config'
import Format from '../lib/Format'
import LocalForage from 'localforage'
import Markdown from './Shared/Markdown'
import Note from '../models/Note'
import Notification from '../lib/Notification'

export default {
  name: 'ScratchPad',
  components: { AppBar, Markdown },
  mounted: function () {
    const self = this

    // Load all ScratchPads data from LocalStorage
    const promises = []
    for (let i = 0; i < this.numPads; i++) {
      promises.push(this.loadTab(i))
    }

    Promise.all(promises)
      .then((values) => {
        self.activePadNum = 0

        for (let i = 0; i < self.numPads; i++) {
          const note = self.contentToNote(values[i])
          self.scratchPads.push(note)
        }
      })
  },

  beforeDestroy: function () {
    this.saveTab(this.activePadNum)
  },

  methods: {
    tabColor: function (tabNum) {
      let color = 'white'
      const pad = this.scratchPads[tabNum]

      if (pad.content) {
        color = 'light-green accent-3'
        if (tabNum === this.activePadNum && this.dirty) {
          color = 'red accent-3'
        }
      }

      return color
    },

    tabKey: function (tabNum) {
      return `scratch-pad-tab-${tabNum}`
    },

    setActiveTab: function (tabNum) {
      this.activePadNum = tabNum
    },

    loadTab: function (tabNum, postLoad = null) {
      const storageKey = this.tabKey(tabNum)

      if (postLoad) {
        LocalForage.getItem(storageKey)
          .then((value) => {
            postLoad(value)
          })
          .catch((err) => {
            Notification.error(`ScratchPad.loadTab(${tabNum}): ${err.toString()}`)
          })
      } else {
        return LocalForage.getItem(storageKey)
      }
    },

    updateTitle: function (tabNum) {
      const pad = this.scratchPads[tabNum]
      if (pad.content) {
        const lines = pad.content.split('\n')
        pad.title = lines[0]
      } else {
        pad.title = ''
      }
    },

    saveTab: function (tabNum, postSave = null) {
      const self = this
      const pad = this.scratchPads[tabNum]
      const storageKey = this.tabKey(tabNum)

      LocalForage.setItem(storageKey, pad.content)
        .then(() => {
          self.dirty = false
          self.updateTitle(tabNum)

          if (postSave) {
            postSave()
          }
        })
        .catch((err) => {
          Notification.error(`ScratchPad.saveTab(${tabNum}): ${err.toString()}`)
        })
    },

    saveActiveTab: function () {
      this.saveTab(this.activePadNum)
    },

    contentToNote: function (content) {
      let note = null

      if (content) {
        const lines = content.split('\n')
        note = new Note({
          title: lines[0],
          content
        })
      } else {
        note = new Note({ title: '', content: null })
      }

      return note
    },

    saveTabToNotes: function () {
      const pad = this.scratchPads[this.activePadNum]
      const dtStamp = Format.formatDateTime(new Date(), 'MMM DD, YYYY HH:mm:ss')

      const note = this.contentToNote(pad.content)
      note.title = `${note.title} (${dtStamp})`

      note.save({
        handlers: {
          onSuccess: () => {
            Notification.success(`Exported Tab #${this.activePadNum + 1} to "${note.title}"`, 4000)
            this.contentUpdate('')
          },
          onError: (err) => { Notification.error(`SP.Editor.saveTabToNotes: ${err.toString()}`) }
        }
      })
    },

    erase: function (tabNum = this.activePadNum) {
      const pad = this.scratchPads[tabNum]
      pad.title = ''
      pad.content = ''
      // pad.content = null
      // this.$set(pad, 'title', '')
      // this.$set(pad, 'content', null)
      this.saveTab(tabNum)
    },

    eraseAll: function () {
      for (let i = 0; i < this.numPads; i++) {
        this.erase(i)
      }
    },

    contentUpdate: function (newContent) {
      const pad = this.scratchPads[this.activePadNum]
      if (newContent !== pad.content) {
        this.dirty = true
        pad.content = newContent
      }
    }
  },

  watch: {
    activePadNum: function (newTab, oldTab) {
      const self = this
      this.saveTab(oldTab, () => {
        self.activePadNum = newTab
      })
    }
  },

  data () {
    const self = this

    const data = {
      activePadNum: 0,
      numPads: 5,
      scratchPads: [],
      dirty: false,
      config: Config,
      keyMap: {
        'Cmd-S': () => { this.saveActiveTab() },
        'Ctrl-S': () => { this.saveActiveTab() }
      },
      appBarButtons: [
        { name: 'Save', icon: 'mdi-content-save', action: this.saveActiveTab },
        { name: 'Erase', icon: 'mdi-eraser', color: 'pink lighten-3', action: this.erase },
        { name: 'Export', icon: 'mdi-application-export', action: this.saveTabToNotes },
        { name: '|' },
        { name: 'Erase All', icon: 'mdi-nuke', color: 'red darken-3', action: this.eraseAll }
      ]
    }

    for (let i = 0; i < data.numPads; i++) {
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
>>>.CodeMirror {
  border: 1px solid rgb(0, 0, 0);
  height: 1100px;
}
</style>
