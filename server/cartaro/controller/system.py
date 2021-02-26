from flask import Blueprint, jsonify

system = Blueprint("system", __name__)

@system.route('/ping', methods=['GET'])
def ping():
    resp = None
    status = 200
    try:
        resp = 'pong'
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return jsonify(resp), status
