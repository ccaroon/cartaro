from . import TimeOff

class Personal(TimeOff):
    TABLE_NAME = "personal"

    # All time off reflected in hours
    # accrual period reflected in months
    def __init__(self, id=None, **kwargs):
        self.type = None
        self.accrual_rate = None
        self.accrual_period = None
        self.rollover = 0.0

        # rethink accrual vs. when given (once per year)

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

    def balance(self):
        # TODO: fix this math
        return self.accrual_rate * self.accrual_period
