import Constants from './Constants'

export default {
  copyToClipboard: function (name, data) {
    navigator.clipboard.writeText(data)
      .then(function () {
        alert(`${name} Copied!`)
        return false
      })
  },

  openLink: function (url, width = null, height = null) {
    window.Main.newWindow(url, width, height)
  },

  rowColor: function (idx, hilite = false) {
    let color = hilite ? Constants.COLORS.ITEM_HIGHLIGHT : Constants.COLORS.GREY

    if (idx % 2 !== 0) {
      color = hilite ? Constants.COLORS.ITEM_HIGHLIGHT_ALT : Constants.COLORS.GREY_ALT
    }

    return color
  }

}
