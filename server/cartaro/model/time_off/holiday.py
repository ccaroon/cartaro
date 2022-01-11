import arrow
from . import TimeOff

class Holiday(TimeOff):
    TABLE_NAME = "holidays"

    def __init__(self, id=None, **kwargs):
        self.name = None
        self.__date = arrow.now(self.TIMEZONE)

        super().__init__(id=id, **kwargs)

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, new_date):
        self.__date = self._date_setter(new_date)

    def _serialize(self):
        data =  {
            'name': self.name,
            'date': self.date.timestamp if self.date else None,
        }

        return data

    def update(self, data):
        self.name = data.get('name', self.name)
        self.date = data.get('date', self.date)
