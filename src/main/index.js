'use strict'

import { app, dialog, Menu, BrowserWindow } from 'electron'
import Config from './config'

const PORT = 4242
const http = require('axios')
const fs = require('fs')
const path = require('path')

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = path.join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow, backendServer
const winURL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:9080'
  : `file://${__dirname}/index.html`

const docPath = path.join(app.getPath('documents'), 'Cartaro')

function initApp () {
  // Create data directory
  if (!fs.existsSync(Config.dataPath)) {
    fs.mkdirSync(Config.dataPath, '0750')
  }
}

function quitApp () {
  mainWindow = null
  backendServer.kill()
  app.quit()
}

function createMenu () {
  var mainMetaKey = process.platform === 'darwin' ? 'Cmd' : 'Ctrl'
  // -------------
  var aboutSubMenu = {
    label: 'About Ĉartaro',
    accelerator: mainMetaKey + '+?',
    click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
  }

  // var settingsSubMenu = {
  //   label: process.platform === 'darwin' ? 'Preferences...' : 'Settings...',
  //   accelerator: mainMetaKey + '+,',
  //   click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-settings')
  // }

  const template = [
    // 0
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', accelerator: 'CmdOrCtrl+Z', selector: 'undo:' },
        { label: 'Redo', accelerator: 'Shift+CmdOrCtrl+Z', selector: 'redo:' },
        { type: 'separator' },
        { label: 'Cut', accelerator: 'CmdOrCtrl+X', selector: 'cut:' },
        { label: 'Copy', accelerator: 'CmdOrCtrl+C', selector: 'copy:' },
        { label: 'Paste', accelerator: 'CmdOrCtrl+V', selector: 'paste:' },
        { label: 'Select All', accelerator: 'CmdOrCtrl+A', selector: 'selectAll:' }
      ]
    },
    // 1
    {
      label: 'View',
      submenu: [
        {
          label: 'Main',
          accelerator: mainMetaKey + '+H',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-main')
        }
      ]
    },
    // 2
    {
      role: 'window',
      submenu: [
        { role: 'minimize' }
      ]
    },
    // 3
    {
      role: 'help',
      submenu: [
        {
          label: 'View on GitHub',
          click () { require('electron').shell.openExternal('https://github.com/ccaroon/cartaro') }
        },
        {
          label: 'Dev Tools',
          accelerator: mainMetaKey + '+I',
          click: () => mainWindow.webContents.openDevTools()
        }
      ]
    }
  ]

  if (process.platform === 'darwin') {
    // Add Apple Menu
    template.unshift({
      label: 'Apple Menu',
      submenu: [
        aboutSubMenu,
        { type: 'separator' },
        // settingsSubMenu,
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
  } else {
    // Add About to help menu
    template[3].submenu = template[3].submenu.concat([
      { type: 'separator' },
      aboutSubMenu
    ])

    // Add File Menu
    template.unshift({
      label: 'File',
      submenu: [
        // settingsSubMenu,
        { type: 'separator' },
        { role: 'quit' }
      ]
    })
  }

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
  // -------------
}

// ---------------------------------------------------------------------------
// SEE: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
// ---------------------------------------------------------------------------
function initServer () {
  var basePath = path.resolve(path.dirname(__dirname))
  var cmd = `./bin/python ./bin/flask run -p ${PORT}`

  var serverPath = null
  if (basePath.match(/\/Resources\//i)) {
    // Electron launched as bundled app
    serverPath = path.join(basePath, '../../server/dist')
  } else {
    // Dev Mode
    serverPath = path.join(basePath, '../server/dist')
  }

  var env = {} // process.env
  env.PYTHONPATH = serverPath
  env.FLASK_ENV = process.env.NODE_ENV
  env.FLASK_APP = 'cartaro'
  env.CARTARO_DOC_PATH = docPath
  env.CARTARO_ENV = process.env.NODE_ENV === 'development' ? 'dev' : 'prod'

  backendServer = require('child_process').spawn(
    cmd,
    null,
    { cwd: serverPath, env: env, shell: true }
  )
  console.log(`Server PID: [${backendServer.pid}]`)

  backendServer.stdout.on('data', function (data) {
    console.log(`[STDOUT:${new Date().toLocaleString()}]\n${data.toString('utf8')}`)
  })

  backendServer.stderr.on('data', function (data) {
    console.log(`[STDERR:${new Date().toLocaleString()}]\n${data.toString('utf8')}`)
  })

  backendServer.on('error', function (err) {
    console.log(`[ERROR:${new Date().toLocaleString()}]\n${err.toString('utf8')}`)
  })

  backendServer.on('exit', function (code, signal) {
    if (code) {
      dialog.showMessageBoxSync(null, {
        type: 'error',
        title: 'Backend Server Has Exited',
        message: 'Backend Server Has Exited',
        detail: `Exit Code: [${code}] | Signal: [${signal}]`
      })
      quitApp()
    }
  })
}

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 1000,
    minWidth: 900,
    minHeight: 600,
    useContentSize: true,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true
    }
  })
  createMenu()

  mainWindow.loadURL(winURL)
}

function serverHealthy (resolve, reject, iteration = 1) {
  const MAX = 5

  http.get(`http://localhost:${PORT}/sys/ping`)
    .then(() => {
      console.log(`Server Healthy After ${iteration} Tries.`)
      resolve()
    })
    .catch(() => {
      console.log(`Health Check Failed: ${iteration}/${MAX}`)
      if (iteration > MAX) {
        reject(`Server not healthy after ${MAX} tries.`)
      } else {
        setTimeout(() => {
          serverHealthy(resolve, reject, iteration + 1)
        }, 500)
      }
    })
}

app.on('window-all-closed', () => {
  quitApp()
})

app.on('ready', () => {
  initApp()

  var startServer = new Promise((resolve, reject) => {
    initServer()
    serverHealthy(resolve, reject)
  })

  startServer
    .then(() => {
      createWindow()
      mainWindow.on('closed', () => {
        quitApp()
      })
    })
    .catch(err => {
      console.log(`Failed to start server: ${err}`)
      quitApp()
    })
})
