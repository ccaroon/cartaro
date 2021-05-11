#!/usr/bin/env python
################################################################################
import os
import re
import sys

"""
Finds all empty and unused tags, then deletes them.
"""

sys.path.append(".")
from cartaro.model.tag import Tag

# Taggable classes
from cartaro.model.log_entry import LogEntry
from cartaro.model.note import Note
from cartaro.model.secret import Secret
from cartaro.model.todo import Todo
from cartaro.model.work_day import WorkDay
# ------------------------------------------------------------------------------
def purge_empty(tags):
    for tag in tags:
        if tag.name == "":
            print(F"Empty {tag.id:04d} - [{tag.name}].")
            tag.delete()

def used_by(tag, items):
    used = False
    for item in items:
        if tag in item.tags:
            used = True
            break
    return used

def prune_unused(tags):
    entries = LogEntry.fetch()
    notes = Note.fetch()
    secrets = Secret.fetch()
    todos = Todo.fetch()
    work_days = WorkDay.fetch()

    unused_tags = []
    for tag in tags:
        used = False
        for items in (entries, notes, secrets, todos, work_days):
            used = used_by(tag, items)
            if used:
                break
        if not used:
            unused_tags.append(tag)

    for tag in unused_tags:
        print(F"Pruning {tag.id:04d} - [{tag.name}].")
        tag.delete()

################################################################################
if __name__ == "__main__":
    env = os.getenv('CARTARO_ENV', 'dev')
    doc_path = os.getenv('CARTARO_DOC_PATH')
    if not doc_path:
        raise Exception("CARTARO_DOC_PATH **must** be set.")

    print(F"Analyzing Tags for {doc_path} in {env}...")

    tags = Tag.fetch()

    purge_empty(tags)
    prune_unused(tags)
