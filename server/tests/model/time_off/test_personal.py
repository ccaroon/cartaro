import arrow
import faker
import unittest

from cartaro.model.time_off.personal import Personal
from cartaro.model.work_day import WorkDay

class TimeOffPersonalTest(unittest.TestCase):

    def setUp(self):
        self.faker = faker.Faker()

    def __test_instance(self, **kwargs):
        data = {
            "type": kwargs.get("type",
                self.faker.random_element(('Vacation', 'Sick', 'Floating', 'Volunteer'))),
            "year": kwargs.get("year", arrow.now().year),
            "accrual": kwargs.get("accrual", None),
            "starting_balance": kwargs.get("starting_balance", self.faker.random_int(0,999))
        }
        return Personal(**data)

    def test_accrual_props(self):
        # with accrual
        pto = self.__test_instance(accrual={'rate': 12.5, 'period': 1})
        self.assertEqual(pto.accrual_rate, 12.5)
        self.assertEqual(pto.accrual_period, 1)

        # with-out accrual
        pto = self.__test_instance()
        self.assertEqual(pto.accrual_rate, None)
        self.assertEqual(pto.accrual_period, None)

    def test_serialize(self):
        # full data set
        pto = self.__test_instance(accrual={'rate': 10.0, 'period': 6})
        data = pto.serialize()

        self.assertEqual(pto.type, data['type'])
        self.assertEqual(pto.year, data['year'])
        self.assertIsNotNone(pto.accrual)
        self.assertEqual(pto.accrual_rate, data['accrual']['rate'])
        self.assertEqual(pto.accrual_period, data['accrual']['period'])
        self.assertEqual(pto.starting_balance, data['starting_balance'])

        # w/o accrual data i.e. accrual == None
        pto = self.__test_instance()
        data = pto.serialize()
        self.assertEqual(pto.type, data['type'])
        self.assertEqual(pto.year, data['year'])
        self.assertIsNone(pto.accrual)
        self.assertIsNone(pto.accrual_rate)
        self.assertIsNone(pto.accrual_period)
        self.assertEqual(pto.starting_balance, data['starting_balance'])

    def test_accrued_ytd(self):
        now = arrow.now()
        
        # Current Year
        pto = self.__test_instance(accrual={
            'rate': 12.5, 'period': 1
        })
        curr_month = now.month
        accrued = (curr_month / pto.accrual_period) * pto.accrual_rate

        self.assertEqual(pto.accrued_ytd(), accrued)

        # Previous Year
        pto = self.__test_instance(year=now.year-1, accrual={
            'rate': 12.5, 'period': 1
        })
        # All 12 months have been accrued
        accrued = (12 / pto.accrual_period) * pto.accrual_rate
        self.assertEqual(pto.accrued_ytd(), accrued)
        
        # Future Year
        pto = self.__test_instance(year=now.year+1, accrual={
            'rate': 12.5, 'period': 1
        })
        # No hours accrued
        self.assertEqual(pto.accrued_ytd(), 0)

    def test_available(self):
        curr_month = arrow.now().month
        pto = self.__test_instance(accrual={
            'rate': 10.0, 'period': 1
        })

        used = pto.used
        accrued = curr_month * pto.accrual_rate
        sb = pto.starting_balance

        self.assertEqual(pto.available(), (sb+accrued) - used)

    def test_used(self):
        numDays = 3
        pto = self.__test_instance(type="Vacation")

        # Add a few in-range NORMAL work days
        for i in range(0,numDays):
            day = WorkDay(
                date=arrow.now().shift(days=i*-1),
                time_in="9:00",
                time_out="16:30",
                note=F"Normal #{i}",
                type=WorkDay.TYPE_NORMAL
            )
            day.save()

        # Add a few in-range Vacation work days
        for i in range(numDays,numDays+numDays):
            day = WorkDay(
                date=arrow.now().shift(days=i*(-1)),
                time_in="00:00",
                time_out="00:00",
                note=F"Vacation #{i}",
                type=WorkDay.TYPE_VACATION
            )
            day.save()

        # Add a few out-of-range Vacation work days
        for i in range(0, numDays):
            day = WorkDay(
                date=arrow.now().shift(days=7+i),
                time_in="00:00",
                time_out="00:00",
                note=F"Future Vacation #{i}",
                type=WorkDay.TYPE_VACATION
            )
            day.save()

        self.assertEqual(pto.used, WorkDay.HOURS_PER_DAY * numDays)
