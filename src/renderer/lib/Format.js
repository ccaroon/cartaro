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

  monthNumberToName: function (monthNumber) {
    return (Moment().month(monthNumber).format('MMMM'))
  }

}
