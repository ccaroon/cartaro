import arrow

from .base import Base
from .taggable import Taggable

class LogEntry(Taggable, Base):
    # CATEGORIES = {
    #     'meeting': "Meeting",
    #     'ticket': "Ticket",
    #     'operational': "Operational",
    #     'other': "Other"
    # }

    def __init__(self, id=None, **kwargs):
        self.logged_at = arrow.now().timestamp
        self.subject = None
        self.content = None
        self.category = None
        self.ticket_link = None

        super().__init__(id=id, **kwargs)

    @property
    def logged_at(self):
        return self.__logged_at

    @logged_at.setter
    def logged_at(self, new_date):
        if isinstance(new_date, arrow.Arrow):
            self.__logged_at = new_date
        elif isinstance(new_date, int):
            self.__logged_at = self._epoch_to_date_obj(new_date)
        else:
            raise TypeError("'logged_at' must be of type INT or Arrow")

    def update(self, data):
        self.logged_at = data.get('logged_at', self.logged_at)
        self.subject = data.get('subject', self.subject)
        self.content = data.get('content', self.content)
        self.category = data.get('category', self.category)

        self.ticket_link = data.get('ticket_link', self.ticket_link)
        # # Related Ticket, such as Jira
        # ticket = data.get('ticket', None)
        # if isinstance(ticket, dict):
        #     self.ticket = Ticket(**ticket)
        # elif isinstance(ticket, Ticket) or ticket == None:
        #     self.ticket = ticket
        # else:
        #     raise TypeError("'ticket' must be of type `Ticket`, `dict` or `None`.")

    def _post_unserialize(self, data):
        # Tags
        super()._unserialize(data)

    def _serialize(self):
        data = {
            "logged_at": self.logged_at.timestamp if self.logged_at else None,
            "subject": self.subject,
            "content": self.content,
            "category": self.category,
            "ticket_link": self.ticket_link
        }
        
        # Tags
        data.update(super()._serialize())

        return data
