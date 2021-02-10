'use strict'

import { app, dialog, Menu, BrowserWindow } from 'electron'

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
  if (!fs.existsSync(docPath)) {
    fs.mkdirSync(docPath, '0750')
  }
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
  var cmd = './bin/python ./bin/flask run -p 4242'

  var serverPath = null
  if (basePath.match(/\/Resources/)) {
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

  if (!backendServer.pid) {
    dialog.showMessageBoxSync(mainWindow, {
      type: 'error',
      title: 'Backend Server Failed to Start',
      message: 'Backend Server Failed to Start',
      detail: `Command: [${serverPath}/${cmd}]`
    })
  }

  // var msg = `__dirname: ${__dirname}\n\nbasePath: ${basePath}\n\nserverPath: ${serverPath}\n\nPID: ${backendServer.pid}`
  // dialog.showMessageBoxSync(mainWindow, {
  //   type: 'info',
  //   message: 'Path Information',
  //   detail: msg
  // })

  backendServer.stdout.on('data', function (data) {
    console.log(`[STDOUT:${new Date().toLocaleString()}]\n${data.toString('utf8')}`)
  })

  backendServer.stderr.on('data', function (data) {
    console.log(`[STDERR:${new Date().toLocaleString()}]\n${data.toString('utf8')}`)
  })

  backendServer.on('error', function (err) {
    console.log(`[ERROR:${new Date().toLocaleString()}]\n${err.toString('utf8')}`)
  })

  mainWindow.on('closed', () => {
    mainWindow = null
    backendServer.kill()
  })
}

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 1000,
    minWidth: 900,
    minHeight: 600,
    useContentSize: true,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true
      // preload: path.join(app.getAppPath(), 'main.js')
    }
  })
  createMenu()

  mainWindow.loadURL(winURL)
  // mainWindow.webContents.openDevTools()
}

app.on('ready', () => {
  initApp()
  createWindow()

  // MUST be done *after* createWindow b/c it depends on `mainWindow`
  initServer()
})

app.on('window-all-closed', () => {
  backendServer.kill()
  app.quit()
})

app.on('activate', () => {
  createMenu()
  if (mainWindow === null) {
    createWindow()
  }
})
