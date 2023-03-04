import Moment from 'moment'
import format from '../lib/format'
import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class PTO extends Resource {
  static RESOURCE_NAME = 'time_off/personal'
  static DEFAULT_ICON = 'mdi-timetable'

  startingBalance () {
    return parseFloat(this.starting_balance)
  }

  icon () {
    let icon = Icon.superSearch(this.type)

    if (icon === null) {
      const month = format.formatDate(new Date(), 'MMMM')
      icon = Icon.superSearch(month, PTO.DEFAULT_ICON)
    }

    return icon
  }

  accruedPerYear () {
    let apy = 0.0
    if (this.accrual) {
      apy = (12 / this.accrual.period) * this.accrual.rate
    }
    return apy
  }

  accruedYTD () {
    let accrued = 0.0
    if (this.accrual) {
      const now = Moment()
      let availMonths = null
      if (this.year < now.year()) {
        availMonths = 12
      } else if (this.year === now.year()) {
        availMonths = now.month() + 1
      } else if (this.year > now.year()) {
        availMonths = 0
      }
      accrued = (availMonths / this.accrual.period) * this.accrual.rate

      // Can't accrue more than accrual.cap
      // Accrual *stops* when reach cap
      // Adjust for that
      if (this.accrual.cap) {
        const totalAvail = (this.startingBalance() + accrued) - this.used
        if (totalAvail >= this.accrual.cap) {
          accrued = accrued - (totalAvail - this.accrual.cap)
        }
      }
    }
    return accrued
  }

  cap_reached () {
    let over = false

    if (this.accrual && this.accrual.cap) {
      if (this.balance() >= this.accrual.cap) {
        over = true
      }
    }

    return over
  }

  available () {
    return this.startingBalance() + this.accruedYTD()
  }

  balance () {
    return this.available() - this.used
  }

  toString () {
    return `${this.type} ${this.year}`
  }
}
// -----------------------------------------------------------------------------
export default PTO
