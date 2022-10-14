// https://github.com/csquared/fernet.js
import fernet from 'fernet'

function _passwordToKey (password) {
  const paddedPwd = password.padEnd(32, ' ')
  return btoa(paddedPwd)
}

const config = global.Cartaro.config
const keyStr = _passwordToKey(config.get('encryption_password'))
// Set Secret Key Globally for all Fernet opts
fernet.setSecret(keyStr)

// -----------------------------------------------------------------------------
export default {
  decrypt: function (data) {
    let result = null
    if (data) {
      const token = new fernet.Token({ token: data, ttl: 0 })
      result = token.decode()
    }
    return result
  }
}
