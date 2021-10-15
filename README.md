# Ĉartaro
Esperanto for Chronicle. Ĉartaro is a journal or chronicle of your work.

[Ĉartaro](https://github.com/ccaroon/cartaro) is a successor to
[Mettisto](https://github.com/ccaroon/metiisto) which is a successor of
[Workman](https://github.com/ccaroon/workman).

## Front-end / UI
* Electron
* VueJS
* Vuetify

## Back-end / Server
* Python 3.8
* Flask
* TinyDB

## Development
Requires NodeJS v14.15.x and Python 3.8.x

### Setup
0. `cd server`
1. Create Virtual Env: `python -mvenv venv`
2. Activate: `. ./venv/bin/activate`
3. Install Deps: `pip install -r requirements.txt`

### Notes
* Unit Tests: `make test`
* Coverage: `make cover`
* Start Dev Server: `make dev`
    - Runs on port 7777

## Build
0. `cd server`
1. `make dist`
2. `cd ..`
3. `npm run build`
4. `cd build`
5. Profit!

## Tools
[Image Converter](https://anyconv.com/png-to-icns-converter/)
