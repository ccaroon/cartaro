<template>
  <v-card>
    <v-card-title :class="constants.COLORS.GREY">ToDo</v-card-title>
    <v-card-text>...</v-card-text>
  </v-card>
</template>
<script>
import Utils from '../../lib/Utils'
import Constants from '../../lib/Constants'

export default {
  name: 'home-todos',
  components: {},

  mounted: function () {
  },

  methods: {
  },

  data () {
    return {
      constants: Constants,
      utils: Utils
    }
  }
}
</script>
