import arrow
from . import TimeOff
from cartaro.model.work_day import WorkDay

class Personal(TimeOff):
    TABLE_NAME = "personal"

    def __init__(self, id=None, **kwargs):
        self.type = None
        self.year = None
        self.accrual = None
        self.starting_balance = 0.0
        self.__used = 0.0

        super().__init__(id=id, **kwargs)

    def _serialize(self):
        data =  {
            'type': self.type,
            'year': self.year,
            'accrual': None,
            'starting_balance': self.starting_balance,
            'used': self.used
        }

        if self.accrual_rate and self.accrual_period:
            data['accrual'] = {
                'rate': self.accrual_rate,
                'period': self.accrual_period,
                'cap': self.accrual_cap
            }

        return data

    @property
    def accrual_rate(self):
        return self.accrual.get('rate') if self.accrual else None

    @property
    def accrual_period(self):
        return self.accrual.get('period') if self.accrual else None

    @property
    def accrual_cap(self):
        return self.accrual.get('cap') if self.accrual else None

    @property
    def used(self):
        self.__used = self.__compute_used()
        return self.__used

    @used.setter
    def used(self, new_used):
        self.__used = new_used

    def update(self, data):
        self.type = data.get('type', self.type)
        self.year = data.get('year', self.year)
        self.accrual = data.get('accrual', self.accrual)
        self.starting_balance = data.get('starting_balance', self.starting_balance)
        self.used = data.get('used', self.__used)

    def __loadWorkDays(self):
        # Beginning of year
        startDate = arrow.get(F"{self.year}-01-01")

        endDate = arrow.now()
        if self.year != endDate.year:
            endDate = arrow.get(F"{self.year}-12-31")

        days = WorkDay.find(
            op="and",
            sort_by="date",
            type=self.type,
            date=F"btw:{startDate.int_timestamp}:{endDate.int_timestamp}"
        )
        return days

    def __compute_used(self):
        days = self.__loadWorkDays()

        used = 0.0
        for day in days:
            used += day.hours

        return used

    def available(self):
        return self.starting_balance + self.accrued_ytd()

    def balance(self):
        return self.available() - self.used

    def accrued_ytd(self):
        accrued = 0.0
        if self.accrual:
            now = arrow.now()
            if self.year < now.year:
                avail_months = 12
            elif self.year == now.year:
                avail_months = arrow.now().month
            elif self.year > now.year:
                avail_months = 0

            accrued = (avail_months / self.accrual_period) * self.accrual_rate

            # Can't accrue more than accrual.cap
            # Accrual *stops* when reach cap
            # Adjust for that
            if self.accrual_cap is not None:
                total_avail = (self.starting_balance + accrued) - self.used
                if total_avail >= self.accrual_cap:
                    accrued = accrued - (total_avail - self.accrual_cap)

        return accrued
