'use strict'

import fs from 'fs'
import path from 'path'

import { app, ipcMain, BrowserWindow } from 'electron'

import Settings from './Settings'
import Logger from './Logger'
import Menu from './Menu'
import Server from './Server'

require('@electron/remote/main').initialize()
// -----------------------------------------------------------------------------
const logger = Logger.getInstance()

let mainWindow = null
let winURL = null
if (process.env.NODE_ENV === 'development') {
  winURL = 'http://localhost:9080'
} else {
  winURL = `file://${path.join(__dirname, 'index.html')}`
  global.__static = path.join(__dirname, '/static').replace(/\\/g, '\\\\')
}
// -----------------------------------------------------------------------------
function initApp () {
  // Create data directory
  if (!fs.existsSync(Settings.docPath)) {
    fs.mkdirSync(Settings.docPath, '0750')
  }

  ipcMain.on('app-show-notification', (event, args) => {
    mainWindow.webContents.send('app-show-notification', args)
  })

  app.on('window-all-closed', () => {
    quitApp()
  })
}
// -----------------------------------------------------------------------------
function createWindow () {
  mainWindow = new BrowserWindow({
    width: Settings.window.width,
    height: Settings.window.height,
    minWidth: Settings.window.minWidth,
    minHeight: Settings.window.minHeight,
    useContentSize: true,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
      // TODO: Code does not run w/o this. Can't figure out what I need to
      //       change to be able to turn this OFF.
      contextIsolation: false
    }
  })
  Menu.attach()

  mainWindow.on('closed', () => {
    quitApp()
  })
  mainWindow.loadURL(winURL)
}
// -----------------------------------------------------------------------------
function quitApp () {
  logger.info(`Shutting Down! Server PID: [${Server.pid()}]`)
  mainWindow = null
  Server.stop()
  app.quit()
}
// -----------------------------------------------------------------------------
// "Main"
// -----------------------------------------------------------------------------
app.on('ready', () => {
  initApp()

  Server.start()
    .then(() => {
      createWindow()
    })
    .catch((err) => {
      logger.error(`Failed to start server: ${err}`)
      quitApp()
    })
})
