import http from 'axios'
import path from 'path'

import { dialog } from 'electron'

import Config from '../Config'
import Logger from './Logger'
import Settings from './Settings'
// -----------------------------------------------------------------------------
class Server {
  static __instance = null

  static PORT = Config.get('serverPort', 4242)
  static LOGGER = Logger.getInstance()
  static HEALTHCHECK_TRIES = 5
  static HEALTHCHECK_SLEEP = 750
  static COMMAND = `./bin/python ./bin/flask run -p ${Server.PORT}`

  static __start () {
    const self = this
    const basePath = path.resolve(path.dirname(__dirname))
    let serverPath = null

    if (basePath.match(/\/Resources\//i)) {
      // Electron launched as bundled app
      serverPath = path.join(basePath, '../../server/dist')
    } else {
      // Dev Mode
      serverPath = path.join(basePath, '../server/dist')
    }

    const env = {} // process.env
    env.PYTHONPATH = serverPath
    env.FLASK_ENV = process.env.NODE_ENV
    env.FLASK_APP = 'cartaro'
    env.CARTARO_DOC_PATH = Settings.docPath
    env.CARTARO_ENV = process.env.NODE_ENV === 'development' ? 'dev' : 'prod'

    // SEE: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
    this.__instance = require('child_process').spawn(
      this.COMMAND,
      null,
      { cwd: serverPath, env: env, shell: true }
    )
    this.LOGGER.info(`Server PID: [${this.__instance.pid}]`)

    this.__instance.stdout.on('data', function (data) {
      self.LOGGER.info(data.toString('utf8'))
    })

    this.__instance.stderr.on('data', function (data) {
      self.LOGGER.info(data.toString('utf8'))
    })

    this.__instance.on('error', function (err) {
      self.LOGGER.error(err.toString('utf8'))
    })

    this.__instance.on('exit', function (code, signal) {
      if (code) {
        dialog.showMessageBoxSync(null, {
          type: 'error',
          title: 'Backend Server Has Exited',
          message: 'Backend Server Has Exited',
          detail: `Exit Code: [${code}] | Signal: [${signal}]`
        })
        self.__instance = null
      }
    })
  }

  static __waitTilHealthy (resolve, reject, iteration = 1) {
    const self = this

    this.ping()
      .then(() => {
        self.LOGGER.info(`Server Healthy After ${iteration} Tries.`)
        resolve()
      })
      .catch(() => {
        self.LOGGER.error(`Health Check Failed: ${iteration}/${self.HEALTHCHECK_TRIES}`)
        if (iteration > self.HEALTHCHECK_TRIES) {
          reject(`Server not healthy after ${self.HEALTHCHECK_TRIES} tries.`)
        } else {
          setTimeout(() => {
            self.__waitTilHealthy(resolve, reject, iteration + 1)
          }, self.HEALTHCHECK_SLEEP)
        }
      })
  }

  static start () {
    const self = this
    if (this.__instance == null) {
      return new Promise((resolve, reject) => {
        self.__start()
        self.__waitTilHealthy(resolve, reject)
      })
    }
  }

  static stop () {
    if (this.__instance) {
      this.__instance.kill()
    }
  }

  static pid () {
    return this.__instance.pid
  }

  static ping () {
    return http.get(`http://localhost:${this.PORT}/sys/ping`)
  }
}
// -----------------------------------------------------------------------------
export default Server
