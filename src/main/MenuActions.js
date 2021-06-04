import { BrowserWindow } from 'electron'

import http from 'axios'
import Config from '../Config'

const PORT = Config.get('serverPort', 4242)

export default {
  FILE: {
    backup: () => {
      http.post(
        `http://localhost:${PORT}/sys/backup`,
        {
          path: Config.get('backup:path'),
          keep: Config.get('backup:keep')
        }
      )
        .then(resp => {
          const msg = resp.status === 201 ? resp.data.message : resp.data.error
          BrowserWindow.getFocusedWindow().webContents.send('app-show-notification', {
            icon: 'mdi-database-check',
            color: 'green',
            message: msg,
            timeout: 5000
          })
        })
        .catch(err => {
          BrowserWindow.getFocusedWindow().webContents.send('app-show-notification', {
            icon: 'mdi-database-remove',
            color: 'red',
            message: err,
            timeout: -1
          })
        })
    }
  },
  VIEW: {
    main: () => {
      BrowserWindow.getFocusedWindow().webContents.send('menu-view-main')
    }
  },
  HELP: {
    about: () => {
      BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
    },
    devtools: () => {
      BrowserWindow.getFocusedWindow().webContents.openDevTools()
    },
    github: () => {
      require('electron').shell.openExternal('https://github.com/ccaroon/cartaro')
    }
  }
}
