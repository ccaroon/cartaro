import Format from '../lib/Format'
import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Holiday extends Resource {
  static RESOURCE_NAME = 'time_off/holidays'
  static DEFAULT_ICON = 'mdi-timetable'

  icon () {
    let icon = Icon.superSearch(this.name)

    if (icon === null) {
      const month = Format.formatDate(new Date(), 'MMMM')
      icon = Icon.superSearch(month, Holiday.DEFAULT_ICON)
    }

    return icon
  }

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default Holiday
