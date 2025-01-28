from invoke import task

import util

TEST_ENV = {
    "CARTARO_ENV": "test",
    "CARTARO_DOC_PATH": "tests/tmp",
    "CARTARO_CFG_PATH": "../tests/data"
}

@task(
    help={
        "module": "Specific Test Module to execute. Ex: tests.module.test_note"
    }
)
def unit_tests(ctx, module=None):
    """ Run Unit Tests """

    cmd = "nose2 -v "
    if module:
        cmd += f"{module}"
    else:
        cmd += f"-s {util.ROOT_DIR}/tests"

    ctx.run(cmd, env=TEST_ENV)


@task(
    help={
        "module": "Specific Test Module to execute. Ex: tests.module.test_note"
    }
)
def coverage(ctx, module=None):
    """ Run Code Coverage """
    cmd = "coverage run -m nose2 -v "
    if module:
        cmd += f"{module}"
    else:
        cmd += f"-s {util.ROOT_DIR}/tests"

    ctx.run(cmd, env=TEST_ENV)
    ctx.run("coverage report")
    ctx.run("coverage html")


@task
def clean(ctx):
    """ Delete Testing Detritus """
    ctx.run(f"rm -f {util.ROOT_DIR}/tests/tmp/*.json {util.ROOT_DIR}/.coverage")
    ctx.run(f"rm -rf {util.ROOT_DIR}/htmlcov")
