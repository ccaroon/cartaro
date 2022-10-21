import os
import json
from flask import Flask

# ------------------------------------------------------------------------------
# Flask App Setup
# ------------------------------------------------------------------------------
flask_app = Flask(__name__)

# ------------------------------------------------------------------------------
# Configure Flask's JSONEncoder to look for a "serialize" method when 
# serializing Cartaro model class instances.
# ------------------------------------------------------------------------------
# Define a function to handle Cartaro models by calling their "serialize"
# method...
# ...for other obj's that don't have a "serialize" method, use the default
# json encoder
def __json_encoder(cls, obj):
    return getattr(obj.__class__, "serialize", __json_encoder.default)(obj)
# Set an attribute named 'default' on the __json_encoder function
# to the method that we are going to be overriding, i.e. the default
# JSONProvider.default method.
# __json_encoder.default is then used as the fallback encoder if the object
# being encoded does NOT have a "serialize" method.
__json_encoder.default = flask_app.json_provider_class.default

# Then override the flask.json.provider.DefaultJSONProvider.default
# method to __json_encoder.
flask_app.json_provider_class.default = __json_encoder
# ------------------------------------------------------------------------------
doc_path = os.environ.get('CARTARO_DOC_PATH', '.')
cfg_path = os.environ.get('CARTARO_CFG_PATH', doc_path)
# NOTE: Top-level keys in CartaroCfg.json MUST be UPPERCASE for Flask to store them
# TODO: Make use of config.py, somehow, for the SERVER part of the config
suffix = "-dev" if os.environ.get('CARTARO_ENV') == "dev" else ""
flask_app.config.from_file(
    F"{cfg_path}/CartaroCfg{suffix}.json", load=json.load, silent=False)
flask_app.config['DOC_PATH'] = doc_path
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Special Model Init
# ------------------------------------------------------------------------------
from cartaro.model.secret import Secret
Secret.ENCRYPTION_KEY = flask_app.config.get('CARTARO', {}).get('encryption_password')
# ------------------------------------------------------------------------------
# Blueprint (controller) Registration
# ------------------------------------------------------------------------------
from cartaro.controller.count_downs import count_downs
from cartaro.controller.log_entries import log_entries
from cartaro.controller.jira import jira
from cartaro.controller.notes import notes
from cartaro.controller.secrets import secrets
from cartaro.controller.system import system
from cartaro.controller.tags import tags
from cartaro.controller.time_off.holidays import holidays
from cartaro.controller.time_off.personal import personal
from cartaro.controller.todos import todos
from cartaro.controller.work_days import work_days

flask_app.register_blueprint(count_downs, url_prefix="/count_downs")
flask_app.register_blueprint(log_entries, url_prefix="/log_entries")
flask_app.register_blueprint(holidays, url_prefix="/time_off/holidays")
flask_app.register_blueprint(jira, url_prefix="/jira")
flask_app.register_blueprint(notes, url_prefix="/notes")
flask_app.register_blueprint(personal, url_prefix="/time_off/personal")
flask_app.register_blueprint(secrets, url_prefix="/secrets")
flask_app.register_blueprint(system, url_prefix="/sys")
flask_app.register_blueprint(tags, url_prefix="/tags")
flask_app.register_blueprint(todos, url_prefix="/todos")
flask_app.register_blueprint(work_days, url_prefix="/work_days")
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Misc
# ------------------------------------------------------------------------------
@flask_app.after_request
def set_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET,HEAD,POST,PUT,DELETE"
    resp.headers['Access-Control-Allow-Headers'] = 'content-type'

    return resp
