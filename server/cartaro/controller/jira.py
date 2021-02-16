from flask import Blueprint, request, jsonify
import requests

from cartaro.model.ticket import Ticket
from cartaro import flask_app

jira = Blueprint("jira", __name__)

JIRA_CONFIG = flask_app.config.get('CARTARO', {}).get('jira', {})
DEFAULT_SEARCH = "assignee = currentUser() AND status != Closed AND issueType in standardIssueTypes()"

@jira.route('/search', methods=['GET'])
def search():
    resp = None
    status = 201
    try:
        host = JIRA_CONFIG.get('host')
        token = JIRA_CONFIG.get('token')
        if not host or not token:
            raise Exception("Jira Connection Not Properly Configured. Missing 'host' and/or 'token'")

        query_string = request.args.copy()
        search_name = query_string.pop('search', 'default')
        jira_jql = JIRA_CONFIG.get("searches", {}).get(search_name, DEFAULT_SEARCH)

        url = F"{host}/rest/api/2/search?jql={jira_jql}"
        resp = requests.get(
            url,
            headers = {
                'Authorization': F"Basic {token}"
            }
        )

        if resp.status_code == 200:
            tickets = Ticket.parse_jira(host, resp.json())
        else:
            raise Exception(F"Error Querying Jira: {resp.status_code} - [{url}]")

        resp = {
            'search_name': search_name,
            'jql': jira_jql,
            'results': tickets
        }
    except Exception as e:
        status = 500
        resp = {
            'error': str(e)
        }

    return jsonify(resp), status
