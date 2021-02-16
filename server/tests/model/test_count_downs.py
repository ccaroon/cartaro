import arrow
import datetime
import unittest

from cartaro.model.count_down import CountDown

class CountDownTest(unittest.TestCase):

    def setUp(self):
        self.countdown = CountDown(
            name = "Test Countdown",
            start_at = arrow.utcnow(),
            end_at = arrow.utcnow().shift(days=+4)
        )

    def test_basics(self):
        self.assertIsInstance(self.countdown.start_at, arrow.Arrow)
        self.assertIsInstance(self.countdown.end_at, arrow.Arrow)

    def test_duration(self):
        now = arrow.utcnow()

        countdown = CountDown(
            name = "Thing1",
            start_at = now,
            end_at = now.shift(seconds=30)
        )

        self.assertEqual(countdown.duration, 30)

        countdown.end_at = now.shift(minutes=42)
        self.assertEqual(countdown.duration, 42*60)

        countdown.end_at = now.shift(days=3)
        self.assertEqual(countdown.duration, 3*24*60*60)

    def test_serialize(self):
        data = self.countdown.serialize()

        self.assertEqual(self.countdown.name, data['name'])
        self.assertEqual(self.countdown.start_at.timestamp, data['start_at'])
        self.assertEqual(self.countdown.end_at.timestamp, data['end_at'])
        self.assertEqual(self.countdown.duration, data['duration'])
