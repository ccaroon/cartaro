import Moment from 'moment'

export default {
  formatMoney: function (amount) {
    return (amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' }))
  },

  formatDate: function (date, format = 'MMM DD, YYYY') {
    return (Moment(date).format(format))
  },

  formatDateTime: function (date, format = 'MMM DD, YYYY hh:mma') {
    return (Moment(date).format(format))
  },

  formatTimePeriod: function (start, end) {
    const duration = Moment.duration(end - start)
    return this.formatDuration(duration)
  },

  formatDuration: function (duration) {
    const ymd = [
      duration.years() + 'y',
      duration.months() + 'm',
      duration.days() + 'd'
    ]
    const hms = [
      this.zeroPad(duration.hours()),
      this.zeroPad(duration.minutes()),
      this.zeroPad(duration.seconds())
    ]

    return ymd.join(' ') + ' ' + hms.join(':')
  },

  monthNumberToName: function (monthNumber) {
    return (Moment().month(monthNumber).format('MMMM'))
  },

  zeroPad: function (num, places = 2) {
    return String(num).padStart(places, '0')
  },

  humanizeDateRange: function (startDate, endDate) {
    const now = Moment()
    let value = null

    // TODO: Update to use new CountDown methods
    if (startDate && !endDate) {
      const start = Moment.unix(startDate)

      // * Start Only: BEFORE Event -> Count Down | AFTER Event -> Count Up
      value = start.from(now)
    } else if (startDate && endDate) {
      const start = Moment.unix(startDate)
      const end = Moment.unix(endDate)

      // * Start & End: BEFORE -> Count Down | DURING -> Count Up | AFTER -> Show Duration
      if (now.isBefore(start)) {
        // 'BEFORE --> Count DOWN'
        value = `Starts ${start.from(now)}`
      } else if (now.isBetween(start, end)) {
        // 'DURING --> Count Up'
        value = `Ends ${end.from(now)}`
      } else {
        // 'AFTER --> DURATION'
        value = start.from(end, true)
      }
    }

    return value
  },

  humanizeDate: function (date, defMsg = 'N/A') {
    const now = Moment()
    let value = defMsg

    if (date != null) {
      value = Moment.unix(date).from(now)
    }
    return value
  },

  humanizeDays: function (days) {
    const aDate = Moment().add(days, 'days')
    // humanDays = `${days} days`

    // if (days >= 7 && days < 30) {
    //   humanDays = `${days / 7} weeks`
    // }
    return aDate.fromNow(true)
  }

}
