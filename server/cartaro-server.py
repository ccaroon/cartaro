#!/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return {
        "name": "Craig",
        "age": 42
    }
