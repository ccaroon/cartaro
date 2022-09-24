import { app } from 'electron'
import path from 'path'

export default {
  docPath: path.join(app.getPath('documents'), 'Cartaro')
}
