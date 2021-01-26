// https://github.com/csquared/fernet.js
import fernet from 'fernet'

// TODO: Read CartaroCfg.json

function _passwordToKey (password) {
  var paddedPwd = password.padEnd(32, ' ')
  return btoa(paddedPwd)
}

// TODO: use config file to read `encryption_password`
//       instead of hard-coding password here
var keyStr = _passwordToKey('42')
// Set Secret Key Globally for all Fernet opts
fernet.setSecret(keyStr)

// -----------------------------------------------------------------------------
export default {
  decrypt: function (data) {
    var token = new fernet.Token({ token: data, ttl: 0 })
    return token.decode()
  }
}
