export default {
  info: function (msg, timeout = 10000) {
    this.showNotification('Info', {
      icon: 'mdi-information',
      color: 'info',
      message: msg,
      timeout
    })
  },

  success: function (msg, timeout = 10000) {
    this.showNotification('Success', {
      icon: 'mdi-information',
      color: 'success',
      message: msg,
      timeout
    })
  },

  warn: function (msg, timeout = -1) {
    this.showNotification('Warning', {
      icon: 'mdi-alert',
      color: 'warning',
      message: msg,
      timeout
    })
  },

  error: function (msg) {
    this.showNotification('Error', {
      icon: 'mdi-alert-octagram',
      color: 'error',
      message: msg,
      timeout: -1
    })
  },

  showNotification: function (type, opts) {
    console.log(`[${opts.color}] --${opts.message}-- (${opts.icon})`)
    const note = new Notification(type, {
      body: opts.message,
      requireInteraction: opts.timeout < 0
    })
    return note
  }
}
