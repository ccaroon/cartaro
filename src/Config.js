// Config
// -----------------------------------------------------------------------------
var app = process.type === 'renderer'
  ? require('electron').remote.app
  : require('electron').app
const fs = require('fs')
const path = require('path')

console.log('-------------------------')
console.log(process.env.NODE_ENV)
console.log('-------------------------')
const docPath = path.join(app.getPath('documents'), 'Cartaro')
// TODO: Separate cfg files for Dev and non-Dev
const configFile = `${docPath}/CartaroCfg.json`
// -----------------------------------------------------------------------------
class Config {
  static DEFAULTS = {}

  path = null
  data = null

  constructor(configPath) {
    this.path = configPath
    this.load()
  }

  get (path, isTransient = false) {
    const pathParts = path.split(':')
    var value = this.data
    if (isTransient) {
      value = this.data.__transient
    }

    pathParts.forEach((key) => {
      value = value[key]
    })

    return value
  }

  getTransient (path) {
    return this.get(path, true)
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

        this.data = Object.assign({}, Config.DEFAULTS, data)
      } else {
        this.data = Config.DEFAULTS
      }

      this.data.__transient = {}
    }
  }

  save () {
    delete this.data.__transient
    var json = JSON.stringify(this.data)
    fs.writeFileSync(this.path, json)
  }
}
// -----------------------------------------------------------------------------
const __instance = new Config(configFile)
// -----------------------------------------------------------------------------
export default __instance
