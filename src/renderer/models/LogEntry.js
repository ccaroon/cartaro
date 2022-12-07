import Moment from 'moment'

import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class LogEntry extends Resource {
  static RESOURCE_NAME = 'log_entries'

  static CATEGORY_MEETING = 'Meeting'
  static CATEGORY_TICKET = 'Ticket'
  static CATEGORY_OPERATIONAL = 'Operational'
  static CATEGORY_OTHER = 'Other'

  static color (category) {
    let color = null

    switch (category) {
      case LogEntry.CATEGORY_MEETING:
        color = 'indigo accent-1'
        break
      case LogEntry.CATEGORY_TICKET:
        color = 'green accent-3'
        break
      case LogEntry.CATEGORY_OPERATIONAL:
        color = 'cyan lighten-1'
        break
      case LogEntry.CATEGORY_OTHER:
        color = 'grey lighten-1'
        break
      default:
        color = 'white'
        break
    }

    return color
  }

  color () {
    return LogEntry.color(this.category)
  }

  icon () {
    return Icon.search(this.category, 'mdi-book-open-variant')
  }

  isToday () {
    return Moment(this.logged_at * 1000).isSame(Moment(), 'day')
  }

  toString () {
    return this.subject
  }
}
// -----------------------------------------------------------------------------
export default LogEntry
