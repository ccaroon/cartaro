import arrow

from .base import Base
from .taggable import Taggable
from .ticket import Ticket

class LogEntry(Taggable, Base):
    # CATEGORIES = {
    #     'meeting': "Meeting",
    #     'ticket': "Ticket",
    #     'operational': "Operational",
    #     'other': "Other"
    # }

    def __init__(self, id=None, **kwargs):
        super().__init__(id=id, **kwargs)

    @property
    def logged_at(self):
        return self.__logged_at

    @logged_at.setter
    def logged_at(self, ts):
        self.__logged_at = self._epoch_to_date_obj(ts)

    def _unserialize(self, data):
        self.logged_at = data.get('logged_at', arrow.now().timestamp)
        self.subject = data.get('subject', None)
        self.content = data.get('content', None)
        self.category = data.get('category', None)
        
        # Related Ticket, such as Jira
        ticket = data.get('ticket', None)
        if isinstance(ticket, dict):
            self.ticket = Ticket(**ticket)
        elif isinstance(ticket, Ticket) or ticket == None:
            self.ticket = ticket
        else:
            raise TypeError("'ticket' must be of type `Ticket`, `dict` or `None`.")

        # Tags
        super()._unserialize(data)

    def _serialize(self):
        data = {
            "logged_at": self.logged_at.timestamp if self.logged_at else None,
            "subject": self.subject,
            "content": self.content,
            "category": self.category,
            "ticket": self.ticket.serialize()
        }
        
        # Tags
        data.update(super()._serialize())

        return data
