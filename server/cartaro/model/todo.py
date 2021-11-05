from .base import Base
from .taggable import Taggable

class Todo(Taggable, Base):

    # Defined in days
    REPEAT_UNITS ={
        'day': 1,
        'week': 7,
        'month': 30,
        'year': 365
    }

    def __init__(self, id=None, **kwargs):
        self.title = None
        self.description = None
        self.priority = None
        self.__due_at = None
        self.repeat = 0
        self.is_complete = False
        self.__completed_at = None
        
        super().__init__(id=id, **kwargs)

    @property
    def due_at(self):
        return self.__due_at

    @due_at.setter
    def due_at(self, new_date):
        self.__due_at = self._date_setter(new_date, null_ok=True)

    @property
    def completed_at(self):
        return self.__completed_at

    @completed_at.setter
    def completed_at(self, new_date):
        self.__completed_at = self._date_setter(new_date, null_ok=True)

    def _serialize(self):
        data =  {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_at': self.due_at.int_timestamp if self.due_at else None,
            'repeat': self.repeat,
            'is_complete': self.is_complete,
            'completed_at': self.completed_at.int_timestamp if self.completed_at else None,
        }

        # Tags
        data.update(super()._serialize())

        return data

    def update(self, data):
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.priority = data.get('priority', self.priority)
        self.due_at = data.get('due_at', self.due_at)
        self.repeat = data.get('repeat', self.repeat)
        self.is_complete = data.get('is_complete', self.is_complete)
        self.completed_at = data.get('completed_at', self.completed_at)
        self.tags = data.get('tags', self.tags)





# 
