# Ĉartaro
Esperanto for Chronicle. Ĉartaro is a journal or chronicle of your work. 

[Ĉartaro](https://github.com/ccaroon/cartaro) is a successor to 
[Mettisto](https://github.com/ccaroon/metiisto) which is a successor of 
[Workman](https://github.com/ccaroon/workman).

## Front-end / UI
* Electron
* VueJS
* Vuetify

### Notes
* Needs to be run/build with NodeJS 10.x.x. NodeJS 12.x.x does not work at the
  moment.

## Server
Supports Python 3.6+. I use 3.8.

### Development
#### Setup
1. Create Virtual Env: `python -mvenv venv`
2. Activate: `. ./venv/bin/activate`
3. Install Deps: `pip install -r requirements.txt`

#### Notes
* Unit Tests: `make test`
* Coverage: `make cover`
* Start Dev Server: `make dev`
    - Runs on port 4242

## Tools
[Image Converter](https://anyconv.com/png-to-icns-converter/)
