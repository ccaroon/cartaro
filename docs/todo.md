# ToDo

## Where Am I?
* [ ] 20220925:
  - ...
* [x] 20220924:
  - Server not shutting down on quit
    - [x] File -> Quit             | Does not call quitApp ... app.quit event
    - [x] Ctrl-Q                   | Does not call quitApp ... app.quit event
    - [x] Click Close Window [X]   | Calls quitApp, but kills wrong process `shell: true`
    - [x] Ctrl-W                   | Calls quitApp, but kills wrong process `shell: true`
    - [x] Right-Click Icon -> Quit | Calls quitApp, but kills wrong process `shell: true`
    - [x] Killing the wrong process; the shell parent instead of the python/flask process
      + don't use `shell` and break cmd into cmd & args parts
* [x] 20220918 - Trying to get Config.js functionality available to the Renderer process.
  - Can't just export the entire Class/instance b/c can't import it in preload.js
  - Probably should just expose single methods on a 'Config' ctxBridge

## Electron
* [ ] Integrate OLD menu/actions with new menu
* [x] Config access via IPC
* [ ] `preload.js` only has access to a sub-set of NodeJS
  - 'fs' & 'path', for instance, cannot be used
  - See: https://www.electronjs.org/docs/latest/tutorial/sandbox
* [x] Consistent casing for Class vs Module
* [ ] Can IPC invocations be synchronous?
* [ ] Replace `new-window` event with call to `setWindowOpenHandler`
      - The new-window event is deprecated and will be removed.
        Please use contents.setWindowOpenHandler() instead.

## Server
* [ ] Replace `nose` with `nose2`
  * [x] Update to work with `nose2`
  * [x] Update Makefile
  * [ ] How to get `--cover-min-percentage 95` back
  * [x] Test or Cover a single file
* Package updates?


## Build
* [ ] Bundling of server code. See Seiche
