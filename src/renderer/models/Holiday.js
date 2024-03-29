import Moment from 'moment'

import format from '../lib/format'
import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Holiday extends Resource {
  static RESOURCE_NAME = 'time_off/holidays'
  static DEFAULT_ICON = 'mdi-timetable'

  icon () {
    let icon = Icon.superSearch(this.name)

    if (icon === null) {
      const month = format.formatDate(new Date(), 'MMMM')
      icon = Icon.superSearch(month, Holiday.DEFAULT_ICON)
    }

    return icon
  }

  thisMonth () {
    return Moment().isSame(Moment(this.date * 1000), 'month')
  }

  isPast () {
    return this.date < Moment().unix()
  }

  // Make a duplicate of this holiday 1 year from now
  duplicate () {
    const dup = new Holiday({
      name: this.name,
      date: Moment(this.date * 1000).add(1, 'y').unix()
    })

    return dup
  }

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default Holiday
