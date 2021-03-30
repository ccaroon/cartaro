import { ipcRenderer } from 'electron'

export default {
  info: function (msg) {
    this.showNotification({
      icon: 'mdi-information',
      color: 'info',
      message: msg,
      timeout: 10000
    })
  },

  warn: function (msg) {
    this.showNotification({
      icon: 'mdi-alert',
      color: 'warning',
      message: msg
    })
  },

  error: function (msg) {
    this.showNotification({
      icon: 'mdi-alert-octagram',
      color: 'error',
      message: msg
    })
  },

  showNotification: function (opts) {
    ipcRenderer.send('app-show-notification', opts)
  }
}
