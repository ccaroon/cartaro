import { app } from 'electron'
import path from 'path'

export default {
  docPath: path.join(app.getPath('documents'), 'Cartaro'),
  window: {
    width: 1280,
    height: 1000,
    minWidth: 900,
    minHeight: 600
  }
}
