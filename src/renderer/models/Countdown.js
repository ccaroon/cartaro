import Resource from './Resource'

import Format from '../lib/Format'
// -----------------------------------------------------------------------------
class Countdown extends Resource {
  static RESOURCE_NAME = 'count_downs'

  humanize () {
    return Format.humanizeDateRange(this.start_at, this.end_at)
  }

  toggleFavorite () {
    this.is_favorite = !this.is_favorite
  }
}
// -----------------------------------------------------------------------------
export default Countdown
