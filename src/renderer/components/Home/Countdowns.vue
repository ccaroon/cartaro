<template>
  <v-footer absolute padless color="white">
    <div class="text-center">
      <v-chip
        class="ma-1 pa-5"
        v-for="(countDown, idx) in countDowns"
        :key="idx"
      >
        <v-icon left> {{ countDown.icon() }} </v-icon>
        {{ countDown.name }}<br />
        ~{{ format.humanizeDateRange(countDown.start_at, countDown.end_at) }}~
      </v-chip>
    </div>
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
        op: 'and',
        is_favorite: true,
        deleted_at: null,
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
