// https://www.electronjs.org/docs/latest/api/menu
import { clipboard, BrowserWindow, Menu, MenuItem } from 'electron'
import menuActions from './menuActions'

const appName = 'Ĉartaro'
const isMac = process.platform === 'darwin'
const mainMetaKey = isMac ? 'Cmd' : 'Ctrl'
// -----------------------------------------------------------------------------
const aboutMenu = {
  label: `About ${appName}`,
  click: () => BrowserWindow.getFocusedWindow().webContents.send('menu-help-about')
}

const macApp = [
  {
    label: appName,
    submenu: [
      aboutMenu,
      { type: 'separator' },
      { role: 'hide' },
      { role: 'hideOthers' },
      { role: 'unhide' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  }]

// const macWindow = [
//   { type: 'separator' },
//   { role: 'front' },
//   { type: 'separator' },
//   { role: 'window' }
// ]

// const macEdit = [
//   { role: 'pasteAndMatchStyle' },
//   { role: 'delete' },
//   { role: 'selectAll' },
//   { type: 'separator' },
//   {
//     label: 'Speech',
//     submenu: [
//       { role: 'startSpeaking' },
//       { role: 'stopSpeaking' }
//     ]
//   }
// ]
// -----------------------------------------------------------------------------
// https://www.electronjs.org/docs/latest/api/menu#menuitems
const template = [
  // { role: 'appMenu' }
  ...(isMac ? macApp : []),
  // { role: 'fileMenu' }
  {
    label: 'File',
    submenu: [
      {
        label: 'Backup',
        accelerator: mainMetaKey + '+B',
        click: () => {
          menuActions.FILE.backup()
        }
      },
      ...(isMac ? [] : [{ role: 'quit' }])
    ]
  },
  { role: 'editMenu' },
  // {
  //   label: 'Edit',
  //   submenu: [
  //     { role: 'undo' },
  //     { role: 'redo' },
  //     { type: 'separator' },
  //     { role: 'cut' },
  //     { role: 'copy' },
  //     { role: 'paste' },
  //     ...(isMac ? macEdit : [{ role: 'selectAll' }])
  //   ]
  // },
  // { role: 'viewMenu' }
  {
    label: 'View',
    submenu: [
      { role: 'resetZoom' },
      { role: 'zoomIn' },
      { role: 'zoomOut' },
      { type: 'separator' },
      { role: 'togglefullscreen' }
    ]
  },
  { role: 'windowMenu' },
  // {
  //   label: 'Window',
  //   submenu: [
  //     { role: 'minimize' },
  //     { role: 'zoom' },
  //     ...(isMac ? macWindow : [{ role: 'close' }])
  //   ]
  // },
  {
    role: 'help',
    submenu: [
      ...(isMac ? [] : [aboutMenu]),
      {
        label: 'View on GitHub',
        click: () => menuActions.HELP.github()
      },
      { role: 'toggleDevTools' }
    ]
  }
]
// -----------------------------------------------------------------------------
export default {
  setApplicationMenu: function () {
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
  },
  addContext: function (window) {
    const ctxMenu = new Menu()
    let clickTarget = null
    ctxMenu.append(new MenuItem({
      label: 'Copy',
      role: 'copy'
    }))
    ctxMenu.append(new MenuItem({
      id: 'ctx-copy-link',
      label: 'Copy Link',
      click: () => {
        clipboard.writeText(clickTarget.linkURL)
      }
    }))
    ctxMenu.append(new MenuItem({
      label: 'Paste',
      role: 'paste'
    }))
    ctxMenu.append(new MenuItem({
      type: 'separator'
    }))
    ctxMenu.append(new MenuItem({
      label: 'Dev Tools',
      role: 'toggleDevTools'
    }))

    window.webContents.on('context-menu',
      (event, target) => {
        clickTarget = target
        event.preventDefault()

        // Don't show "Copy Link" if target is not a link
        const copyLinkItem = ctxMenu.getMenuItemById('ctx-copy-link')
        if (clickTarget && clickTarget.linkURL.length > 0) {
          copyLinkItem.visible = true
        } else {
          copyLinkItem.visible = false
        }

        ctxMenu.popup(window.webContents)
      },
      false
    )
  }
}
