import arrow
import cartaro
import unittest

from cartaro.model.work_day import WorkDay
# ------------------------------------------------------------------------------
class WorkDaysControllerTest(unittest.TestCase):

    def __gen_work_days(self, start, count):
        date = arrow.get(start).replace(tzinfo=WorkDay.TIMEZONE)
        for i in range(0, count):
            wd = WorkDay(
                date=date,
                time_in="09:00",
                time_out="16:30",
                note=F"Test WorkDay #{i}"
            )
            wd.save()
            date = date.shift(days=+1)

    def setUp(self):
        # Setup Flask Testing
        cartaro.flask_app.config['TESTING'] = True
        self.client = cartaro.flask_app.test_client()

        WorkDay.purge()

    def test_range(self):
        self.__gen_work_days('1980-01-01', 90)

        #  Start & End
        r = self.client.get('/work_days/range?start=1980-02-01&end=1980-02-29')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        work_days = data.get('work_days', [])
        self.assertEqual(len(work_days), 29)
        self.assertEqual(work_days[0]['date'], arrow.get("1980-02-01").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)
        self.assertEqual(work_days[28]['date'], arrow.get("1980-02-29").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)

        #  Start & Days
        r = self.client.get('/work_days/range?start=1980-01-01&days=5')
        self.assertEqual(r.status_code, 200)

        data = r.get_json()
        work_days = data.get('work_days', [])
        self.assertEqual(len(work_days), 6)
        self.assertEqual(work_days[0]['date'], arrow.get("1980-01-01").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)
        self.assertEqual(work_days[5]['date'], arrow.get("1980-01-06").replace(tzinfo=WorkDay.TIMEZONE).int_timestamp)

        # Missing params - NO start
        r = self.client.get('/work_days/range?end=1980-02-01')
        self.assertEqual(r.status_code, 500)

        data = r.get_json()
        error_msg = data.get('error', None)
        self.assertRegex(error_msg, "Requires 'start' and either 'end' or 'days'")

        # Missing params - NO end or days
        r = self.client.get('/work_days/range?start=1980-02-01')
        self.assertEqual(r.status_code, 500)

        data = r.get_json()
        error_msg = data.get('error', None)
        self.assertRegex(error_msg, "Requires 'start' and either 'end' or 'days'")








#
