import Winston from 'winston'
const path = require('path')
// -----------------------------------------------------------------------------
class Logger {
  static __instance = null

  static init (logDir) {
    if (this.__instance === null) {
      const logSuffix = process.env.NODE_ENV === 'development' ? '-dev' : ''

      this.__instance = Winston.createLogger({
        level: 'info',
        format: Winston.format.combine(
          Winston.format.timestamp({ format: 'YYYY-MM-DD@HH:mm:ss' }),
          Winston.format.uncolorize(),
          Winston.format.json()
        ),
        transports: [
          new Winston.transports.File({
            filename: path.join(logDir, `CartaroLog${logSuffix}.json`)
          })
        ]
      })

      if (process.env.NODE_ENV === 'development') {
        // Log to console when in Dev mode
        this.__instance.add(new Winston.transports.Console({
          format: Winston.format.printf((info) => {
            return `${info.level}: ${info.message}`
          })
        }))
      }
    }
  }

  static getInstance () {
    return this.__instance
  }
}
// -----------------------------------------------------------------------------
export default Logger
