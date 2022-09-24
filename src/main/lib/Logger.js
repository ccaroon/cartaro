import path from 'path'

import Winston from 'winston'
import settings from './settings'
// -----------------------------------------------------------------------------
class Logger {
  constructor () {
    const logSuffix = process.env.NODE_ENV === 'development' ? '-dev' : ''

    this.__winston = Winston.createLogger({
      level: 'info',
      format: Winston.format.combine(
        Winston.format.timestamp({ format: 'YYYY-MM-DD@HH:mm:ss' }),
        Winston.format.uncolorize(),
        Winston.format.json()
      ),
      transports: [
        new Winston.transports.File({
          filename: path.join(settings.docPath, `CartaroLog${logSuffix}.json`)
        })
      ]
    })

    if (process.env.NODE_ENV === 'development') {
      // Log to console when in Dev mode
      this.__winston.add(new Winston.transports.Console({
        format: Winston.format.printf((info) => {
          return `${info.level}: ${info.message}`
        })
      }))
    }
  }

  log (level, msg) {
    this.__winston.log(level, msg)
  }

  error (msg) {
    this.log('error', msg)
  }

  info (msg) {
    this.log('info', msg)
  }
}
// -----------------------------------------------------------------------------
export default Logger
