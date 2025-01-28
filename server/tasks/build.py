import os
import shutil

from invoke import task

import util

CODE_PATH = f"{util.ROOT_DIR}/cartaro"
DIST_PATH = f"{util.ROOT_DIR}/dist"

PACKAGE_NAME = "cartaro-server.zip"
PACKAGE_PATH = f"{util.ROOT_DIR}/{PACKAGE_NAME}"
PACKAGE_FILES = [
    f"{util.ROOT_DIR}/bin/python",
    f"{util.ROOT_DIR}/requirements-prod.txt"
]


@task
def clean(ctx):
    """
    Remove Build Detritus
    """
    if os.path.exists(DIST_PATH):
        print(f"=> Deleting {DIST_PATH}")
        shutil.rmtree(DIST_PATH)

    if os.path.exists(PACKAGE_PATH):
        print(f"=> Deleting {PACKAGE_PATH}")
        os.remove(PACKAGE_PATH)


@task
def package(ctx):
    """
    Build a distribution package (ZIP) file
    """
    # Find Python File Deps
    deps = []
    for base_dir, _, files in os.walk(CODE_PATH):
        for file in files:
            if file.endswith(".py"):
                deps.append(f"{base_dir}/{file}")

    deps.extend(PACKAGE_FILES)
    needs_build = False
    for file in deps:
        if not os.path.exists(PACKAGE_PATH) or is_newer(file, PACKAGE_PATH):
            needs_build = True
            break

    if needs_build:
        if os.path.exists(DIST_PATH):
            shutil.rmtree(DIST_PATH)

        if os.path.exists(PACKAGE_PATH):
            os.remove(PACKAGE_PATH)

        ctx.run(f"pip install --target {DIST_PATH} -r requirements-prod.txt")
        ctx.run(f"cp {util.ROOT_DIR}/bin/python {DIST_PATH}/bin")
        ctx.run(f"cp -a {CODE_PATH} {DIST_PATH}/")
        with ctx.cd(DIST_PATH):
            ctx.run(f"zip -r {PACKAGE_PATH} *")

        print(f"=> Package Built: {PACKAGE_PATH}")
    else:
        print("=> Nothing to do.")


@task
def python(ctx):
    """
    Update the version of Python used to run the server.
    """
    ctx.run(f"cp `pyenv which python` {util.ROOT_DIR}/bin")
    print("Complete")


# UTIL Functions
def is_newer(file1, file2):
    """
    Is `file1` newer than `file2`?

    Args:
        file1 (str): Path to a file
        file2 (str): Path to a file

    Returns:
        boolean: True if file1 is newer than file2, False otherwise
    """
    mt1 = os.path.getmtime(file1)
    mt2 = os.path.getmtime(file2)

    return mt1 > mt2
