<template>
  <div>
    <v-card>
      <v-card-title :class="constants.COLORS.GREY">Balances </v-card-title>

      <v-card-text>This space intentionally left blank</v-card-text>
    </v-card>
  </div>
</template>
<script>
import Constants from '../../lib/Constants'

export default {
  name: 'timeoff-personal',
  components: { },
  data () {
    return {
      constants: Constants
    }
  }
}
</script>
