'use strict'

import { app, ipcMain, protocol, screen, BrowserWindow, Menu, MenuItem } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS_DEVTOOLS } from 'electron-devtools-installer'

import fs from 'fs'
import path from 'path'

import settings from './lib/settings'
import ipc from './lib/ipc'
import Logger from './lib/Logger'
import Server from './lib/Server'
import windowHelper from './lib/windowHelper'

// -----------------------------------------------------------------------------
let mainWindow = null
const logger = new Logger()
const server = Server.instance

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

// -----------------------------------------------------------------------------
function initApp () {
  logger.info('Initializing App...')
  // Create data directory
  if (!fs.existsSync(settings.docPath)) {
    fs.mkdirSync(settings.docPath, '0750')
  }

  ipcMain.on('app-show-notification', (event, args) => {
    mainWindow.webContents.send('app-show-notification', args)
  })

  app.on('window-all-closed', () => {
    quitApp()
  })
}

// -----------------------------------------------------------------------------
function quitApp () {
  logger.info(`Shutting Down! Server PID: [${server.pid()}]`)
  mainWindow = null
  server.stop()
  app.quit()
}

// -----------------------------------------------------------------------------
async function createWindow () {
  logger.info('Creating Main Window...')
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

  // Add Context Menu
  const menu = new Menu()
  menu.append(new MenuItem({
    label: 'Copy',
    role: 'copy'
  }))
  menu.append(new MenuItem({
    label: 'Paste',
    role: 'paste'
  }))
  menu.append(new MenuItem({
    type: 'separator'
  }))
  menu.append(new MenuItem({
    label: 'Dev Tools',
    role: 'toggleDevTools'
  }))

  mainWindow.webContents.on('context-menu',
    (event, click) => {
      event.preventDefault()
      menu.popup(mainWindow.webContents)
    },
    false
  )

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
  mainWindow.webContents.on('new-window', function (event, url) {
    event.preventDefault()
    // shell.openExternal(url) // Open in system default browser
    windowHelper.new(url)
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
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }

  initApp()

  // createWindow()
  // ipc.registerHandlers()

  server.start()
    .then(() => {
      createWindow()
      ipc.registerHandlers()
    })
    .catch((err) => {
      logger.error(`Failed to start server: ${err}`)
      quitApp()
    })
})
// -----------------------------------------------------------------------------
// Exit cleanly on request from parent process in development mode.
// -----------------------------------------------------------------------------
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        quitApp()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      quitApp()
    })
  }
}
