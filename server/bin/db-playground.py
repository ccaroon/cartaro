#!/usr/bin/env python

import arrow
import pprint
from tinydb import TinyDB, Query

DB_PATH = "/home/ccaroon/Documents/Cartaro"
DB_FILE = "Todos-dev.json"
db = TinyDB(F"{DB_PATH}/{DB_FILE}")

now = arrow.now()
ago = now.shift(days=-3)
later = now.shift(days=+3)
print(now, " | ", ago, " | ", later)
# print(now.timestamp)
# docs = db.all()
# for doc in docs:
#     pprint.pprint(doc)

query = Query()
# items = db.search(query.due_at < now.timestamp)
items = db.search(query.due_at > 3)
# print(len(items))

# Custom test with parameters:
def cmp_lt(doc_val, test_val):
    if doc_val:
        return doc_val < test_val
    else:
        return False

# items = db.search(
#     (query.is_complete == False)
#     &
#     (query.due_at.test(cmp_lt, later.timestamp))
# )

# print("---------------------------")
# for doc in items:
#     print(F"* {doc['title']}")
# print("---------------------------")
# print(len(items))
