class Ticket:
    def __init__(self, key, summary, type, status, link):
        self.key = key
        self.summary = summary
        self.type = type
        self.status = status
        self.link = link
        self.sub_tasks = []


    @classmethod
    def _ticket_from_jira_issue(cls, host, issue):
        fields = issue.get('fields', {})
        ticket = Ticket(
            key=issue['key'],
            summary=fields['summary'],
            type=fields['issuetype']['name'],
            status=fields['status']['name'],
            link=F"{host}/browse/{issue['key']}"
        )

        return ticket

    @classmethod
    def parse_jira(cls, host, jira_data):
        tickets = []
        for issue in jira_data['issues']:
            ticket = cls._ticket_from_jira_issue(host, issue)

            for sub_task in issue['fields'].get("subtasks", []):
                child = cls._ticket_from_jira_issue(host, sub_task)
                ticket.add_sub_task(child)

            tickets.append(ticket)

        return tickets

    def add_sub_task(self, ticket):
        self.sub_tasks.append(ticket)

    def serialize(self, **kwargs):
        data = {
            "key": self.key,
            "summary": self.summary,
            "type": self.type,
            "status": self.status,
            "link": self.link
        }

        if not kwargs.get('omit_sub_tasks', False):
            data['sub_tasks'] = [task.serialize() for task in self.sub_tasks]

        return data
