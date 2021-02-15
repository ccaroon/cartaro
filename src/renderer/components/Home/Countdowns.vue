<template>
  <v-footer absolute padless color="white">
    <v-list dense rounded>
      <v-row dense no-gutters>
        <v-col cols="2" v-for="(countDown, idx) in countDowns" :key="idx">
          <v-list-item dense rounded class="grey lighten-1">
            <v-list-item-content>
              <v-list-item-title>{{ countDown.name }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ format.humanizeDateRange(countDown.start_at, countDown.end_at) }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
    </v-row>
  </v-footer>
</template>
<script>
import Format from '../../lib/Format'

export default {
  name: 'home-countdowns',
  components: {},

  mounted: function () {
    this.loadCountDowns()
  },

  methods: {
    loadCountDowns: function () {
      var self = this
      var qs = `is_favorite=true&sort_by=start_at`

      this.$http.get(`http://127.0.0.1:4242/count_downs/?${qs}`)
        .then(resp => {
          self.countDowns = resp.data.count_downs
        })
        .catch(err => {
          self.$emit('error', 'error', `Countdowns: ${err.response.status} - ${err.response.data.error.substring(0, 120)}`)
        })
    }
  },

  data () {
    return {
      countDowns: [],
      format: Format
    }
  }
}
</script>
