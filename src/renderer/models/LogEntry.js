import Moment from 'moment'

import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class LogEntry extends Resource {
  static RESOURCE_NAME = 'log_entries'

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
