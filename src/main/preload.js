const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('Main', {
  newWindow: (location, width, height) => {
    ipcRenderer.invoke('main:newWindow', location, width, height)
  }
})

contextBridge.exposeInMainWorld('Config', {
  get: (path, defValue = null, isTransient = false) => {
    return ipcRenderer.invoke('config:get', path, defValue, isTransient)
  },
  instance: () => {
    return ipcRenderer.invoke('config:instance')
  }
})

contextBridge.exposeInMainWorld('NodeJS', { process })

contextBridge.exposeInMainWorld('Modules', {
  vuejs: {
    version: require('vue/package.json').version
  }
})
