# CHANGELOG

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

### Deprecated
n/a

### Removed
n/a

### Security
n/a

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
