import { ipcMain } from 'electron'

import config from './config'
import windowHelper from './windowHelper'

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      windowHelper.new(location, width, height)
    })

    // Config Handlers
    // ipcMain.handle('config:get', (event, path, defValue, isTransient) => {
    //   const value = config.get(path, defValue, isTransient)
    //   return value
    // })
    ipcMain.handle('config:data', (event) => {
      return config.data
    })

    // Other Handlers
  }
}
