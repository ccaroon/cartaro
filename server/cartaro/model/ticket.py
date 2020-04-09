class Ticket:
    def __init__(self, key, summary, type, status, link, points=0, is_flagged=False, parent=None):
        self.key = key
        self.summary = summary
        self.type = type
        self.status = status
        self.is_flagged = is_flagged
        self.link = link
        self.points = points

        self.parent = parent
        self.sub_tasks = []

    def add_sub_task(self, ticket):
        ticket.parent = self
        self.sub_tasks.append(ticket)

    def serialize(self, **kwargs):
        data = {
            "key": self.key,
            "summary": self.summary,
            "type": self.type,
            "status": self.status,
            "is_flagged": self.is_flagged,
            "link": self.link,
            "points": self.points,
            "parent": self.parent.serialize(omit_sub_tasks=True) if self.parent else None,
        }

        if not kwargs.get('omit_sub_tasks', False):
            data['sub_tasks'] = [task.serialize() for task in self.sub_tasks]

        return data
