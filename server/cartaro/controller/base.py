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

    # ...OLD..
    # ?page=1&pp=10&op=AND&sort_by=date&group_by=priority&title=Ghoti&priority=4
    #
    # ...PROPOSED...
    # ?meta=page=1:pp=10:sort_by=date:group_by=priority&query=(title=~Ghoti OR priority>=4) AND deleted_at~=null
    #
    @controller.route('/', methods=['GET'])
    def find():
        """
        Find records based on query string info
        """
        resp = None
        status = 200

        try:
            query_string = request.args.copy()

            # meta data
            ## -- fields: page, pp, sort_by, group_by
            ## -- example: meta=page=1:pp=10:sort_by=date:group_by=priority
            ## Convert meta data string to list
            # TODO: need a better default...not x=x
            meta_data = query_string.pop('meta', 'x=x').split(':')
            ## ['page=1', 'pp=10', 'sort_by=date']
            ## Convert meta data list to dict
            splitter = lambda meta_field: meta_field.split('=', 2)
            meta = { splitter(m)[0]: splitter(m)[1] for m in meta_data }

            page     = int(meta.get('page', 1))
            per_page = int(meta.get('pp', 10))
            # TODO: don't need operator
            operator = meta.get('op', 'or')
            sort_by  = meta.get('sort_by', None)
            group_by = meta.get('group_by', None)

            # print(page, per_page, operator, sort_by, group_by)

            # the query
            ## -- query - get passed directly to TinyDB
            ## -- example - query=(title=~Ghoti OR priority>=4) AND deleted_at~=null
            search_query = query_string.pop('query', "")

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
