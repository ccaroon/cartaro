import arrow

from .base import Base
from .taggable import Taggable

class WorkDay(Taggable, Base):
    TYPE_NORMAL = "normal"
    TYPE_PTO = "pto "
    TYPE_SICK = "sick"
    TYPE_HOLIDAY = "holiday"

    def __init__(self, id=None, **kwargs):
        self.__date = None
        self.time_in = None
        self.time_out = None
        self.note = None
        self.type = self.TYPE_NORMAL

        super().__init__(id=id, **kwargs)

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, new_date):
        if isinstance(new_date, arrow.Arrow):
            self.__date = new_date
        elif isinstance(new_date, int):
            self.__date = self._epoch_to_date_obj(new_date)
        else:
            raise TypeError("'date' must be of type INT or Arrow")

    def update(self, data):
        self.date = data.get('date', self.date)
        self.time_in = data.get('time_in', self.time_in)
        self.time_out = data.get('time_out', self.time_out)
        self.note = data.get('note', self.note)
        self.type = data.get('type', self.type)

    def _post_unserialize(self, data):
        # Tags
        super()._unserialize(data)

    def _serialize(self):
        data = {
            "date": self.date.timestamp if self.date else None,
            "time_in": self.time_in,
            "time_out": self.time_out,
            "note": self.note,
            "type": self.type
        }
        
        # Tags
        data.update(super()._serialize())

        return data
