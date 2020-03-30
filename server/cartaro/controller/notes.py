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
def find():
    resp = None
    status = 200

    try:
        query_string = request.args.copy()

        page     = int(query_string.pop('page', 1))
        per_page = int(query_string.pop('pp', 10))

        num_notes = None
        notes = None
        offset = (page - 1) * per_page
        if not query_string:
            notes = Note.fetch(offset, per_page)
            num_notes = Note.count()
        else:
            notes = Note.find(**query_string)
            num_notes = len(notes)
            # s = slice(offset, offset + per_page)
            if num_notes > per_page:
                notes = notes[offset:offset + per_page]

        resp = {
            'total': num_notes,
            'page': page,
            'per_page': per_page,
            'notes': notes
        }
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
        safe_del = request.args.get('safe', False)
        
        note = Note(id=id)
        note.delete(safe=safe_del)

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

# ------------------------------------------------------------------------------
# CLI commands
# ------------------------------------------------------------------------------
import click
import faker
FAKER = faker.Faker()

@notes.cli.command('bulk-create')
@click.option('-c', '--count', default=25)
def create(count):
    """Create a bunch of fake notes in the database"""

    for i in range(0, count):
        note = Note(
            title=FAKER.sentence(),
            content='\n'.join(FAKER.paragraphs(nb=5)),
            is_favorite=FAKER.boolean(chance_of_getting_true=25)
        )
        note.save()

        print(F"Created {i+1}/{count}", end='\r')

    print("\nDone.")
















# 
