import os
from flask import Flask

# ------------------------------------------------------------------------------
# Flask App Setup
# ------------------------------------------------------------------------------
flask_app = Flask(__name__)

doc_path = os.environ.get('CARTARO_DOC_PATH', '.')
flask_app.config.from_json(F"{doc_path}/CartaroCfg.json", silent=True)
flask_app.config['DOC_PATH'] = doc_path
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Blueprint (controller) Registration
# ------------------------------------------------------------------------------
from cartaro.controller.notes import notes

flask_app.register_blueprint(notes, url_prefix="/notes")
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
