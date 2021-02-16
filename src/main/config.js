
var app
if (process.type === 'renderer') {
  app = require('electron').remote.app
} else {
  app = require('electron').app
}

const fs = require('fs')
const path = require('path')

const dataPath = path.join(app.getPath('documents'), 'Cartaro')
const configFile = `${dataPath}/CartaroCfg.json`

var configData = {}
var DEFAULTS = {}
// -----------------------------------------------------------------------------
export default {
  // NOT user configurable
  configFile: configFile,
  dataPath: dataPath,

  get: function (path = null) {
    var option = configData

    if (path !== null) {
      var pathParts = path.split(':')

      pathParts.forEach((key) => {
        option = option[key]
      })
    }

    return option
  },

  set: function (path, value) {
    console.log(`SET: Not yet implemented- [${path}] -> [${value}]`)
  },

  load: function () {
    if (fs.existsSync(configFile)) {
      var contents = fs.readFileSync(configFile)
      var data = JSON.parse(contents)

      configData = Object.assign({}, DEFAULTS, data)
    } else {
      // Config file does not exist...
      // 1. Set to defaults
      // 2. Create it.
      configData = DEFAULTS
      this.save()
    }
  },

  save: function () {
    var json = JSON.stringify(configData)
    fs.writeFileSync(configFile, json)
  }
}
