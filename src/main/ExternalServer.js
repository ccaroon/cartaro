import http from 'axios'

import { dialog } from 'electron'

import Config from '../Config'
import Logger from './Logger'
// -----------------------------------------------------------------------------
class ExternalServer {
  static __instance = null

  static PORT = Config.get('server:port', 4242)
  static LOGGER = Logger.getInstance()
  static HEARTBEAT_INTERVAL = 1000 * 5

  static __heartBeat (mainWindow) {
    const self = this

    this.ping()
      .then(() => {
        setTimeout(() => {
          self.__heartBeat(mainWindow)
        }, self.HEARTBEAT_INTERVAL)
      })
      .catch(() => {
        self.LOGGER.error('Server Heartbeat failed.')
        const buttonId = dialog.showMessageBoxSync(null, {
          type: 'info',
          title: 'Server Not Detected',
          message: 'Heartbeat failed to detect the external Cartaro Server',
          detail: 'Please start the Cartaro Server',
          buttons: ['Try Again', 'Quit']
        })

        if (buttonId === 0) {
          self.__heartBeat(mainWindow)
        } else if (buttonId === 1) {
          mainWindow.close()
        }
      })
  }

  static start (mainWindow) {
    this.__heartBeat(mainWindow)
  }

  static ping () {
    return http.get(`http://localhost:${this.PORT}/sys/ping`)
  }
}
// -----------------------------------------------------------------------------
export default ExternalServer
