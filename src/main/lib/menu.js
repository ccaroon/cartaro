import { Menu } from 'electron'
import menuActions from './menuActions'

const mainMetaKey = process.platform === 'darwin' ? 'Cmd' : 'Ctrl'

const aboutSubMenu = {
  label: 'About Ĉartaro',
  accelerator: mainMetaKey + '+?',
  click: () => menuActions.HELP.about()
}

// const settingsSubMenu = {
//     label: process.platform === 'darwin' ? 'Preferences...' : 'Settings...',
//     accelerator: mainMetaKey + '+,',
//     click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-settings')
// }

const template = [
  // 0
  {
    label: 'File',
    submenu: [
      {
        label: 'Backup',
        accelerator: mainMetaKey + '+B',
        click: () => {
          menuActions.FILE.backup()
        }
      }
    ]
  },
  // 1
  {
    label: 'Edit',
    submenu: [
      { label: 'Undo', accelerator: 'CmdOrCtrl+Z', selector: 'undo:' },
      { label: 'Redo', accelerator: 'Shift+CmdOrCtrl+Z', selector: 'redo:' },
      { type: 'separator' },
      { label: 'Cut', accelerator: 'CmdOrCtrl+X', selector: 'cut:' },
      { label: 'Copy', accelerator: 'CmdOrCtrl+C', selector: 'copy:' },
      { label: 'Paste', accelerator: 'CmdOrCtrl+V', selector: 'paste:' },
      { label: 'Select All', accelerator: 'CmdOrCtrl+A', selector: 'selectAll:' }
    ]
  },
  // 2
  {
    label: 'View',
    submenu: [
      {
        label: 'Main',
        accelerator: mainMetaKey + '+H',
        click: () => menuActions.VIEW.main()
      }
    ]
  },
  // 3
  {
    role: 'window',
    submenu: [
      { role: 'minimize' }
    ]
  },
  // 4
  {
    role: 'help',
    submenu: [
      {
        label: 'View on GitHub',
        click: () => menuActions.HELP.github()
      },
      {
        label: 'Dev Tools',
        accelerator: mainMetaKey + '+I',
        click: () => menuActions.HELP.devtools()
      }
    ]
  }
]

export default {
  attach: function () {
    if (process.platform === 'darwin') {
      // Add Apple Menu
      template.unshift({
        label: 'Apple Menu',
        submenu: [
          aboutSubMenu,
          { type: 'separator' },
          // settingsSubMenu,
          { type: 'separator' },
          { role: 'quit' }
        ]
      })
    } else {
      // Add Quit to File menu
      template[0].submenu = template[0].submenu.concat(
        [
          { type: 'separator' },
          { role: 'quit' }
        ]
      )

      // Add About to help menu
      template[4].submenu = template[4].submenu.concat(
        [
          { type: 'separator' },
          aboutSubMenu
        ]
      )
    }

    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
  }
}
