#!/usr/bin/env python
import pprint

from model.note import Note
# import server.model.note
# from server.controller.hello import hello

note = Note(id=77)
# note.load()
# pprint.pprint(note)

print(note.id)
print(note.title)
print(note.created_at)
print(note.updated_at)
print(note.deleted_at)
