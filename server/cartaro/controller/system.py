from genericpath import exists
from flask import Blueprint, request, jsonify
import os
import sys

from cartaro import flask_app
from cartaro.utils.archive import Archive

system = Blueprint("system", __name__)

@system.route('/ping', methods=['GET'])
def ping():
    resp = None
    status = 200
    try:
        resp = f'pong - {sys.version} | {sys.path}'
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return jsonify(resp), status

@system.route('/backup', methods=['POST'])
def backup():
    resp = None
    status = 201

    doc_path = flask_app.config['DOC_PATH']
    backup_cfg = flask_app.config.get('CARTARO', {}).get('backup', {})
    try:
        data = request.json or {}
        
        keep = data.get('keep', backup_cfg.get('keep', 7))

        archive_path = data.get('path',
            backup_cfg.get('path', F"{doc_path}Backup"))
        os.makedirs(archive_path, exist_ok=True)

        archive = Archive(archive_path)
        archive.add(doc_path)
        archive.clean(older_than=keep)

        resp = {
            'message': F"Data in {doc_path} archived to {archive_path}."
        }
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return jsonify(resp), status
