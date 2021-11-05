import arrow

from tinydb import Query

from .base import Base
from .taggable import Taggable
from cartaro.utils.db_helper import DbHelper

class WorkDay(Taggable, Base):
    TYPE_NORMAL = "normal"
    TYPE_PTO = "pto"
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
        if isinstance(new_date, arrow.Arrow) or new_date is None:
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
        self.tags = data.get('tags', self.tags)

    def _serialize(self):
        data = {
            "date": self.date.int_timestamp if self.date else None,
            "time_in": self.time_in,
            "time_out": self.time_out,
            "note": self.note,
            "type": self.type
        }
        
        # Tags
        data.update(super()._serialize())

        return data

    @classmethod
    def range(cls, start, end=None, days=None):
        start_date = start
        end_date = end
        
        if not isinstance(start, arrow.Arrow):
            start_date = arrow.get(start).replace(tzinfo=cls.TIMEZONE)

        if end and not isinstance(end, arrow.Arrow):
            end_date = arrow.get(end).replace(tzinfo=cls.TIMEZONE)

        if days:
            if days > 0:
                end_date = start_date.shift(days=days)
            elif days < 0:
                end_date = start_date
                start_date = end_date.shift(days=days)

        db = cls._database()

        Day = Query()
        docs = db.search(Day.date.test(lambda value, s, e: s <= value <= e, start_date.int_timestamp, end_date.int_timestamp))
        docs = DbHelper.sort(docs, 'date')

        work_days = []
        for doc in docs:
            work_days.append(cls(id=doc.doc_id, **doc))

        return work_days
