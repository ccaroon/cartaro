<template>
  <v-container fluid class="black">
    <AppBar
      v-bind:name="'Scratch Pad'"
      v-bind:buttons="appBarButtons"
      v-bind:hideSearch="true"
    ></AppBar>
    <v-tabs v-model="activePadNum" fixed-tabs dark>
      <v-tab v-for="(pad, idx) in scratchPads" :key="idx">
        <v-icon :color="tabColor(idx)">{{
          pad.icon(`mdi-numeric-${idx + 1}-box`)
        }}</v-icon>
      </v-tab>
      <v-tabs-items v-model="activePadNum">
        <v-tab-item v-for="(pad, idx) in scratchPads" :key="idx">
          <Markdown
            :id="idx"
            :content="pad.buffer"
            :keyMap="keyMap"
            height="90"
            @update="contentUpdate"
            @save="saveActiveTab"
          >
          </Markdown>
        </v-tab-item>
      </v-tabs-items>
    </v-tabs>
  </v-container>
</template>
<script>
import Mousetrap from 'mousetrap'

import AppBar from './Shared/AppBar'
import format from '../lib/format'
import LocalForage from 'localforage'
import Markdown from './Shared/Markdown'
import Note from '../models/Note'
import notification from '../lib/notification'

export default {
  name: 'scratch-pad-main',
  components: { AppBar, Markdown },
  mounted: function () {
    const self = this

    Mousetrap.bind(['ctrl+s', 'command+s'], () => {
      self.saveActiveTab()
      return false
    })

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
          // Can't pass note.content directly to Markdown component as
          // `content` b/c it's update handler will fire everytime the
          // CM doc changes which causes the `content` prop to change
          // which in turn caused the watch on `content` in the MD component
          // to fire which leads to weird behavior.
          note.buffer = note.content
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
            notification.error(`ScratchPad.loadTab(${tabNum}): ${err.toString()}`)
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
          notification.error(`ScratchPad.saveTab(${tabNum}): ${err.toString()}`)
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
      const dtStamp = format.formatDateTime(new Date(), 'MMM DD, YYYY HH:mm:ss')

      const note = this.contentToNote(pad.content)
      note.title = `${note.title} (${dtStamp})`

      note.save({
        handlers: {
          onSuccess: () => {
            notification.success(`Exported Tab #${this.activePadNum + 1} to "${note.title}"`, 4000)
            this.contentUpdate('')
          },
          onError: (err) => { notification.error(`SP.Editor.saveTabToNotes: ${err.toString()}`) }
        }
      })
    },

    erase: function (tabNum = this.activePadNum) {
      const pad = this.scratchPads[tabNum]
      pad.title = ''
      pad.content = ''
      pad.buffer = ''
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
      config: global.Cartaro.config,
      keyMap: [],
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
      data.keyMap.push({
        key: `Mod-${i + 1}`,
        run () {
          self.setActiveTab(i)
          return true
        }
      })

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
