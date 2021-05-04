import { Menu, BrowserWindow } from 'electron'

const mainMetaKey = process.platform === 'darwin' ? 'Cmd' : 'Ctrl'

const aboutSubMenu = {
  label: 'About Ĉartaro',
  accelerator: mainMetaKey + '+?',
  click: () => {
    BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
  }
}

// const settingsSubMenu = {
//     label: process.platform === 'darwin' ? 'Preferences...' : 'Settings...',
//     accelerator: mainMetaKey + '+,',
//     click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-settings')
// }

const template = [
  // 0
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
  // 1
  {
    label: 'View',
    submenu: [
      {
        label: 'Main',
        accelerator: mainMetaKey + '+H',
        click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-view-main')
      }
    ]
  },
  // 2
  {
    role: 'window',
    submenu: [
      { role: 'minimize' }
    ]
  },
  // 3
  {
    role: 'help',
    submenu: [
      {
        label: 'View on GitHub',
        click () { require('electron').shell.openExternal('https://github.com/ccaroon/cartaro') }
      },
      {
        label: 'Dev Tools',
        accelerator: mainMetaKey + '+I',
        click: () => BrowserWindow.getFocusedWindow().webContents.openDevTools()
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
      // Add About to help menu
      template[3].submenu = template[3].submenu.concat([
        { type: 'separator' },
        aboutSubMenu
      ])

      // Add File Menu
      template.unshift({
        label: 'File',
        submenu: [
          // settingsSubMenu,
          { type: 'separator' },
          { role: 'quit' }
        ]
      })
    }

    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
  }
}
