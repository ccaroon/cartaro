// import { ipcRenderer } from 'electron'

export default {
  info: function (msg, timeout = 10000) {
    this.showNotification({
      icon: 'mdi-information',
      color: 'info',
      message: msg,
      timeout
    })
  },

  success: function (msg, timeout = 10000) {
    this.showNotification({
      icon: 'mdi-information',
      color: 'success',
      message: msg,
      timeout
    })
  },

  warn: function (msg, timeout = -1) {
    this.showNotification({
      icon: 'mdi-alert',
      color: 'warning',
      message: msg,
      timeout
    })
  },

  error: function (msg) {
    this.showNotification({
      icon: 'mdi-alert-octagram',
      color: 'error',
      message: msg,
      timeout: -1
    })
  },

  showNotification: function (opts) {
    // ipcRenderer.send('app-show-notification', opts)
    const msg = `[${opts.color}] --${opts.message}-- (${opts.icon})`
    console.log(msg)
    alert(msg)
  }
}
