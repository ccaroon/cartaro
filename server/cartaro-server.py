#!/bin/env python
from flask import Flask
app = Flask(__name__)

# TODO: Need to handle SIGTERM?
# TODO: logging

@app.route('/')
def hello_world():
    return {
        "name": "Craig",
        "age": 42
    }

@app.after_request
def set_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET,HEAD,POST,PUT"
    resp.headers['Access-Control-Allow-Headers'] = 'content-type'

    return resp
