// https://github.com/csquared/fernet.js
import fernet from 'fernet'

function init (passwd) {
  const keyStr = passwordToKey(passwd)
  fernet.setSecret(keyStr)
}

function passwordToKey (password) {
  const paddedPwd = password.padEnd(32, ' ')
  return btoa(paddedPwd)
}
// -----------------------------------------------------------------------------
export default {
  init,
  decrypt: function (data) {
    let result = null
    if (data) {
      const token = new fernet.Token({ token: data, ttl: 0 })
      result = token.decode()
    }
    return result
  }
}
