import http from 'axios'
import config from './config'

const PORT = config.get('serverPort', 4242)

export default {
  FILE: {
    backup: () => {
      http.post(
        `http://localhost:${PORT}/sys/backup`,
        {
          path: config.get('backup:path'),
          keep: config.get('backup:keep')
        }
      )
        .then(resp => {
          const msg = resp.status === 201 ? resp.data.message : resp.data.error
          // TODO: Dialog to notify
          console.log(`Backup Success: ${msg}`)
        })
        .catch(err => {
          // TODO: Dialog to notify
          console.log(`Backup Failed: ${err}`)
        })
    }
  },
  HELP: {
    github: () => {
      require('electron').shell.openExternal('https://github.com/ccaroon/cartaro')
    }
  }
}
