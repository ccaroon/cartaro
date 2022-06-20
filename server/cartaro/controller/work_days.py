from flask import request, jsonify

from cartaro.model.work_day import WorkDay
import cartaro.controller.base as base

work_days = base.create_controller("work_days", WorkDay)

@work_days.route('/range', methods=['GET'])
def range():
    resp = None
    status = 200

    try:
        query_string = request.args.copy()

        start = query_string.pop('start', None)
        end = query_string.pop('end', None)
        days = int(query_string.pop('days', 0))

        work_days = []
        if start and (end or days):
            work_days = WorkDay.range(start, end, days)
        else:
            raise TypeError("Error: Requires 'start' and either 'end' or 'days'.")

        resp = {
            'work_days': work_days
        }
    except Exception as e:
        status = 500
        resp = {
            "error": str(e)
        }

    return jsonify(resp), status
