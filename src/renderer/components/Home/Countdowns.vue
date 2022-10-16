<template>
  <v-footer absolute padless color="white">
    <div class="text-center">
      <v-chip
        class="ma-1 pa-5"
        v-for="(countDown, idx) in countDowns"
        :key="idx"
      >
        <v-tooltip top>
          <template v-slot:activator="{ on }">
            <v-icon left v-on="on"> {{ countDown.icon() }} </v-icon>
          </template>
          <span>
            <v-icon color="white">{{ toolTipIcon(countDown) }}</v-icon>
            {{ toolTip(countDown) }}
          </span>
        </v-tooltip>
        {{ countDown.name }}
        <br />
        ~{{ countDown.humanize() }}~
      </v-chip>
    </div>
  </v-footer>
</template>
<script>
import format from '../../lib/format'
import notification from '../../lib/notification'

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
          onError: (err) => { notification.error(`HM.CntDwn.loadCountDowns: ${err}`) }
        }
      })
    },

    toolTipIcon: function (countDown) {
      let icon = 'mdi-timer-sand-empty'

      if (!countDown.hasStarted()) {
        icon = 'mdi-timer-sand-empty'
      } else {
        if (countDown.isDuration()) {
          if (countDown.hasEnded()) {
            icon = 'mdi-timer-sand-complete'
          } else {
            icon = 'mdi-timer-sand'
          }
        } else {
          icon = 'mdi-infinity'
        }
      }

      return icon
    },

    toolTip: function (countDown) {
      let tip = null
      if (countDown.isDuration()) {
        // ** start + end **
        if (countDown.hasEnded()) {
          // - has-ended -> count up till NOW
          // between end_at & now
          tip = format.formatTimePeriod(countDown.end_at * 1000, Date.now())
        } else {
          if (countDown.hasStarted()) {
            // - has-started -> count down till end
            // between now & end_at
            tip = format.formatTimePeriod(Date.now(), countDown.end_at * 1000)
          } else {
            // - not-started -> count down till start
            // between now & start_at
            tip = format.formatTimePeriod(Date.now(), countDown.start_at * 1000)
          }
        }
      } else {
        // ** start only **
        if (countDown.hasStarted()) {
          // - has-started -> count up to NOW
          // between start_at & now
          tip = format.formatTimePeriod(countDown.start_at * 1000, Date.now())
        } else {
          // - not-started -> count down till start
          // between now & start_at
          tip = format.formatTimePeriod(Date.now(), countDown.start_at * 1000)
        }
      }

      return tip
    }
  },

  data () {
    return {
      countDowns: [],
      format: format
    }
  }
}
</script>
