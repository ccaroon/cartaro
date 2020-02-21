#!/usr/bin/env python
import os
from server import app
import server.controller.hello

# TODO: logging

@app.after_request
def set_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET,HEAD,POST,PUT"
    resp.headers['Access-Control-Allow-Headers'] = 'content-type'

    return resp
