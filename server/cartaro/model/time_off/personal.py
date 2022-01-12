import arrow
from . import TimeOff

class Personal(TimeOff):
    TABLE_NAME = "personal"

    def __init__(self, id=None, **kwargs):
        self.type = None
        self.accrual_rate = None # in hours
        self.accrual_period = None # in months
        self.rollover = 0.0

        super().__init__(id=id, **kwargs)

    def _serialize(self):
        data =  {
            'type': self.type,
            'accrual_rate': self.accrual_rate,
            'accrual_period': self.accrual_period,
            'rollover': self.rollover,
        }

        return data

    def update(self, data):
        self.type = data.get('type', self.type)
        self.accrual_rate = data.get('accrual_rate', self.accrual_rate)
        self.accrual_period = data.get('accrual_period', self.accrual_period)
        self.rollover = data.get('rollover', self.rollover)

    def total(self, period=12):
        """Total PTO accrued for the given period of time"""
        
        accruable = self.accrual_rate * (self.accrual_period * period)
        return accruable + self.rollover

    def available(self):
        """Available PTO given the current month"""
        total = self.total()
        curr_month = arrow.now().month

        avail = total * (curr_month/self.accrual_period)
        return avail
