import arrow
import datetime
import unittest

from cartaro.model.work_day import WorkDay
from cartaro.model.taggable import Taggable

class WorkDayTest(unittest.TestCase):

    def setUp(self):
        WorkDay.purge()

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

        with self.assertRaisesRegex(TypeError, 'must be of type INT, STR or Arrow'):
            self.work_day.date = [2021, 1, 18]

    def test_hours(self):
        self.assertEqual(self.work_day.hours, 7.5)

        wd = WorkDay(time_in='10:30', time_out='10:31')
        self.assertEqual(wd.hours, 0.02)

        wd = WorkDay(time_in='10:30', time_out='11:00')
        self.assertEqual(wd.hours, 0.5)

        wd = WorkDay(time_in='10:45', time_out='11:00')
        self.assertEqual(wd.hours, 0.25)

        wd = WorkDay(time_in='9:00', time_out='15:40')
        self.assertEqual(wd.hours, 6.67)

        wd = WorkDay(time_in='9:05', time_out='17:05')
        self.assertEqual(wd.hours, 8.0)

    def test_serialize(self):
        data = self.work_day.serialize()

        self.assertEqual(self.work_day.date.int_timestamp, data['date'])
        self.assertEqual(self.work_day.time_in, data['time_in'])
        self.assertEqual(self.work_day.time_out, data['time_out'])
        self.assertEqual(self.work_day.note, data['note'])
        self.assertEqual(self.work_day.type, data['type'])

    def test_range(self):
        date = arrow.get("2020-01-01").replace(tzinfo=WorkDay.TIMEZONE)
        for i in range(0,180):
            wd = WorkDay(
                date=date,
                time_in="09:00",
                time_out="16:30",
                note=F"Test WorkDay #{i}"
            )
            wd.save()
            date = date.shift(days=+1)

        self.assertEqual(WorkDay.count(), 180)

        # Two dates
        day_range = WorkDay.range('2020-01-01', '2020-01-31')
        self.assertEqual(len(day_range), 31)
        self.assertIsInstance(day_range[0], WorkDay)
        self.assertEqual(day_range[0].date.int_timestamp, arrow.get("2020-01-01").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)
        self.assertEqual(day_range[30].date.int_timestamp, arrow.get("2020-01-31").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)

        # Defined range by date and delta days POSITIVE
        day_range = WorkDay.range('2020-02-19', days=+7)
        self.assertEqual(len(day_range), 8) # 8 b/c inclusive
        self.assertIsInstance(day_range[0], WorkDay)
        self.assertEqual(day_range[0].date.int_timestamp, arrow.get("2020-02-19").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)
        self.assertEqual(day_range[7].date.int_timestamp, arrow.get("2020-02-26").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)

        # Defined range by date and delta days NEGATIVE
        day_range = WorkDay.range('2020-02-19', days=-7)
        self.assertEqual(len(day_range), 8) # 8 b/c inclusive
        self.assertIsInstance(day_range[0], WorkDay)
        self.assertEqual(day_range[0].date.int_timestamp, arrow.get("2020-02-12").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)
        self.assertEqual(day_range[7].date.int_timestamp, arrow.get("2020-02-19").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)







#
