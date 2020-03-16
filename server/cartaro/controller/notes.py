from flask import Blueprint, request, jsonify
from cartaro.model.note import Note

notes = Blueprint('notes', __name__)

# NOTE: Currently does not support/surface the Note classes encryption ability

@notes.route('/', methods=['POST'])
def create():
    resp = None
    status = 201
    try:
        data = request.json

        note = Note(**data)
        note.save()

        resp = {
            'id': note.id
        }
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return jsonify(resp), status

@notes.route('/<int:id>', methods=['GET'])
def retrieve(id):
    note = Note(id=id)

    resp = None
    status = 200
    try:
        note.load()
        resp = note
    except Exception as e:
        if "Record Not Found" in str(e):
            status = 404
        else:
            status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status

@notes.route('/', methods=['GET'])
def retrieve_all():
    resp = None
    status = 200

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('pp', 25))

        offset = (page - 1) * per_page
        count  = per_page

        notes = Note.fetch(offset, count)
        resp = notes
    except Exception as e:
        status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status

@notes.route('/<int:id>', methods=['PUT'])
def update(id):
    resp = None
    status = 200
    try:
        data = request.json

        note = Note(id=id)
        note.load()

        # Update
        note.title = data.get('title', note.title)
        note.is_favorite = data.get('is_favorite', note.is_favorite)
        note.content = data.get('content', note.content)

        note.save()

        resp = note
    except Exception as e:
        if "Record Not Found" in str(e):
            status = 404
        else:
            status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status

@notes.route('/<int:id>', methods=['DELETE'])
def delete(id):
    resp = None
    status = 200

    try:
        data = request.json or {}

        note = Note(id=id)
        note.delete(safe=data.get('safe', False))

        resp = {
            'id': id
        }
    except Exception as e:
        if "Record Not Found" in str(e):
            status = 404
        else:
            status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status
