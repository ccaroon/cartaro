import arrow
import faker
import unittest

from cartaro.model.time_off.personal import Personal
class TimeOffPersonalTest(unittest.TestCase):

    def setUp(self):
        self.faker = faker.Faker()
        self.vacation = self.__test_instance(
            accrual = {
                'period': 1,
                'rate': 10.0
            }
        )

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

    # def test_total(self):
    #     total = self.vacation.total()
    #     accruable = self.vacation.accrual_rate * (self.vacation.accrual_period*12)

    #     self.assertEqual(total,
    #         accruable + self.vacation.starting_balance
    #     )

    # def test_available(self):
    #     month = arrow.now().month
    #     total = self.vacation.total()
    #     avail = self.vacation.available()

    #     self.assertEqual(avail, total * (month/self.vacation.accrual_period))
