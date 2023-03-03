const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('Main', {
  newWindow: (location, width, height) => {
    ipcRenderer.invoke('main:newWindow', location, width, height)
  }
})

contextBridge.exposeInMainWorld('Config', {
  // get: (path, defValue = null, isTransient = false) => {
  //   return ipcRenderer.invoke('config:get', path, defValue, isTransient)
  // },
  data: () => {
    return ipcRenderer.invoke('config:data')
  }
})

contextBridge.exposeInMainWorld('NodeJS', { process })

// Menu Action Handler Registration
contextBridge.exposeInMainWorld('Menu', {
  registerHandler: (menuId, callback) => ipcRenderer.on(menuId, callback)
})
