'use strict'

import { app, BrowserWindow } from 'electron'

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
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

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

  mainWindow.loadURL(winURL)

  // ---------------------------------------------------------------------------
  // SEE: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
  // ---------------------------------------------------------------------------

  // var serverPath = path.join(__dirname, '/server')
  var serverPath = '/Users/ccaroon/src/github/cartaro/server'
  var cmd = './server.sh'
  // var args = ['run', '-p 4242']
  // var env = {
  //   FLASK_APP: 'cartaro-server.py'
  // }
  backendServer = require('child_process').spawn(
    cmd,
    null,
    { cwd: serverPath }
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

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  backendServer.kill()
  app.quit()
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
