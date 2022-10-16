import Moment from 'moment'

import Resource from './Resource'

import format from '../lib/format'
import Icon from '../lib/Icon'
// -----------------------------------------------------------------------------
class Countdown extends Resource {
  static RESOURCE_NAME = 'count_downs'
  static DEFAULT_ICON = 'mdi-timer'
  humanize () {
    return format.humanizeDateRange(this.start_at, this.end_at)
  }

  icon () {
    let icon = Countdown.DEFAULT_ICON
    if (this.name) {
      icon = Icon.superSearch(this.name, Countdown.DEFAULT_ICON)
    }
    return icon
  }

  onGoing () {
    return this.hasStarted() && !this.hasEnded()
  }

  hasStarted () {
    return (this.start_at * 1000) < Date.now()
  }

  hasEnded () {
    let ended = false

    if (this.end_at) {
      ended = (this.end_at * 1000) < Date.now()
    }

    return ended
  }

  isDuration () {
    return this.start_at && this.end_at
  }

  asDuration () {
    const start = this.start_at * 1000
    const end = this.end_at ? this.end_at * 1000 : Date.now()
    const duration = Moment.duration(end - start)
    return duration
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
