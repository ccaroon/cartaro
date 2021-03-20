// Config
// -----------------------------------------------------------------------------
var app = process.type === 'renderer'
  ? require('electron').remote.app
  : require('electron').app
const fs = require('fs')
const path = require('path')

const docPath = path.join(app.getPath('documents'), 'Cartaro')
// -----------------------------------------------------------------------------
class Config {
  static DEFAULTS = {}

  path = null
  data = null

  constructor(configPath) {
    this.path = configPath
    this.load()
  }

  get (path, defValue = null, isTransient = false) {
    const pathParts = path.split(':')
    var value = this.data
    if (isTransient) {
      value = this.data.__transient
    }

    pathParts.forEach((key) => {
      value = value[key]
    })

    if (value === undefined || value === null) {
      value = defValue
    }

    return value
  }

  getTransient (path, defValue = null) {
    return this.get(path, defValue, true)
  }

  set (path, value, isTransient = false) {
    const pathParts = path.split(':')
    const key = pathParts.pop()
    var data = this.data
    if (isTransient) {
      data = this.data.__transient
    }

    pathParts.forEach((item) => {
      data = data[item]
    })
    data[key] = value
  }

  setTransient (path, value) {
    this.set(path, value, true)
  }

  load () {
    if (this.data === null) {
      if (fs.existsSync(this.path)) {
        var contents = fs.readFileSync(this.path)
        var data = JSON.parse(contents)

        this.data = Object.assign({}, Config.DEFAULTS, data.CARTARO)
      } else {
        this.data = Config.DEFAULTS
      }

      this.data.__transient = {}
    }
  }

  save () {
    delete this.data.__transient
    var data = {
      CARTARO: this.data
    }
    var json = JSON.stringify(data)
    fs.writeFileSync(this.path, json)
  }
}
// -----------------------------------------------------------------------------
const suffix = process.env.NODE_ENV === 'development' ? '-dev' : ''
const configFile = `${docPath}/CartaroCfg${suffix}.json`
const __instance = new Config(configFile)
// -----------------------------------------------------------------------------
export default __instance
