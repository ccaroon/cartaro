from flask import Blueprint
from server import app
from server.model.hello import Hello

hello = Blueprint('hello', __name__)

@hello.route('/')
def say_hi():
    conf = app.config.get('SERVER', {})
    hi = Hello(conf.get('name', 'World'))
    return {
        "msg": hi.msg()
    }
