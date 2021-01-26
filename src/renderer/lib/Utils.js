export default {
  copyToClipboard: function (name, data) {
    navigator.clipboard.writeText(data)
      .then(function () {
        alert(`${name} Copied!`)
        return false
      })
  }
}
