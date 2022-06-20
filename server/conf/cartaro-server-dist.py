#-------------------------------------------------------------------------------
# Example Gunicorn Config File
# https://docs.gunicorn.org/en/latest/index.html
#
# Should be copied to your XDG_CONFIG_HOME or $HOME/.config directory as 'cartaro-server.py'
# Can be used as-is, no changes needed. But feel free to tweak it for your own
# needs.
#-------------------------------------------------------------------------------
import os
import json

#-------------------------------------------------------------------------------

CARTARO_ENV=os.environ.get('CARTARO_ENV', "dev")
CARTARO_DOC_PATH=F'{os.environ.get("HOME")}/Documents/Cartaro'

cfg_file = "CartaroCfg.json" if CARTARO_ENV == "prod" else F"CartaroCfg-{CARTARO_ENV}.json"
CARTARO_CFG_FILE=F'{CARTARO_DOC_PATH}/{cfg_file}'

#-------------------------------------------------------------------------------

def bind():
    host = '127.0.0.1'
    port = None
    with open(CARTARO_CFG_FILE, "r") as file:
        config = json.load(file).get('CARTARO', {})
        port = config.get('server', {}).get('port', 2424)

    return F"{host}:{port}"

#-------------------------------------------------------------------------------

bind = bind()
daemon = True
raw_env = [
    F'CARTARO_DOC_PATH={CARTARO_DOC_PATH}',
    F'CARTARO_ENV={CARTARO_ENV}'
]
workers = 1
