import { ipcMain } from 'electron'

import Window from './window'

export default {
  registerHandlers: function () {
    // Main Handlers
    ipcMain.handle('main:newWindow', (event, location, width, height) => {
      Window.new(location, width, height)
    })

    // Other Handlers
  }
}
