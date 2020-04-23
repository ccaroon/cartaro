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
from cartaro.controller.log_entries import log_entries
from cartaro.controller.notes import notes
from cartaro.controller.tags import tags
from cartaro.controller.work_days import work_days

flask_app.register_blueprint(log_entries, url_prefix="/log_entries")
flask_app.register_blueprint(notes, url_prefix="/notes")
flask_app.register_blueprint(tags, url_prefix="/tags")
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
