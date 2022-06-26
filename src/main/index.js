'use strict'

import fs from 'fs'
import path from 'path'

import { app, ipcMain, BrowserWindow } from 'electron'

import Config from '../Config'
import Settings from './Settings'
import Logger from './Logger'
import Menu from './Menu'
import EmbeddedServer from './EmbeddedServer'
import ExternalServer from './ExternalServer'

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

  // Properties to be used when Electron open a new browser window
  // b/c of a `target=_blank` or `window.open`
  mainWindow.webContents.setWindowOpenHandler(() => {
    return {
      action: 'allow',
      overrideBrowserWindowOptions: {
        parent: mainWindow,
        fullscreenable: false,
        webPreferences: {
          devTools: false
        },
        autoHideMenuBar: true,
        width: Settings.childWindow.width,
        height: Settings.childWindow.height
      }
    }
  })

  mainWindow.on('closed', () => {
    quitApp()
  })
  mainWindow.loadURL(winURL)
}
// -----------------------------------------------------------------------------
function quitApp () {
  mainWindow = null

  if (Config.get('server:mode', 'embedded') === 'embedded') {
    logger.info(`Shutting Down! Server PID: [${EmbeddedServer.pid()}]`)
    EmbeddedServer.stop()
  }

  app.quit()
}
// -----------------------------------------------------------------------------
// "Main"
// -----------------------------------------------------------------------------
app.on('ready', () => {
  initApp()

  if (Config.get('server:mode', 'embedded') === 'embedded') {
    EmbeddedServer.start()
      .then(() => {
        createWindow()
      })
      .catch((err) => {
        logger.error(`Failed to start server: ${err}`)
        quitApp()
      })
  } else {
    logger.info('"server:mode" set to "external". Waiting for Server to become available.')
    createWindow()
    ExternalServer.start(mainWindow)
  }
})
