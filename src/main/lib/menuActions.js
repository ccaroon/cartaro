import { Notification } from 'electron'
import http from 'axios'
import config from './config'

const PORT = config.get('server:port')

export default {
  FILE: {
    backup: () => {
      http.post(
        `http://127.0.0.1:${PORT}/sys/backup`,
        {
          path: config.get('backup:path'),
          keep: config.get('backup:keep')
        }
      )
        .then(resp => {
          const msg = resp.status === 201 ? resp.data.message : resp.data.error
          // console.log(`Backup Success: ${msg}`)
          new Notification({
            title: 'Backup Success',
            body: msg
          }).show()
        })
        .catch(err => {
          // console.log(`Backup Failed: ${err}`)
          new Notification({
            title: 'Backup Failed',
            body: err
          }).show()
        })
    }
  },
  HELP: {
    github: () => {
      require('electron').shell.openExternal('https://github.com/ccaroon/cartaro')
    }
  }
}
