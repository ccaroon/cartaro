import { app } from 'electron'
import path from 'path'

export default {
  docPath: path.join(app.getPath('documents'), 'Cartaro'),
  window: {
    width: 1680,
    height: 1250,
    minWidth: 900,
    minHeight: 600
  },
  childWindow: {
    width: 1200,
    height: 900
  }
}
