'use strict'

import { app, Menu, BrowserWindow } from 'electron'

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
      label: 'View',
      submenu: [
        {
          label: 'Main',
          accelerator: mainMetaKey + '+H',
          click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-main')
        }
      ]
    },
    // 1
    {
      role: 'window',
      submenu: [
        { role: 'minimize' }
      ]
    },
    // 2
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
    template[2].submenu = template[2].submenu.concat([
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

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 928,
    minWidth: 900,
    minHeight: 600,
    useContentSize: true,
    webPreferences: {
      nodeIntegration: true
      // preload: path.join(app.getAppPath(), 'main.js')
    }
  })

  createMenu()

  mainWindow.loadURL(winURL)

  // ---------------------------------------------------------------------------
  // SEE: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
  // ---------------------------------------------------------------------------

  // var serverPath = path.join(__dirname, '/server')
  var serverPath = '/Users/ccaroon/src/github/cartaro/server'
  var cmd = './server.sh'
  // var args = ['run', '-p 4242']
  var env = {
    CARTARO_DOC_PATH: docPath
  }
  backendServer = require('child_process').spawn(
    cmd,
    null,
    { cwd: serverPath, env: env }
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

  mainWindow.on('closed', () => {
    mainWindow = null
    backendServer.kill()
  })
}

app.on('ready', () => {
  initApp()
  createWindow()
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
