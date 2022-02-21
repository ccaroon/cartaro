import arrow
from . import TimeOff

class Personal(TimeOff):
    TABLE_NAME = "personal"

    def __init__(self, id=None, **kwargs):
        self.type = None
        self.year = None
        self.accrual = None
        self.starting_balance = 0.0

        super().__init__(id=id, **kwargs)

    def _serialize(self):
        data =  {
            'type': self.type,
            'year': self.year,
            'accrual': None,
            'starting_balance': self.starting_balance,
        }

        if self.accrual_rate and self.accrual_period:
            data['accrual'] = {
                'rate': self.accrual_rate,
                'period': self.accrual_period
            }

        return data

    @property
    def accrual_rate(self):
        return self.accrual.get('rate') if self.accrual else None

    @property
    def accrual_period(self):
        return self.accrual.get('period') if self.accrual else None

    def update(self, data):
        self.type = data.get('type', self.type)
        self.year = data.get('year', self.year)
        self.accrual = data.get('accrual', self.accrual)
        self.starting_balance = data.get('starting_balance', self.starting_balance)

    # def total(self, period=12):
    #     """Total PTO accrued for the given period of time"""

    #     accruable = 0.0
    #     if self.accrual:
    #         accruable = self.accrual_rate * (self.accrual_period * period)

    #     return accruable + self.starting_balance

    # def available(self):
    #     """Available PTO given the current month"""
    #     total = self.total()
    #     curr_month = arrow.now().month

    #     avail = total * (curr_month/self.accrual_period)
    #     return avail
