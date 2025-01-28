from invoke import Collection

import check
import build
import server

ns = Collection(
    build,
    check,
    server
)
