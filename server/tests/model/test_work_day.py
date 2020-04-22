import arrow
import datetime
import unittest

from cartaro.model.work_day import WorkDay
from cartaro.model.taggable import Taggable

class WorkDayTest(unittest.TestCase):

    def setUp(self):
        self.work_day = WorkDay(
            date=arrow.now(),
            time_in="9:00",
            time_out="16:30",
            note="Just Another Day",
            type=WorkDay.TYPE_NORMAL
        )

    def test_basics(self):
        self.assertIsInstance(self.work_day, Taggable)
        self.assertIsInstance(self.work_day.date, arrow.Arrow)

    def test_date(self):
        self.work_day.date = 1
        self.assertIsInstance(self.work_day.date, arrow.Arrow)

        self.work_day.date = arrow.now()
        self.assertIsInstance(self.work_day.date, arrow.Arrow)

        with self.assertRaisesRegex(TypeError, 'must be of type INT or Arrow'):
            self.work_day.date = "now"

    def test_serialize(self):
        data = self.work_day.serialize()

        self.assertEqual(self.work_day.date.timestamp, data['date'])
        self.assertEqual(self.work_day.time_in, data['time_in'])
        self.assertEqual(self.work_day.time_out, data['time_out'])
        self.assertEqual(self.work_day.note, data['note'])
        self.assertEqual(self.work_day.type, data['type'])
