'use strict'

import { app, ipcMain, protocol, screen, BrowserWindow } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'

import fs from 'fs'
import path from 'path'

import ipc from './lib/ipc'
import Logger from './lib/Logger'
import menu from './lib/menu'
import Server from './lib/Server'
import settings from './lib/settings'
import windowHelper from './lib/windowHelper'

// -----------------------------------------------------------------------------
let mainWindow = null
const logger = new Logger('debug')
const server = Server.instance

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

// -----------------------------------------------------------------------------
function initApp () {
  logger.debug('Initializing App...')
  // Create data directory
  if (!fs.existsSync(settings.docPath)) {
    fs.mkdirSync(settings.docPath, '0750')
  }

  ipcMain.on('app-show-notification', (event, args) => {
    mainWindow.webContents.send('app-show-notification', args)
  })

  app.on('quit', () => {
    logger.debug('App Event: quit')
    quitApp()
  })

  app.on('window-all-closed', () => {
    logger.debug('App Event: window-all-closed')
    app.quit()
  })
}

// -----------------------------------------------------------------------------
function quitApp () {
  logger.info(`Shutting Down! Server PID: [${server.pid()}]`)
  mainWindow = null
  server.stop()
}

// -----------------------------------------------------------------------------
async function createWindow () {
  logger.debug('Creating Main Window...')
  const display = screen.getPrimaryDisplay()

  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: display.size.width * 0.70,
    height: display.size.height * 0.90,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),

      // Use vue.config.js#pluginOptions.nodeIntegration & leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    }
  })

  // Application Menu
  menu.setApplicationMenu()

  // Add Context Menu
  menu.addContext(mainWindow)

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await mainWindow.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    // if (!process.env.IS_TEST) mainWindow.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    mainWindow.loadURL('app://./index.html')
  }

  // Links that open new windows on target="_blank" use this
  mainWindow.webContents.setWindowOpenHandler((details) => {
    // Open a new window like **we** want
    windowHelper.new(details.url)
    // Prevent the default window from opening.
    return { action: 'deny' }
  })
}
// -----------------------------------------------------------------------------
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
// -----------------------------------------------------------------------------
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS_DEVTOOLS)
    } catch (e) {
      logger.error('Vue Devtools failed to install:', e.toString())
    }
  }

  initApp()

  server.start()
    .then(() => {
      createWindow()
      ipc.registerHandlers()
    })
    .catch((err) => {
      logger.error(`Failed to start server: ${err}`)
      app.quit()
    })
})
// -----------------------------------------------------------------------------
// Exit cleanly on request from parent process in development mode.
// -----------------------------------------------------------------------------
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
