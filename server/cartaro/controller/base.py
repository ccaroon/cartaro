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
            operator = query_string.pop('op', 'or')
            sort_by  = query_string.pop('sort_by', None)
            group_by = query_string.pop('group_by', None)

            num_objs = None
            objs = None
            offset = (page - 1) * per_page
            if not query_string:
                objs = Model.fetch(offset, per_page, sort_by=sort_by)
                num_objs = Model.count()
            else:
                objs = Model.find(op=operator, sort_by=sort_by, **query_string)
                num_objs = len(objs)
                # s = slice(offset, offset + per_page)
                if num_objs > per_page:
                    objs = objs[offset:offset + per_page]

            if group_by:
                grouped_objs = {}
                for obj in objs:
                    group_key = getattr(obj, group_by)
                    group = grouped_objs.get(group_key, [])
                    group.append(obj)
                    grouped_objs[group_key] = group

                objs = grouped_objs

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

    @controller.route('/undelete/<int:id>', methods=['PUT'])
    def undelete(id):
        resp = None
        status = 200
        try:
            obj = Model(id=id)
            obj.load()
            obj.undelete()

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
            # Assume 'safe' specified as 0 or 1
            safe_del = int(request.args.get('safe', False))

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
