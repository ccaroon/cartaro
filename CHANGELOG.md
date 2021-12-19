# CHANGELOG

## UNRELEASED: v1.5.0 - Cartographer - 2021-??-??
### Added
* Ability for the server to back up the data files
  - `utils/archive.py`
  - `/sys/backup` end point on the `system.py` controller
* File menu added to UI
* File -> Backup added to UI. Calls the `/sys/backup` API endpoint.
* Added the item count to the various lists on the Home Screen (Tickets, Todos, Notes & Entries)
* Added "Erase" button to ScratchPad AppBar -- Erases the active tab
* Added "Edit" & "Snooze" buttons to Todos on Home Screen
* Added "Build Date" to About dialog
* Added a few convenience methods to the Countdown class

### Changed
* Maximized the height of the editor for LogEntries and Notes
* Clicking a Todo on the Home Screen now views it instead of editing it.
* Work Day Calendar now shows an emoji for the day type instead of a 3-letter code.
* Added a few new icons
* Improvements to Icon searching
* Note icons are now first based on the title, then the tags
* Work Day Calendar "edit" pop-up now emphasizes the Close button instead of Delete
* If the same WorkDay has multiple entries, the Home Screen will now show them
  listed under the same day instead of multiple entries in the list.
* The WorkDay list Weekly Total on the Home Screen now show hours worked and
  hours not worked.
* New entries created on the WorkDay Calendar by clicking the Date number will
  have "EDIT ME" in the note field.
* Reduced the height of the Log Entries list on the Home Screen and increased
  the number of entries it loads from 10 to 25.
* Added a ToolTip to each of the Countdowns on the Home Screen
  - Appears when you hover over the icon

### Fixed
...

### Deprecated
...

### Removed
* `yarn` is no longer supported. Just use `npm`

### Security
...

### Misc
* Lots of minor module updates
  - electron, vue, vuetify, etc.
* Updated to use Python 3.9.x
* Updated a bunch of python requirements to the latest versions
  - `arrow` 1.2.1 has some breaking changes from 0.17.0
    - `.timestamp` properly became a method and returned a float
    - Updated the code to use `.int_timestamp`

--------------------------------------------------------------------------------

## v1.4.0 - Ouroboros - 2021-05-21
### Added
* Script to purge empty and unused tags: `server/bin/prune-tags.py`
  - `CARTARO_ENV=dev|prod CARTARO_DOC_PATH=~/... bin/prune-tags.py`

### Changed
* Added AppBar to dialogs for Editors and Viewers
  - Moved "Close" button to an "X" in the app bar
  - Moved dialog title to app bar
  - Generally nicer looking dialogs
* WorkDays are now represented by a monthly calendar
* Updated the look of the WorkDays on Home screen
  - Tightened up a bit
  - Only show hours if a normal day
  - Show time in and time out
  - Show note for non-normal days
* Allow for multiple Notifications to be displayed at one time.

### Fixed
* Links in Markdown now open in a new browser window
  - previously they would take over the main window
  - new windows are child windows of the main window

### Deprecated
...

### Removed
...

### Security
...

### Misc
* Updated lots of node modules including...
  - electron & electron/remote
  - eslint
  - vuetify
  - markdown-it
  - etc...

--------------------------------------------------------------------------------

## v1.3.0 - Anaximenes - 2021-05-04
### Added
* ScratchPad
  - An tabbed editor to quickly save scratch work or copy/pasted snippets
  - Saved to local storage.
  - Cmd/Ctrl-S: save the active scratch pad
  - Cmd/Ctrl-<n>: switch to scratch pad #n
  - Tab number changes color when content has changed
  - A tab can be converted to a Note
* Pageable item screens (LogEntries, Notes, etc) can be paged using the `left` & `right` arrow keys.
* New Secret type "BLOT" - BLock Of Text.
    - can be used to store things like licenses, SSH keys, etc.
* Can now specify a `group_by` parameter to the server's find routes (`GET /`)
  - Example: `/secrets/?group_by=system`
* Markdown Editor keyMaps
  - Can pass in a `keyMap` option to the Markdown component to map hot keys to actions.
* Countdowns get a dynamic icon based on their name

### Changed
* Shared/AppBar
  - Removed `newItem` and `newIcon` properties
  - Added `buttons` property that can be used in a more general way to define 
    any number of buttons and their actions.
  - Icon in Top-Left of App indicates if the App is running in development mode.
  - Added `endSlot` option
    + Will add a `spacer` and the value of `endSlot` to the right-most side of the
    AppBar if defined.
* Updated "sleep" time between serverHealthy checks on startup from 500ms to 750ms
* Secrets Enhancements
  + Secrets entries are now grouped by "System" on the main screen
  + Data fields are now presented in the order defined by the Secret type
     - I.e. `username-password` lists Username first on screens, then Password
