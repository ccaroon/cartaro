# Ĉartaro
Esperanto for Chronicle. Ĉartaro is a journal or chronicle of your work.

[Ĉartaro](https://github.com/ccaroon/cartaro) is a successor to
[Mettisto](https://github.com/ccaroon/metiisto) which is a successor of
[Workman](https://github.com/ccaroon/workman).

## Front-end / UI
Electron / VueJS / Vuetify

## Back-end / Server
* Python 3.10.x
* Flask
* TinyDB

## Development
Requires NodeJS v16.16.x and Python 3.10.x

### Setup
0. `cd server`
1. Create Virtual Env: `python -mvenv venv`
2. Activate: `. ./venv/bin/activate`
3. Install Deps: `pip install -r requirements.txt`
4. `make test` && `make cover`
5. `make help`

### Dev UI
1. `cd server; make dist; cd ..`
2. `npm run dev`

## Production Build
0. `cd server`
1. `make dist`
2. `cd ..`
3. `npm run build`
4. `cd dist_electron; ls`
5. Profit!

## Tech
### UI
* [VueJS 2](https://v2.vuejs.org/)
* [Vuetify](https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides)
* [MomentJS](https://fontawesome.com/icons)
* [Material Design Icons](https://materialdesignicons.com/)
* [Font Awesome FREE](https://fontawesome.com/icons)
* [Electron](https://www.electronjs.org/)

### Tooling
* [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [Vue CLI](https://cli.vuejs.org/)
* [Vue Electron Builder](https://nklayman.github.io/vue-cli-plugin-electron-builder/)
* [Electron Builder](https://www.electron.build/)

### Server
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html)

## Tools
[Image Converter](https://anyconv.com/png-to-icns-converter/)
