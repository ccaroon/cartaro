from server import app
from server.model.hello import Hello

@app.route('/')
def hello():
    conf = app.config.get('SERVER', {})
    hello = Hello(conf.get('name', 'World'))
    return {
        "msg": hello.msg()
    }
