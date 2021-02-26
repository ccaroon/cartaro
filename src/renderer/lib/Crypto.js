// https://github.com/csquared/fernet.js
import fernet from 'fernet'
import Config from '../../main/config'
Config.load()

function _passwordToKey (password) {
  var paddedPwd = password.padEnd(32, ' ')
  return btoa(paddedPwd)
}

var keyStr = _passwordToKey(Config.get('CARTARO:encryption_password'))
// Set Secret Key Globally for all Fernet opts
fernet.setSecret(keyStr)

// -----------------------------------------------------------------------------
export default {
  decrypt: function (data) {
    var result = null
    if (data) {
      var token = new fernet.Token({ token: data, ttl: 0 })
      result = token.decode()
    }
    return result
  }
}
