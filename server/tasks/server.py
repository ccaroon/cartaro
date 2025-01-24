import os
from invoke import task

@task
def dev(ctx):
    """ Start Server in DEV mode """

    home_dir = os.getenv("HOME")
    env = {
        "CARTARO_DOC_PATH": f"{home_dir}/Documents/Cartaro",
        "CARTARO_ENV": "dev",
        "FLASK_DEBUG": "1",
        "FLASK_APP": "cartaro"
    }

    ctx.run("flask run -p 7777", env=env)
