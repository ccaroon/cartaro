#!/usr/bin/env python
import os
from server import app

from server.controller.notes import notes

app.register_blueprint(notes, url_prefix="/notes")

# TODO: logging

@app.after_request
def set_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET,HEAD,POST,PUT"
    resp.headers['Access-Control-Allow-Headers'] = 'content-type'

    return resp
