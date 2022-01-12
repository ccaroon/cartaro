import arrow
import unittest

from cartaro.model.time_off.personal import Personal
class TimeOffPersonalTest(unittest.TestCase):

    def setUp(self):
        self.vacation = Personal(
            type="vacation",
            accrual_rate=10.0,
            accrual_period=1,
            rollover=42.5
        )

    def test_serialize(self):
        data = self.vacation.serialize()

        self.assertEqual(self.vacation.type, data['type'])
        self.assertEqual(self.vacation.accrual_rate, data['accrual_rate'])
        self.assertEqual(self.vacation.accrual_period, data['accrual_period'])
        self.assertEqual(self.vacation.rollover, data['rollover'])

    def test_total(self):
        total = self.vacation.total()
        accruable = self.vacation.accrual_rate * (self.vacation.accrual_period*12)

        self.assertEqual(total,
            accruable + self.vacation.rollover
        )

    def test_available(self):
        month = arrow.now().month
        total = self.vacation.total()
        avail = self.vacation.available()

        self.assertEqual(avail, total * (month/self.vacation.accrual_period))
