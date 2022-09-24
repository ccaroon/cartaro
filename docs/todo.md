# ToDo

## Where Am I?
* [ ] 20220924 -
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

## Server
* [ ] Replace `nose` with `nose2`
  * [x] Update to work with `nose2`
  * [x] Update Makefile
  * [ ] How to get `--cover-min-percentage 95` back
  * [x] Test or Cover a single file
* Package updates?


## Build
* [ ] Bundling of server code. See Seiche
