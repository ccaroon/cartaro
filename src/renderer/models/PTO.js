import Moment from 'moment'
import Format from '../lib/Format'
import Icon from '../lib/Icon'
import Resource from './Resource'
// import WorkDay from './WorkDay'
// -----------------------------------------------------------------------------
class PTO extends Resource {
  static RESOURCE_NAME = 'time_off/personal'
  static DEFAULT_ICON = 'mdi-timetable'

  icon () {
    let icon = Icon.superSearch(this.type)

    if (icon === null) {
      const month = Format.formatDate(new Date(), 'MMMM')
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
      const currMonth = Moment().month() + 1
      accrued = (currMonth / this.accrual.period) * this.accrual.rate
    }
    return accrued
  }

  available () {
    return parseInt(this.starting_balance) + this.accruedYTD()
  }

  // TODO: write this method
  used () {
    // const query = {
    //   pp: 9999,
    //   type: this.type,
    //   sort_by: 'due_at,priority,is_complete'
    // }
    // await WorkDay.fetch(query, '/', { asPromise: true })
    return 0.0
  }

  balance () {
    return this.available() - this.used()
  }

  toString () {
    return `${this.type} ${this.year}`
  }
}
// -----------------------------------------------------------------------------
export default PTO
