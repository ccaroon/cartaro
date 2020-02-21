import os
from flask import Flask

app = Flask(__name__)

doc_path = os.environ.get('CARTARO_DOC_PATH', '.')
app.config.from_json(F"{doc_path}/CartaroCfg.json", silent=True)
app.config['DOC_PATH'] = doc_path
