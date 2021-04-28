import Resource from './Resource'

import Format from '../lib/Format'
import Icon from '../lib/Icon'
// -----------------------------------------------------------------------------
class Countdown extends Resource {
  static RESOURCE_NAME = 'count_downs'
  static DEFAULT_ICON = 'mdi-timer'
  humanize () {
    return Format.humanizeDateRange(this.start_at, this.end_at)
  }

  icon () {
    let icon = Countdown.DEFAULT_ICON
    if (this.name) {
      icon = Icon.superSearch(this.name, Countdown.DEFAULT_ICON)
    }
    return icon
  }

  toggleFavorite () {
    this.is_favorite = !this.is_favorite
  }

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default Countdown
