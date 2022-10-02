import Crypto from '../lib/Crypto'
import Icon from '../lib/Icon'
import Resource from './Resource'
// -----------------------------------------------------------------------------
class Secret extends Resource {
  static RESOURCE_NAME = 'secrets'

  static TYPE_USERNAME_PASSWORD = 'username-password'

  changeType (newType) {
    this.type = newType

    // Stub in new, empty data
    this.data = {}
    this.keys(key => {
      this.data[key] = ''
    })
  }

  items (iterator) {
    this.keys(key => {
      iterator(key, this.data[key])
    })
  }

  keys (iterator) {
    this.fieldNames().forEach(fld => {
      iterator(fld)
    })
  }

  values (iterator) {
    this.keys(key => {
      iterator(this.data[key])
    })
  }

  fieldNames () {
    let names = []
    if (this.type) {
      names = this.type.split('-')
    }

    return names
  }

  decrypt () {
    if (this.__encrypted) {
      this.keys(key => {
        this.data[key] = Crypto.decrypt(this.data[key])
      })
      this.__encrypted = false
    }

    return this.data
  }

  icon (field = null) {
    let icon = null

    if (field) {
      icon = Icon.search(field, 'mdi-eye-off')
    } else {
      icon = Icon.get('secret', 'mdi-eye-off')
    }
    return icon
  }

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default Secret
