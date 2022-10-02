<template>
  <v-container fluid>
    <AppBar v-bind:name="'Home'" v-bind:hideSearch="true"
      v-bind:endSlot="format.formatDate(Date.now(), 'dddd MMM Do, YYYY')" v-bind:buttons="appBarButtons"></AppBar>
    <v-row dense no-gutters>
      <WorkDays></WorkDays>
    </v-row>
    <v-row dense>
      <v-col>
        <Tickets></Tickets>
      </v-col>
      <v-col>
        <Todos></Todos>
      </v-col>
      <v-col>
        <Notes></Notes>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col>
        <LogEntries></LogEntries>
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
// import Mousetrap from 'mousetrap'

import AppBar from './Shared/AppBar'
import Countdowns from './Home/Countdowns'
import LogEntries from './Home/LogEntries'
import Notes from './Home/Notes'
import Tickets from './Home/Tickets'
import Todos from './Home/Todos'
import WorkDays from './Home/WorkDays'

import Format from '../lib/Format'

export default {
  name: 'HomeScreen',
  components: { AppBar, Countdowns, LogEntries, Notes, Tickets, Todos, WorkDays },

  mounted: function () {
    this.bindShortcutKeys()
  },

  methods: {
    bindShortcutKeys: function () { }
  },

  data () {
    return {
      format: Format,
      appBarButtons: []
    }
  }
}
</script>
