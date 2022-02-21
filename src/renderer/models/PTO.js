import Format from '../lib/Format'
import Icon from '../lib/Icon'
import Resource from './Resource'
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

  // TODO: write this method
  available () {
    return this.starting_balance
  }

  // TODO: write this method
  used () {
    return 10.0
  }

  toString () {
    return `${this.type} ${this.year}`
  }
}
// -----------------------------------------------------------------------------
export default PTO
