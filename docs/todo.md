# ToDo

## Where Am I?
* 20220918 - Trying to get Config.js functionality available to the Renderer process.

## Electron
* [ ] Integrate OLD menu/actions with new menu
* [ ] Config access via IPC
* [ ] `preload.js` only has access to a sub-set of NodeJS
  - 'fs' & 'path', for instance, cannot be used
  - See: https://www.electronjs.org/docs/latest/tutorial/sandbox

## Server
* [ ] Replace `nose` with `nose2`
  * [x] Update to work with `nose2`
  * [x] Update Makefile
  * [ ] How to get `--cover-min-percentage 95` back
  * [x] Test or Cover a single file
* Package updates?


## Build
* [ ] Bundling of server code. See Seiche
