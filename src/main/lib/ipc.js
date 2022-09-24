import { ipcMain } from 'electron'

import Config from './Config'
import windowHelper from './windowHelper'

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      windowHelper.new(location, width, height)
    })

    // Config Handlers
    ipcMain.handle('config:get', (event, path, defValue, isTransient) => {
      const value = Config.get(path, defValue, isTransient)
      return value
    })

    // Other Handlers
  }
}
