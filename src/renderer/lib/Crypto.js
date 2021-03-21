// https://github.com/csquared/fernet.js
import fernet from 'fernet'
import config from '../../Config'

function _passwordToKey (password) {
  var paddedPwd = password.padEnd(32, ' ')
  return btoa(paddedPwd)
}

var keyStr = _passwordToKey(config.get('encryption_password'))
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
