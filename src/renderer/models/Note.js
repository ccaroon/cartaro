import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Note extends Resource {
  static RESOURCE_NAME = 'notes'
  static DEFAULT_ICON = 'mdi-note'

  icon (defIcon = Note.DEFAULT_ICON) {
    let icon = null

    if (this.title) {
      icon = Icon.superSearch(this.title)
    }

    if (icon === null) {
      if (this.tags) {
        icon = Icon.superSearch(this.tags, defIcon)
      } else {
        icon = defIcon
      }
    }

    return icon
  }

  toString () {
    return this.title
  }
}
// -----------------------------------------------------------------------------
export default Note
