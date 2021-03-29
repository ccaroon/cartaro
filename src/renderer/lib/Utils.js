import Constants from './Constants'

const { BrowserWindow } = require('electron').remote

export default {
  copyToClipboard: function (name, data) {
    navigator.clipboard.writeText(data)
      .then(function () {
        alert(`${name} Copied!`)
        return false
      })
  },

  openLink: function (title, url, width = 1200, height = 900) {
    const main = BrowserWindow.getFocusedWindow()
    const child = new BrowserWindow({
      parent: main,
      title: title,
      fullscreenable: false,
      webPreferences: {
        devTools: false
      },
      autoHideMenuBar: true,
      width: width,
      height: height
    })

    child.loadURL(url)
  },

  rowColor: function (idx) {
    let color = Constants.COLORS.GREY

    if (idx % 2 === 0) {
      color = Constants.COLORS.GREY_ALT
    }
    return color
  }

}
