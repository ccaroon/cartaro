import arrow
import datetime
import unittest

from cartaro.model.log_entry import LogEntry
from cartaro.model.taggable import Taggable

class LogEntryTest(unittest.TestCase):

    def setUp(self):
        self.entry = LogEntry(
            logged_at=datetime.datetime.now().timestamp(),
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update",
            ticket_link="https://jira.example.com/browse/CNC-42"
        )

    def test_basics(self):
        self.assertIsInstance(self.entry, Taggable)
        self.assertIsInstance(self.entry.logged_at, arrow.Arrow)

    def test_construction(self):
        # logged_at should default to now
        entry = LogEntry(
            subject="Just Another Day",
            content="Just another day at sea. Lost. Hopeless.",
            category="Mourning Update"
        )
        self.assertIsNotNone(entry.logged_at)
        self.assertAlmostEqual(entry.logged_at.timestamp, arrow.now().timestamp)

    def test_serialize(self):
        data = self.entry.serialize()

        self.assertEqual(self.entry.logged_at.timestamp, data['logged_at'])
        self.assertEqual(self.entry.subject, data['subject'])
        self.assertEqual(self.entry.content, data['content'])
        self.assertEqual(self.entry.category, data['category'])
        self.assertEqual(self.entry.ticket_link, data['ticket_link'])
