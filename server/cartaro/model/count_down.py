import arrow
from .base import Base


class CountDown(Base):
    def __init__(self, id=None, **kwargs):
        self.name = None
        self.__start_at = arrow.now(self.TIMEZONE)
        self.__end_at = None
        self.is_favorite = False

        super().__init__(id=id, **kwargs)

    @property
    def start_at(self):
        return self.__start_at

    @start_at.setter
    def start_at(self, new_date):
        self.__start_at = self._date_setter(new_date)

    @property
    def end_at(self):
        return self.__end_at

    @end_at.setter
    def end_at(self, new_date):
        self.__end_at = self._date_setter(new_date, null_ok=True)

    @property
    def duration(self):
        duration = None
        if self.start_at and self.end_at:
            duration = self.end_at.int_timestamp - self.start_at.int_timestamp

        return duration

    def _serialize(self):
        return {
            'name': self.name,
            'start_at': self.start_at.int_timestamp if self.start_at else None,
            'end_at': self.end_at.int_timestamp if self.end_at else None,
            'is_favorite': self.is_favorite,
            'duration': self.duration
        }

    def update(self, data):
        self.name = data.get('name', self.name)
        self.start_at = data.get('start_at', self.start_at)
        self.end_at = data.get('end_at', self.end_at)
        self.is_favorite = data.get('is_favorite', self.is_favorite)
