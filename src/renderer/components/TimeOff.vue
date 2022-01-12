<template>
  <v-container fluid>
    <AppBar
      v-bind:name="'TimeOff'"
      v-bind:hideSearch="true"
      v-bind:buttons="appBarButtons"
    ></AppBar>
    <v-row dense>
      <v-col>
        <PTOPersonal></PTOPersonal>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col>
        <PTOHolidays></PTOHolidays>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import AppBar from './Shared/AppBar'
import PTOHolidays from './TimeOff/Holidays'
import PTOPersonal from './TimeOff/Personal'

export default {
  name: 'timeoff',
  components: { AppBar, PTOHolidays, PTOPersonal },

  mounted: function () {
  },

  methods: {
    bindShortcutKeys: function () {}
  },

  data () {
    return {
      appBarButtons: []
    }
  }
}</script>
