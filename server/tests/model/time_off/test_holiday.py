# import arrow
import unittest

from cartaro.model.time_off.holiday import Holiday
class TimeOffHolidayTest(unittest.TestCase):

    def setUp(self):
        self.holiday = Holiday(
            name="Christmas",
            date="2025-12-25"
        )

    def test_serialize(self):
        data = self.holiday.serialize()

        self.assertEqual(self.holiday.name, data['name'])
        self.assertEqual(self.holiday.date.int_timestamp, data['date'])
