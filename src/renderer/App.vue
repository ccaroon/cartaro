<template>
  <v-app>
    <!-- <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - {{ pageName }}</v-toolbar-title>
    </v-app-bar>-->

    <v-navigation-drawer v-model="drawer" app dark mini-variant clipped>
      <v-list dense>
        <v-list-item
          v-for="(page, index) in menu_main"
          @click="goTo(page)"
          :key="index"
        >
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item
          v-for="(page, index) in menu_misc"
          @click="goTo(page)"
          :key="index"
        >
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-bottom-sheet
      inset
      overlay-color="black"
      overlay-opacity="0.75"
      v-model="showConsole"
    >
      <!-- <Console></Console> -->
    </v-bottom-sheet>

    <v-main>
      <About v-model="showAbout" v-on:close="closeAbout" />
      <router-view></router-view>
      <v-snackbar :timeout="notifyTO" v-model="notifyVisible">
        <span v-for="(note, idx) in notifications" :key="idx">
          <v-icon :color="note.color">{{ note.icon }} }}</v-icon>
          {{ note.message }}<br />
        </span>
        <template v-slot:action="{ attrs }">
          <v-btn icon v-bind="attrs" @click="notifyVisible = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>

    <!-- <v-footer app fixed padless dark>
      <v-col class="text-center" cols="12">
        &copy; 2020 - {{ new Date().getFullYear() }} —
        Craig N. Caroon
      </v-col>
    </v-footer>-->
  </v-app>
</template>

<script>
import Mousetrap from 'mousetrap'
// import Console from './components/Console'
import About from './components/About'

// import { ipcRenderer } from 'electron'

export default {
  name: 'CartaroApp',
  components: { About },
  mounted () {
    // ipcRenderer.on('menu-view-main', (event, arg) => {
    //   this.$router.push('/')
    // })

    // ipcRenderer.on('app-show-notification', (event, note) => {
    //   this.addNotification(note)
    // })

    this.bindShortcutKeys()
    this.registerMenuHandlers()
  },

  methods: {
    addNotification: function (note) {
      if (!this.notifyVisible) {
        this.notifyTO = note.timeout || -1
        this.notifications = []
      } else {
        // If notifications already exists, set the TO to -1 to cause the
        // notification to stay on screen until manually dismissed.
        this.notifyTO = -1
      }

      this.notifications.push(note)
      this.notifyVisible = true
    },

    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+shift+/', 'meta+shift+/'], () => {
        self.showAbout = true
        return false
      })

      Mousetrap.bind(['ctrl+shift+`', 'shift+`'], () => {
        self.showConsole = true
        return false
      })
    },

    registerMenuHandlers: function () {
      // Help
      window.Menu.registerHandler('menu-help-about', (event) => {
        this.showAbout = true
      })
    },

    closeAbout: function () {
      this.showAbout = false
    },

    goTo: function (page) {
      this.pageName = page.name
      this.$router.push(page.path)
    }
  },

  data: () => ({
    drawer: true,
    showAbout: false,
    showConsole: false,
    notifications: [{
      icon: null,
      color: null,
      message: null
    }],
    notifyVisible: false,
    notifyTO: -1,
    pageName: 'Home',
    menu_main: [
      { name: 'Home', path: '/', icon: 'mdi-home' },
      { name: 'LogEntries', path: '/log_entries', icon: 'mdi-book-open-variant' },
      { name: 'WorkDays', path: '/work_days', icon: 'mdi-calendar-clock' },
      { name: 'Notes', path: '/notes', icon: 'mdi-note-multiple' },
      { name: 'Todos', path: '/todos', icon: 'mdi-clipboard-list-outline' },
      { name: 'Secrets', path: '/secrets', icon: 'mdi-lock' },
      { name: 'CountDowns', path: '/count_downs', icon: 'mdi-update' },
      { name: 'ScratchPad', path: '/scratch_pad', icon: 'mdi-square-edit-outline' }
    ],
    menu_misc: [
      { name: 'TimeOff', path: '/timeoff', icon: 'mdi-timetable' }
      // { name: 'Debug', path: '/debug', icon: 'mdi-bug' }
    ]
  })
}
</script>
<style>
blockquote {
  background: #f9f9f9;
  border-left: 5px solid #ccc;
  margin: 0.5em 5px;
  padding: 2px;
}
blockquote p {
  display: inline;
}
</style>
