#!/usr/bin/env python

# import arrow
import pprint
import re
from tinydb import TinyDB, Query

DB_PATH = "/home/ccaroon/Documents/Cartaro"
DB_FILE = "Todos-dev.json"
db = TinyDB(F"{DB_PATH}/{DB_FILE}")

# now = arrow.now()

# items = db.search(query.due_at < now.int_timestamp)

def read_query():
    query = input('query> ')
    return query


def parse_query(query_str):
    return parse_query2(query_str)

# query = query_parts[0]
# if op == "or":
#     for qp in query_parts:
#         query |= qp
# elif op == "and":
#     for qp in query_parts:
#         query &= qp
# => (title=~Ghoti OR priority>=4) AND deleted_at~=null
# -> AND { OR {title=~Ghoti, priority >=4}, deleted_at != null }
def parse_query1(query_str):
    query = Query()

    # TODO: and | or NOT case sensitive
    pattern = re.compile('^(and|or)\s+{(.*)}$')

    more = True
    curr_query = query_str
    # TODO: loop around this somehow
    while more:
        match = re.match(pattern, curr_query)
        if not match:
            raise Exception(F'Malformed Query: [{curr_query}]')

        # TODO: stash this stuff away...
        operator = match.group(1)
        # TODO: how to split tests?
        tests = match.group(2).strip().split(',')

        print(F"OP: `{operator}` | Q: `{tests}`")
        # TODO: ...and repeat if necessry


    # qparts.append(query.title == 'Do something')
    # qparts.append((query.priority >= 4) & (query.deleted_at == None))
    # qparts.append(query.deleted_at == None)

    return (query.title == 'fish')

# (title=~Ghoti OR priority>=4) AND deleted_at~=null
def parse_query2(query_str):
    query = Query()

    # split on AND or OR



    # TODO: and | or NOT case sensitive
    pattern = re.compile('^(and|or)\s+{(.*)}$')

    more = True
    curr_query = query_str
    # TODO: loop around this somehow
    while more:
        match = re.match(pattern, curr_query)
        if not match:
            raise Exception(F'Malformed Query: [{curr_query}]')

        # TODO: stash this stuff away...
        operator = match.group(1)
        # TODO: how to split tests?
        tests = match.group(2).strip().split(',')

        print(F"OP: `{operator}` | Q: `{tests}`")
        # TODO: ...and repeat if necessry


    # qparts.append(query.title == 'Do something')
    # qparts.append((query.priority >= 4) & (query.deleted_at == None))
    # qparts.append(query.deleted_at == None)

    return (query.title == 'fish')

# AND { OR {title=~Ghoti, priority >=4}, deleted_at != null }
def parse_query3(query_str):


def execute_query(query_str):

    try:
        query = parse_query(query_str)

        records = db.search(query)
        # pprint.pprint(records)
        for rec in records:
            print(F"[{rec['priority']}] - {rec['title']} ({rec['deleted_at']})")
    except Exception as exc:
        print(exc)

if __name__ == "__main__":
    query_str = None

    try:
        while query_str != 'QUIT':
            query_str = read_query()
            if query_str:
                execute_query(query_str)
    except EOFError as err:
        print("Exiting!")







#
