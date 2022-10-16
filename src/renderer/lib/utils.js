import constants from './constants'

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
    let color = hilite ? constants.COLORS.ITEM_HIGHLIGHT : constants.COLORS.GREY

    if (idx % 2 !== 0) {
      color = hilite ? constants.COLORS.ITEM_HIGHLIGHT_ALT : constants.COLORS.GREY_ALT
    }

    return color
  }

}
