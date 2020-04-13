from flask import Blueprint, request, jsonify

def create_controller(controller_name, Model):
    controller = Blueprint(controller_name, __name__)

    @controller.route('/', methods=['POST'])
    def create():
        resp = None
        status = 201
        try:
            data = request.json

            obj = Model(**data)
            obj.save()

            resp = {
                'id': obj.id
            }
        except Exception as e:
            status = 500
            resp = {
                'error': str(e)
            }

        return jsonify(resp), status

    @controller.route('/<int:id>', methods=['GET'])
    def retrieve(id):
        obj = Model(id=id)

        resp = None
        status = 200
        try:
            obj.load()
            resp = obj
        except Exception as e:
            if "Record Not Found" in str(e):
                status = 404
            else:
                status = 500
            resp = {
                "error": str(e)
            }

        return jsonify(resp), status

    @controller.route('/', methods=['GET'])
    def find():
        resp = None
        status = 200

        try:
            query_string = request.args.copy()

            page     = int(query_string.pop('page', 1))
            per_page = int(query_string.pop('pp', 10))

            num_objs = None
            objs = None
            offset = (page - 1) * per_page
            if not query_string:
                objs = Model.fetch(offset, per_page)
                num_objs = Model.count()
            else:
                objs = Model.find(**query_string)
                num_objs = len(objs)
                # s = slice(offset, offset + per_page)
                if num_objs > per_page:
                    objs = objs[offset:offset + per_page]

            resp = {
                'total': num_objs,
                'page': page,
                'per_page': per_page,
            }
            resp[controller_name] = objs
        except Exception as e:
            status = 500
            resp = {
                "error": str(e)
            }

        return jsonify(resp), status

    @controller.route('/<int:id>', methods=['PUT'])
    def update(id):
        resp = None
        status = 200
        try:
            data = request.json

            obj = Model(id=id)
            obj.load()

            obj.update(data)

            obj.save()

            resp = obj
        except Exception as e:
            if "Record Not Found" in str(e):
                status = 404
            else:
                status = 500
            resp = {
                "error": str(e)
            }

        return jsonify(resp), status

    @controller.route('/<int:id>', methods=['DELETE'])
    def delete(id):
        resp = None
        status = 200

        try:
            safe_del = request.args.get('safe', False)
            
            obj = Model(id=id)
            obj.delete(safe=safe_del)

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

    return controller
