from flask import Blueprint, request, jsonify
from cartaro.model.tag import Tag

tags = Blueprint('tags', __name__)

@tags.route('/', methods=['GET'])
def find():
    resp = None
    status = 200

    try:
        query_string = request.args.copy()
        
        tags = None
        if not query_string:
            tags = Tag.fetch()
        else:
            tags = Tag.find(**query_string)

        resp = {
            'tags': tags
        }
    except Exception as e:
        status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status
