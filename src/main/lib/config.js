// Config Instance
// TODO: Should this module be a sub-class of shared/Config.js?
// -----------------------------------------------------------------------------
import fs from 'fs'
import settings from './settings'

import Config from '../../shared/Config'
// -----------------------------------------------------------------------------
function load (filePath) {
  let data = null
  if (fs.existsSync(filePath)) {
    const contents = fs.readFileSync(filePath)
    const jsonData = JSON.parse(contents)

    data = Object.assign({}, {}, jsonData.CARTARO)
  } else {
    data = {}
  }

  data.__transient = {}
  return data
}

// function save (filePath, data) {
//   delete data.__transient
//   const jsonData = {
//     CARTARO: data
//   }
//   const json = JSON.stringify(jsonData)
//   fs.writeFileSync(filePath, json)
// }
// -----------------------------------------------------------------------------
const suffix = process.env.NODE_ENV === 'development' ? '-dev' : ''
const configFile = `${settings.docPath}/CartaroCfg${suffix}.json`
const configData = load(configFile)
const configInstance = new Config(configData)
// -----------------------------------------------------------------------------
export default configInstance
