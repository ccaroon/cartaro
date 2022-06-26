import { app } from 'electron'
import path from 'path'

import Config from '../Config'

const windowSettings = Config.get('window', {
  width: 1600,
  height: 900
})
const windowWidth = windowSettings.width
const windowHeight = windowSettings.height

export default {
  docPath: path.join(app.getPath('documents'), 'Cartaro'),
  window: {
    width: windowWidth,
    height: windowHeight,
    minWidth: 1280,
    minHeight: 720
  },
  childWindow: {
    width: windowWidth * 0.75,
    height: windowHeight * 0.75
  }
}
