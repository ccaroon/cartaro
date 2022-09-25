import http from 'axios'
import path from 'path'

import { dialog } from 'electron'

import config from './Config'
import Logger from './Logger'
import settings from './settings'
// -----------------------------------------------------------------------------
class Server {
  constructor (docPath, port, hcTries, hcSleep, logger = null) {
    this.__docPath = docPath
    this.__port = port
    this.__healthCheckTries = hcTries
    this.__healthCheckSleep = hcSleep
    this.__logger = logger
    this.__process = null
  }

  __log (level, msg) {
    if (this.__logger) {
      this.__logger.log(level, msg)
    }
  }

  __start () {
    const self = this
    const basePath = path.resolve(path.dirname(__dirname))

    // Default for DEV mode
    let serverPath = path.join(basePath, './server/dist')
    // Electron launched as bundled app
    // TODO: is the serverPath correct?
    if (basePath.match(/\/Resources/i)) {
      serverPath = path.join(basePath, './server/dist')
    }

    const env = {}
    env.PYTHONPATH = serverPath
    env.FLASK_ENV = process.env.NODE_ENV
    env.FLASK_APP = 'cartaro'
    env.CARTARO_DOC_PATH = this.__docPath
    env.CARTARO_ENV = process.env.NODE_ENV === 'development' ? 'dev' : 'prod'

    // SEE: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
    this.__process = require('child_process').spawn(
      './bin/python',
      ['./bin/flask', 'run', '-p', this.__port],
      { cwd: serverPath, env }
    )
    this.__log('info', `Server PID: [${this.__process.pid}]`)

    this.__process.stdout.on('data', function (data) {
      self.__log('info', data.toString('utf8'))
    })

    this.__process.stderr.on('data', function (data) {
      self.__log('info', data.toString('utf8'))
    })

    this.__process.on('error', function (err) {
      self.__log('error', err.toString('utf8'))
    })

    this.__process.on('exit', function (code, signal) {
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

  __waitTilHealthy (resolve, reject, iteration = 1) {
    const self = this

    this.ping()
      .then(() => {
        self.__log('info', `Server Healthy After ${iteration} Tries.`)
        resolve()
      })
      .catch(() => {
        self.__log('error', `Health Check Failed: ${iteration}/${self.__healthCheckTries}`)
        if (iteration > self.__healthCheckTries) {
          reject(`Server not healthy after ${self.__healthCheckTries} tries.`)
        } else {
          setTimeout(() => {
            self.__waitTilHealthy(resolve, reject, iteration + 1)
          }, self.__healthCheckSleep)
        }
      })
  }

  start () {
    const self = this
    if (this.__process == null) {
      return new Promise((resolve, reject) => {
        self.__start()
        self.__waitTilHealthy(resolve, reject)
      })
    }
  }

  stop () {
    if (this.__process) {
      this.__process.kill()
    }
  }

  pid () {
    return this.__process.pid
  }

  ping () {
    return http.get(`http://localhost:${this.__port}/sys/ping`)
  }
}
// -----------------------------------------------------------------------------
const PORT = config.get('serverPort', 4242)
const defaultServer = new Server(settings.docPath, PORT, 5, 1000, new Logger())
export default {
  instance: defaultServer
}
