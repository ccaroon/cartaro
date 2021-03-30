import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Note extends Resource {
  static RESOURCE_NAME = 'notes'

  icon () {
    let icon = null
    if (this.tags) {
      icon = Icon.superSearch(this.tags)
    }

    if (icon === null) {
      icon = Icon.superSearch(this.title, 'mdi-note')
    }

    return icon
  }

  toString () {
    return this.title
  }
}
// -----------------------------------------------------------------------------
export default Note
