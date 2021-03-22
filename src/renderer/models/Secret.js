import Resource from './Resource'

import Crypto from '../lib/Crypto'
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
    this.type.split('-').forEach(fld => {
      iterator(fld)
    })
  }

  values (iterator) {
    this.keys(key => {
      iterator(this.data[key])
    })
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

  toString () {
    return this.name
  }
}
// -----------------------------------------------------------------------------
export default Secret
