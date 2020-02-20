<template>
  <v-app id="app">
    <v-content container--fluid>
      <About></About>
      <router-view></router-view>
    </v-content>
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
  }
}
</script>