* Change Home screen to use the Shared/AppBar component instead of defining it's own
  using very similar code.
* Shared/Actions: The `onArchiveDelete` action callback now takes an event param.
* Changed Countdowns from inline new/edit to using a bottom sheet editor.
* Improved Markdown Rendering
  - Less clunky looking (font smaller)
  - Tweaked a few options
  - Added syntax highlighting for code blocks
  - Added Task list rendering:  `- [x] stuff`
* `main/index.js` code clean-up for better readability & maintainability

### Fixed
* Archived/Deleted Countdowns, if favorited, no longer show on Home screen

### Deprecated
...

### Removed
...

### Security
...

### Misc
* Increased server unit test coverage: 98%

--------------------------------------------------------------------------------

## v1.2.0 - van Schagen - 2021-03-30
### Added
* Electron main process now logs to `DOCUMENTS/CartaroLog.json`
  - Includes STDOUT/STDERR from backend python server process.
* Added App wide notification system
* Icons
  - Created Icon class to manage all icons
  - Moved Constants.ICONS to Icon class
  - Includes code to dynamically select an icon based on keywords or sentences.
  - Added dynamic Icons to Notes based on, first, it's tags, then it's title.

### Changed
* Added the ability to edit and view LogEntries from the home page
  - Edit was already available
  - Added View as the default action
* Made edit & view actions consistent across Home screen components.
  - Click row to view
  - Click "new" edit icon to edit
* Better `Notifcation.error()` messages so that the source can be identified.
* Replaced TextArea "editors" with `vue-codemirror`
  - Better editing experience
  - Syntax Highlighting
  - Color Themes
* Models - Added Client/UI side JS models for the various Server Resources
  - Resource - Base model
  - Countdown, Secret, Todo, Tag, JiraTicket, LogEntry, WorkDay ... Etc.
  - Helps to DRY'up and Factor out lots of similar code.
* Config File
  - Converted to a class and refactored it's code a bit
  - Separate config file for DEV mode and PROD mode
  - Meaning that you can have DEV instance and PROD instance run on different ports.
* Consistent Archive / Delete behavior
  - Moved all archive/delete handling to the `Shared/Actions` component
  - All components now support archiving.
  - After an item is archived, it can be deleted (forever) or restored.

### Upgrades
* `eslint`: 7.23.0
  - eslint related modules to the latest versions and fixed lots of linting issues.
* `electron`: 11.4.1 -> 12.0.2
  - Had to disable `contextIsolation` for v12 :(
* Switched to `@electron/remote` instead of using (soon-to-be-deprecated) built-in `remote`
  - https://github.com/electron/remote
* `electron-builder`: 22.10.5
* `vuetify`: 2.4.8
* Various `XYZZY-loader` modules

--------------------------------------------------------------------------------

## v1.1.0 - Scylax - 2021-02-26
### Added
* Ability to rekey encrypted Secrets (`server/bin/rekey-secrets.py`)
* UI now has access to the config file
* Added new operators to the "find" REST API endpoint:
  * gt, gte, lt, lte, eq, ne - Example: `?field=gt:100`
  * Ability to search for `null` values - Example: `?field=null`
* Home Screen with:
  - Today's Date in menu bar
  - Work Days
  - Tickets
  - Todos
  - Notes
  - Log Entries
  - Countdowns
* Added `/sys` REST API endpoint to server. Supports:
  - `/sys/ping` (responds with "pong")
  - Used as a health check to ensure that the server is up from the UI

### Changed
* Better CHANGELOG management
* Reduced the size of each item in the Secrets list
* Added a Todo model on the UI side to help DRY-up the Javascript code.
  - Will model the other data types ASAP.
  - Stubbed in WorkDay model
* WorkDay screen improvements:
  - Changed icon to day type instead of celestial icons
  - Changed "today" highlight color. Was too dark.
  - Added a footer with some week related info
    - This weeks date range
    - Week number of the year
    - Total hours worked.
* Removed "Search" from Home screen menu bar (it was not implemented anyway)

### Fixed
* UI now reads encryption password from config file (was hard-coded for testing)
* Fixed a bug where App would display Home screen on startup **before** server
  was ready causing the Home screen to be blank/have no data.

--------------------------------------------------------------------------------

## v1.0.0 - Here Be Dragons - 2021-02-16
First release.

--------------------------------------------------------------------------------

## vM.N.P - Codename - YYYY-MM-DD
### Added
for new features

### Changed
for changes in existing functionality

### Fixed
for any bug fixes

### Deprecated
for soon-to-be removed features

### Removed
for now removed features

### Security
in case of vulnerabilities
