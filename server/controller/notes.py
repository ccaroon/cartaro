from flask import Blueprint, request
from server.model.note import Note

notes = Blueprint('notes', __name__)

@notes.route('/<int:id>')
def view(id):
    note = Note(id=id)

    data = None
    status = 200
    try:
        note.load()
        data = note.for_json()
    except Exception as e:
        if "Record Not Found" in str(e):
            status = 404
        else:
            status = 500
        data = {
            "error": str(e)
        }

    return data, status

@notes.route('/', methods=['POST'])
def new():
    data = request.json
    note = Note(**data)
    note.save()

    return F"New({note.id}) - {note.title} - Success", 200
