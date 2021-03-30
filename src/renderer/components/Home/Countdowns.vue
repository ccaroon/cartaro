<template>
  <v-footer absolute padless color="white">
    <v-list dense rounded>
      <v-row dense no-gutters>
        <v-col v-for="(countDown, idx) in countDowns" :key="idx">
          <v-list-item dense rounded class="grey lighten-1">
            <v-list-item-content>
              <v-list-item-title>{{ countDown.name }}</v-list-item-title>
              <v-list-item-subtitle>
                {{
                  format.humanizeDateRange(countDown.start_at, countDown.end_at)
                }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
    </v-list>
  </v-footer>
</template>
<script>
import Format from '../../lib/Format'
import Notification from '../../lib/Notification'

import Countdown from '../../models/Countdown'

export default {
  name: 'home-countdowns',
  components: {},

  mounted: function () {
    this.loadCountDowns()
  },

  methods: {
    loadCountDowns: function () {
      const self = this
      const query = {
        is_favorite: true,
        sort_by: 'start_at'
      }

      Countdown.fetch(query, '/', {
        handlers: {
          onSuccess: (items) => {
            self.countDowns = items
          },
          onError: (err) => { Notification.error(`HM.CntDwn.loadCountDowns: ${err}`) }
        }
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
