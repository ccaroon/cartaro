<template>
  <v-app>
    <!-- <v-app-bar app dense fixed dark clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Ĉartaro - {{ pageName }}</v-toolbar-title>
    </v-app-bar>-->

    <v-navigation-drawer v-model="drawer" app dark mini-variant clipped>
      <v-list dense>
        <v-list-item v-for="(page, index) in menu" @click="goTo(page)" :key="index">
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <About />
      <router-view></router-view>
    </v-content>

    <v-footer app fixed dark>
      <span>&copy; 2020</span>
    </v-footer>
  </v-app>
</template>

<script>
import About from './components/About'

const { ipcRenderer } = require('electron')

export default {
  name: 'Cartaro',
  components: { About },
  mounted () {
    ipcRenderer.on('menu-view-main', (event, arg) => {
      this.$router.push('/')
    })
  },

  methods: {
    goTo: function (page) {
      this.pageName = page.name
      this.$router.push(page.path)
    }
  },

  data: () => ({
    drawer: true,
    about: false,
    pageName: 'Home',
    menu: [
      { name: 'Home', path: '/', icon: 'mdi-home' },
      { name: 'Notes', path: '/notes', icon: 'mdi-note-multiple' },
      { name: 'Secrets', path: '/secrets', icon: 'mdi-lock' }
    ]
  })
}
</script>
