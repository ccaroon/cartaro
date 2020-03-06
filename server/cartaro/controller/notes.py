from flask import Blueprint, request
from cartaro.model.note import Note

notes = Blueprint('notes', __name__)

@notes.route('/<int:id>', methods=['GET'])
def retrieve(id):
    note = Note(id=id)

    resp = None
    status = 200
    try:
        note.load()
        if note.is_encrypted:
            # TODO: Get Password from Server Config
            passwd = "fish"
            note.decrypt(passwd)

        resp = note.for_json()
    except Exception as e:
        if "Record Not Found" in str(e):
            status = 404
        else:
            status = 500
        resp = {
            "error": str(e)
        }

    return resp, status

@notes.route('/', methods=['POST'])
def create():
    resp = None
    status = 201
    try:
        data = request.json
        note = Note(**data)

        if note.is_encrypted:
            # TODO: Get Password from Server Config
            passwd = "fish"
            note.encrypt(passwd)

        note.save()
        resp = {
            'id': note.id
        }
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return resp, status

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

        # TODO: Get Password from Config
        passwd = "fish"
        was_encrypted = note.is_encrypted
        if note.is_encrypted:
            note.decrypt(passwd)

        note.content = data.get('content', note.content)
        
        if was_encrypted:
            note.encrypt(passwd)
        
        note.save()
        
        if note.is_encrypted:
            note.decrypt(passwd)
        
        resp = note.for_json()
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return resp, status








# 
