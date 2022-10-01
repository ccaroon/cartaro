import Constants from './Constants'

const { BrowserWindow } = require('@electron/remote')

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
      title,
      fullscreenable: false,
      webPreferences: {
        devTools: false
      },
      autoHideMenuBar: true,
      width,
      height
    })

    child.loadURL(url)
  },

  rowColor: function (idx, hilite = false) {
    let color = hilite ? Constants.COLORS.ITEM_HIGHLIGHT : Constants.COLORS.GREY

    if (idx % 2 !== 0) {
      color = hilite ? Constants.COLORS.ITEM_HIGHLIGHT_ALT : Constants.COLORS.GREY_ALT
    }

    return color
  }

}
